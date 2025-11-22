# python3 stdCOO.py A_coo.parquet Astd_coo.parquet -n 2000 --chunk 1000000

import polars as pl
import pyarrow.parquet as pq
import pyarrow as pa
import argparse
import os
import math

def standardize_coo_parquet(input_path, output_path, total_rows, chunk_size=1_000_000):
    """
    Standardize each column of a COO Parquet file using true mean/std
    where zeros are implicit (COO contains only nonzero values).
    row/col are cast to int32.
    """

    if os.path.exists(output_path):
        os.remove(output_path)

    # ---------------------------------------------------
    # Step 1: Compute corrected mean/std for each column
    # ---------------------------------------------------
    print(f"Computing corrected column-wise mean/std for: {input_path}")
    coo = pl.read_parquet(input_path)

    # Cast row/col to int32 for safety
    coo = coo.with_columns([
        pl.col("row").cast(pl.Int32),
        pl.col("col").cast(pl.Int32),
        pl.col("val").cast(pl.Float32)
    ])

    # aggregate nonzero stats
    stats = (
        coo.group_by("col")
        .agg([
            pl.col("val").sum().alias("sum_nz"),
            (pl.col("val")**2).sum().alias("sum_sq_nz")
        ])
        .with_columns([
            (pl.col("sum_nz") / total_rows).alias("mean"),
            (
                (pl.col("sum_sq_nz") / total_rows)
                - (pl.col("sum_nz") / total_rows) ** 2
            ).alias("var")
        ])
        .with_columns([
            pl.col("var").clip(1e-12, None).sqrt().alias("std")
        ])
        .select(["col", "mean", "std"])
        .with_columns([
            pl.col("col").cast(pl.Int32)  # cast stats col to int32
        ])
    )

    print(f"Computed stats for {stats.height} columns")

    # ---------------------------------------------------
    # Step 2: Process in chunks
    # ---------------------------------------------------
    meta = pq.read_metadata(input_path)
    max_rows = meta.num_rows
    print(f"Processing {max_rows} rows in chunks of {chunk_size}")

    offset = 0
    first_chunk = True

    while offset < max_rows:
        print(f"Processing rows {offset} -> {min(offset+chunk_size, max_rows)}")

        chunk = pl.scan_parquet(input_path).slice(offset, chunk_size).collect()

        # cast row/col in each chunk
        chunk = chunk.with_columns([
            pl.col("row").cast(pl.Int32),
            pl.col("col").cast(pl.Int32),
            pl.col("val").cast(pl.Float32)
        ])

        # Standardize values safely
        chunk_std = (
            chunk.join(stats, on="col")
            .with_columns([
                pl.when(pl.col("std").is_null() | (pl.col("std") == 0))
                .then(0.0)
                .otherwise((pl.col("val") - pl.col("mean")) / pl.col("std"))
                .alias("val")
            ])
            .select(["row", "col", "val"])
        )

        table = chunk_std.to_arrow()

        if first_chunk:
            pq.write_table(table, output_path)
            first_chunk = False
        else:
            pq.write_table(table, output_path, append=True)

        offset += chunk_size

    print(f"Done. Standardized COO Parquet written to {output_path}")


# ----------------------------
# CLI
# ----------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Standardize columns of COO Parquet using true mean/std (zeros implicit)")
    parser.add_argument("input_path", help="Input COO Parquet file")
    parser.add_argument("output_path", help="Output standardized COO Parquet file")
    parser.add_argument("-n", type=int, required=True, help="Total number of rows in the full matrix")
    parser.add_argument("--chunk", type=int, default=1_000_000, help="Chunk size for processing")
    args = parser.parse_args()

    standardize_coo_parquet(args.input_path, args.output_path, args.n, args.chunk)
