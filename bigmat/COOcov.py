# python3 COOcov.py AT_coo.parquet A_coo.parquet cov_coo.parquet -n 2000 --chunk 1000000 --chunk_B 1000000

import polars as pl
import pyarrow.parquet as pq
import os
import argparse

def matmul_coo_parquet_cov(A_path, B_path, C_path, N_rows, chunk_A=1_000_000, chunk_B=1_000_000):
    """
    Compute C = A x B / (N_rows-1) with both A and B chunked.
    This is suitable for covariance / correlation computation.
    Writes C to Parquet incrementally.
    """

    # Remove old output
    if os.path.exists(C_path):
        os.remove(C_path)

    # Metadata
    meta_A = pq.read_metadata(A_path)
    maxA = meta_A.num_rows
    meta_B = pq.read_metadata(B_path)
    maxB = meta_B.num_rows
    print(f"A: {maxA} nonzero rows, B: {maxB} nonzero rows")

    first_chunk = True
    offset_A = 0

    while offset_A < maxA:
        print(f"Processing A chunk: {offset_A} -> {min(offset_A+chunk_A, maxA)}")
        A_chunk = (
            pl.scan_parquet(A_path)
            .slice(offset_A, chunk_A)
            .select(["row", "col", "val"])
            .collect()
        )

        if A_chunk.height == 0:
            break

        partial_results = None
        offset_B = 0

        while offset_B < maxB:
            print(f"  Processing B chunk: {offset_B} -> {min(offset_B+chunk_B, maxB)}")
            B_chunk = (
                pl.scan_parquet(B_path)
                .slice(offset_B, chunk_B)
                .select(["row", "col", "val"])
                .collect()
            )

            if B_chunk.height == 0:
                break

            # Multiply and scale by N_rows for covariance
            joined = (
                A_chunk.join(B_chunk, left_on="col", right_on="row", how="inner")
                .with_columns((pl.col("val") * pl.col("val_right")).alias("mul"))
                .group_by(["row", "col_right"])
                .agg((pl.sum("mul")/(N_rows-1)).alias("val"))
                .rename({"col_right": "col"})
            )

            if partial_results is None:
                partial_results = joined
            else:
                partial_results = (
                    partial_results.vstack(joined)
                    .group_by(["row", "col"])
                    .agg(pl.sum("val").alias("val"))
                )

            offset_B += chunk_B

        # Write partial results to Parquet
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
    ap.add_argument("-n", type=int, required=True, help="Total number of rows for scaling")
    ap.add_argument("--chunk", type=int, default=5_000_000, help="Rows per chunk for A")
    ap.add_argument("--chunk_B", type=int, default=1_000_000, help="Rows per chunk for B")
    args = ap.parse_args()

    matmul_coo_parquet_cov(args.A, args.B, args.C, N_rows=args.n, chunk_A=args.chunk, chunk_B=args.chunk_B)
