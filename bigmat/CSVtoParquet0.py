# python3 CSVtoParquet0.py A_coo.csv A_coo.parquet

import polars as pl
import argparse
import os

def csv_to_parquet(csv_path, parquet_path, chunksize=100000):
    """
    Convert CSV (no header) to Parquet with float32 dtype
    """
    # Check if CSV file exists
    if not os.path.exists(csv_path):
        print(f"Error: CSV file not found: {csv_path}")
        return

    # Lazy read CSV without header (comma is default)
    print(f"Reading CSV: {csv_path}")
    lf = pl.scan_csv(csv_path, has_header=False)

    # Collect LazyFrame
    df = lf.collect()

    # Rename columns to default names: col_0, col_1, ...
    df.columns = [f"col_{i}" for i in range(len(df.columns))]

    # Convert all columns to float32
    df = df.with_columns([pl.col(c).cast(pl.Float32) for c in df.columns])
    print(f"Converted all columns to float32")

    # Write to Parquet
    print(f"Writing Parquet: {parquet_path}")
    df.write_parquet(parquet_path)
    print("Conversion finished.")

# ----------------------------
# CLI using argparse
# ----------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert headerless CSV to Parquet (float32, large files)")
    parser.add_argument("csv_path", help="Input CSV file path")
    parser.add_argument("parquet_path", help="Output Parquet file path")
    parser.add_argument("--chunksize", type=int, default=10**6,
                        help="Chunk size for processing (currently unused, placeholder for future enhancements)")

    args = parser.parse_args()
    csv_to_parquet(args.csv_path, args.parquet_path, args.chunksize)
