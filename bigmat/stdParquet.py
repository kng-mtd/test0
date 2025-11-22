# python3 stdParquet.py input.parquet output.parquet --col_chunk 1000

import polars as pl
import argparse
import math

def standardize_parquet(input_path, output_path, col_chunk=1000):
    """
    Standardize columns of a Parquet file to mean 0, std 1.
    """
    lf = pl.scan_parquet(input_path)
    all_cols = lf.collect_schema().names()  # Avoid PerformanceWarning
    standardized_chunks = []

    print(f"Total columns: {len(all_cols)}")
    
    for i in range(0, len(all_cols), col_chunk):
        chunk_cols = all_cols[i:i+col_chunk]
        print(f"Processing columns {i} -> {i+len(chunk_cols)-1}")

        # Compute mean and std for each column in chunk
        agg_exprs = []
        for c in chunk_cols:
            agg_exprs.append(pl.col(c).mean().alias(f"{c}_mean"))
            agg_exprs.append(pl.col(c).std().alias(f"{c}_std"))
        stats = lf.select(agg_exprs).collect()[0]

        # Generate standardized columns
        standardized_exprs = []
        for c in chunk_cols:
            mean = stats[f"{c}_mean"].item()
            std  = stats[f"{c}_std"].item()
            if std is None or math.isclose(std, 0.0):
                standardized_exprs.append(pl.lit(0.0).alias(c))
            else:
                standardized_exprs.append(((pl.col(c) - mean)/std).alias(c))

        standardized_chunk = lf.select(standardized_exprs).collect()
        standardized_chunks.append(standardized_chunk)

    # Concatenate column blocks horizontally
    result = pl.concat(standardized_chunks, how="horizontal")
    result.write_parquet(output_path)
    print(f"Standardized Parquet saved to: {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Standardize columns of a Parquet file")
    parser.add_argument("input", help="Input Parquet file path")
    parser.add_argument("output", help="Output Parquet file path")
    parser.add_argument("--col_chunk", type=int, default=1000, help="Number of columns per block")
    args = parser.parse_args()

    standardize_parquet(args.input, args.output, args.col_chunk)
