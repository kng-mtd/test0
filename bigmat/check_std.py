import polars as pl
import math
import argparse

def check_standardized_parquet_lazy(parquet_path, col_chunk=5000, tol=1e-6):
    """
    Check each column of a standardized Parquet file (lazy, memory-efficient).
    Print only columns where mean != 0 or std != 1.
    
    Args:
        parquet_path (str): Path to standardized Parquet file
        col_chunk (int): Number of columns to process per block
        tol (float): Tolerance for numerical comparison
    """
    print(f"Checking standardized Parquet (lazy) for {parquet_path}")
    
    # LazyFrame for memory efficiency
    lf = pl.scan_parquet(parquet_path)
    all_cols = lf.collect_schema().names()
    print(f"Total columns: {len(all_cols)}")
    
    for i in range(0, len(all_cols), col_chunk):
        chunk_cols = all_cols[i:i+col_chunk]
        print(f"Processing columns {i} -> {i+len(chunk_cols)-1}")
        
        # Compute mean and std for this column block
        stats = lf.select(chunk_cols).collect().to_dict(as_series=True)
        
        for c in chunk_cols:
            col = stats[c]
            mean = col.mean()
            std = col.std()
            # Skip empty columns
            if mean is None or std is None:
                print(f"Column '{c}': no data, skipped")
                continue
            if not math.isclose(mean, 0.0, abs_tol=tol) or not math.isclose(std, 1.0, abs_tol=tol):
                print(f"Column '{c}': mean={mean:.6f}, std={std:.6f}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Memory-efficient check of standardized Parquet columns")
    parser.add_argument("parquet", help="Path to standardized Parquet file")
    parser.add_argument("--chunk", type=int, default=5000, help="Number of columns per block")
    parser.add_argument("--tol", type=float, default=1e-6, help="Tolerance for mean/std check")
    args = parser.parse_args()

    check_standardized_parquet_lazy(args.parquet, col_chunk=args.chunk, tol=args.tol)
