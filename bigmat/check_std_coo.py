import polars as pl
import math
import argparse

def check_standardized_coo(parquet_path, total_rows, tol=1e-6):
    """
    Check each column of a standardized COO Parquet file (row, col, val).
    Print only columns where mean != 0 or std != 1.
    row/col are cast to int32 for safety.
    """
    print(f"Checking standardized COO Parquet: {parquet_path}")

    # Read as LazyFrame for memory efficiency
    coo = pl.scan_parquet(parquet_path).with_columns([
        pl.col("row").cast(pl.Int32),
        pl.col("col").cast(pl.Int32),
        pl.col("val").cast(pl.Float32)
    ])
    
    # Compute mean and std per column
    stats = (
        coo.group_by("col")
        .agg([
            pl.col("val").sum().alias("sum_nz"),
            (pl.col("val")**2).sum().alias("sum_sq_nz")
        ])
        .with_columns([
            (pl.col("sum_nz") / total_rows).alias("mean"),
            ((pl.col("sum_sq_nz") / total_rows) - (pl.col("sum_nz") / total_rows) ** 2).alias("var")
        ])
        .with_columns([
            pl.col("var").clip(1e-12, None).sqrt().alias("std")
        ])
        .select(["col", "mean", "std"])
        .with_columns([
            pl.col("col").cast(pl.Int32)
        ])
        .collect()
    )

    print(stats)

    # Check for deviations
    for row in stats.iter_rows():
        col_idx, mean, std = row

        # Skip columns with no data
        if mean is None or std is None:
            continue

        if not math.isclose(mean, 0.0, abs_tol=tol) or not math.isclose(std, 1.0, abs_tol=tol):
            print(f"Column {col_idx}: mean={mean:.6f}, std={std:.6f}")

# ----------------------------
# CLI
# ----------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check standardized COO Parquet columns")
    parser.add_argument("parquet", help="Path to standardized COO Parquet file")
    parser.add_argument("-n", type=int, required=True, help="Total number of rows in the full matrix")
    parser.add_argument("--tol", type=float, default=1e-6, help="Tolerance for mean/std check")
    args = parser.parse_args()

    check_standardized_coo(args.parquet, args.n, tol=args.tol)
