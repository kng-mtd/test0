# python3 COOmul.py A_coo.parquet B_coo.parquet C_coo.parquet --chunk 5000000 --chunk_B 1000000

import polars as pl
import pyarrow.parquet as pq
import os
import argparse

def matmul_coo_parquet_full_chunked(A_path, B_path, C_path, chunk_A=5_000_000, chunk_B=1_000_000):
    """
    Compute C = A x B with both A and B chunked to limit memory usage.
    Writes C to Parquet incrementally.
    """

    # Remove old output
    if os.path.exists(C_path):
        os.remove(C_path)

    # Number of rows in A
    meta_A = pq.read_metadata(A_path)
    maxA = meta_A.num_rows
    print(f"A has {maxA} nonzero entries (COO rows)")

    # Number of rows in B
    meta_B = pq.read_metadata(B_path)
    maxB = meta_B.num_rows
    print(f"B has {maxB} nonzero entries (COO rows)")

    first_chunk = True

    offset_A = 0
    while offset_A < maxA:
        print(f"Processing A chunk: rows {offset_A} -> {min(offset_A+chunk_A, maxA)}")
        A_chunk = (
            pl.scan_parquet(A_path)
            .slice(offset_A, chunk_A)
            .select(["row", "col", "val"])
            .collect()
        )

        if A_chunk.height == 0:
            break

        # Initialize an empty Polars DataFrame to accumulate partial results
        partial_results = None

        offset_B = 0
        while offset_B < maxB:
            print(f"  Processing B chunk: rows {offset_B} -> {min(offset_B+chunk_B, maxB)}")
            B_chunk = (
                pl.scan_parquet(B_path)
                .slice(offset_B, chunk_B)
                .select(["row", "col", "val"])
                .collect()
            )

            if B_chunk.height == 0:
                break

            # Multiply COO chunks
            joined = (
                A_chunk.join(B_chunk, left_on="col", right_on="row", how="inner")
                .with_columns((pl.col("val") * pl.col("val_right")).alias("mul"))
                .group_by(["row", "col_right"])
                .agg(pl.sum("mul").alias("val"))
                .rename({"col_right": "col"})
            )

            if partial_results is None:
                partial_results = joined
            else:
                # accumulate sums
                partial_results = (
                    partial_results.vstack(joined)
                    .group_by(["row", "col"])
                    .agg(pl.sum("val").alias("val"))
                )

            offset_B += chunk_B

        # Write the accumulated result of this A_chunk
        table = partial_results.to_arrow()
        if first_chunk:
            pq.write_table(table, C_path)
            first_chunk = False
        else:
            pq.write_table(table, C_path, append=True)

        offset_A += chunk_A

    print(f"Done. Wrote C: {C_path}")


# ----------------------------
# CLI
# ----------------------------
if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("A", help="COO Parquet A")
    ap.add_argument("B", help="COO Parquet B transposed")
    ap.add_argument("C", help="Output COO Parquet C")
    ap.add_argument("--chunk", type=int, default=5_000_000, help="Rows per chunk for A")
    ap.add_argument("--chunk_B", type=int, default=1_000_000, help="Rows per chunk for B")
    args = ap.parse_args()

    matmul_coo_parquet_full_chunked(args.A, args.B, args.C, chunk_A=args.chunk, chunk_B=args.chunk_B)
