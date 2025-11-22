# python3 matmul.py A_dense.parquet B_dense.parquet C_dir --A_size 5000 --B_size 5000

import polars as pl
import os
import time
import argparse

def dense_block_matmul(A_parquet, B_parquet, C_dir, A_size=5000, B_size=5000):
    """
    Perform dense block matrix multiplication using Polars LazyFrame and save each block to Parquet.
    """

    # Create output directory if it doesn't exist
    os.makedirs(C_dir, exist_ok=True)

    # ----------------------------
    # 1. Read LazyFrames
    # ----------------------------
    A_lf = pl.scan_parquet(A_parquet)  # Each column is a dense column
    B_lf = pl.scan_parquet(B_parquet)

    # Get matrix sizes
    A_df = A_lf.collect()
    B_df = B_lf.collect()
    A_nrows = A_df.height
    B_ncols = B_df.width


    # ----------------------------
    # 2. Block-wise matrix multiplication
    # ----------------------------
    current_A_row = 0
    block_idx = 0
    start_time = time.time()

    while current_A_row < A_nrows:
        end_A_row = min(current_A_row + A_size, A_nrows)
        A_block = A_lf.slice(current_A_row, end_A_row - current_A_row).collect()

        current_B_col = 0
        while current_B_col < B_ncols:
            end_B_col = min(current_B_col + B_size, B_ncols)
            B_block_cols = B_lf.columns[current_B_col:end_B_col]
            B_block = B_lf.select(B_block_cols).collect()

            # Convert to NumPy for block multiplication
            A_np = A_block.to_numpy()
            B_np = B_block.to_numpy()
            C_np = A_np @ B_np  # Dense block multiplication

            # Save block to Parquet
            C_block_file = os.path.join(C_dir, f"C_block_{block_idx}.parquet")
            C_block = pl.DataFrame(C_np.tolist())
            C_block.write_parquet(C_block_file)

            print(f"Block {block_idx} done: A rows {current_A_row}-{end_A_row}, B cols {current_B_col}-{end_B_col}")

            current_B_col = end_B_col
            block_idx += 1

        current_A_row = end_A_row

    end_time = time.time()
    print(f"Dense block matrix multiplication finished in {end_time - start_time:.2f} s")


# ----------------------------
# CLI using argparse
# ----------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Dense block matrix multiplication using Polars LazyFrame")
    parser.add_argument("A_parquet", help="Input Parquet file for matrix A")
    parser.add_argument("B_parquet", help="Input Parquet file for matrix B")
    parser.add_argument("C_dir", help="Output directory to store block Parquet files")
    parser.add_argument("--A_size", type=int, default=5000, help="Number of rows per block for A")
    parser.add_argument("--B_size", type=int, default=5000, help="Number of columns per block for B")

    args = parser.parse_args()
    dense_block_matmul(args.A_parquet, args.B_parquet, args.C_dir, args.A_size, args.B_size)
