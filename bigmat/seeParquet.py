#python3 seeParquet.py ---.parquet

import argparse
import polars as pl
import pyarrow.parquet as pq

def seeParquet(parquet_path):
    """
    Show number of rows, columns, and first 5 rows of a Parquet file.
    """
    # --- PyArrow for metadata ---
    pq_file = pq.ParquetFile(parquet_path)
    total_rows = pq_file.metadata.num_rows
    total_cols = len(pq_file.schema)

    print(f"File: {parquet_path}")
    print(f"Number of rows: {total_rows}")
    print(f"Number of columns: {total_cols}")

    # --- Polars LazyFrame for first 10 rows ---
    lf = pl.scan_parquet(parquet_path)
    print("\nFirst 10 rows:")
    print(lf.head(10).collect())



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Quickly inspect a Parquet file.")
    parser.add_argument("parquet", help="Path to Parquet file")
    args = parser.parse_args()

    seeParquet(args.parquet)


