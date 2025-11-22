# python3 CSVtoParquet1.py A.csv A.parquet

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import argparse
import os

def csv_to_parquet_float32_pyarrow(csv_path, parquet_path, chunksize=1_000_000):
    """
    Convert large CSV to a single Parquet file safely using PyArrow ParquetWriter.
    All columns are cast to float32. Suitable for huge CSV files.
    """
    if not os.path.exists(csv_path):
        print(f"Error: CSV file not found: {csv_path}")
        return

    # Remove output if exists
    if os.path.exists(parquet_path):
        os.remove(parquet_path)

    writer = None
    total_rows = 0
    for i, df_chunk in enumerate(pd.read_csv(csv_path, header=None, chunksize=chunksize)):
        # Cast all columns to float32
        df_chunk = df_chunk.astype('float32')

        # Convert to PyArrow Table
        table = pa.Table.from_pandas(df_chunk)

        # Initialize writer on first chunk
        if writer is None:
            writer = pq.ParquetWriter(parquet_path, table.schema)

        # Write chunk
        writer.write_table(table)
        total_rows += table.num_rows
        print(f"Written chunk {i+1} with {table.num_rows} rows (total {total_rows})")

    if writer:
        writer.close()

    print(f"Conversion completed: {parquet_path}, total rows: {total_rows}")

# ----------------------------
# CLI
# ----------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert huge CSV to Parquet safely (float32, chunked, single file)"
    )
    parser.add_argument("csv_path", help="Input CSV file path")
    parser.add_argument("parquet_path", help="Output Parquet file path")
    parser.add_argument("--chunksize", type=int, default=1_000_000, help="Rows per chunk")
    args = parser.parse_args()

    csv_to_parquet_float32_pyarrow(args.csv_path, args.parquet_path, args.chunksize)

