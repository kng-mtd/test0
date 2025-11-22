# python3 tpCOO.py A_coo.parquet AT_coo.parquet

import polars as pl
import pyarrow.parquet as pq
import argparse
import os

def transpose_coo_parquet_chunked(input_parquet, output_parquet, chunk_size=1_000_000):
    """
    Transpose a COO Parquet safely in chunks to avoid memory overflow.
    """
    print(f"Transposing {input_parquet} → {output_parquet}")
    if os.path.exists(output_parquet):
        os.remove(output_parquet)

    # get number of rows from metadata
    meta = pq.read_metadata(input_parquet)
    total_rows = meta.num_rows
    print(f"Total rows: {total_rows}, chunk_size: {chunk_size}")

    offset = 0
    first_chunk = True

    while offset < total_rows:
        print(f"Processing rows {offset} -> {min(offset + chunk_size, total_rows)}")

        # slice chunk and collect
        chunk = pl.scan_parquet(input_parquet).slice(offset, chunk_size).collect()

        # swap row/col
        chunk = chunk.select([
            pl.col("col").alias("row"),
            pl.col("row").alias("col"),
            pl.col("val")
        ])

        # convert to Arrow Table
        table = chunk.to_arrow()

        # write/append to Parquet
        if first_chunk:
            pq.write_table(table, output_parquet)
            first_chunk = False
        else:
            pq.write_table(table, output_parquet, append=True)

        offset += chunk_size

    print("Transpose completed.")

# ----------------------------
# CLI
# ----------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Chunked transpose of COO Parquet file")
    parser.add_argument("input_parquet", help="Input COO Parquet path")
    parser.add_argument("output_parquet", help="Output transposed Parquet path")
    parser.add_argument("--chunk_size", type=int, default=1_000_000, help="Rows per chunk")
    args = parser.parse_args()

    transpose_coo_parquet_chunked(args.input_parquet, args.output_parquet, args.chunk_size)
