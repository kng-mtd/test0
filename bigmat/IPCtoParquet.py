import pyarrow.ipc as ipc
import polars as pl
import argparse
import os

def arrowipc_to_parquet_chunked(ipc_path, parquet_path):
    """
    Convert ArrowIPC / Feather to Parquet with all columns as float32 in batches
    """
    if not os.path.exists(ipc_path):
        print(f"Error: ArrowIPC file not found: {ipc_path}")
        return

    print(f"Opening ArrowIPC: {ipc_path}")
    reader = ipc.open_file(ipc_path)
    num_batches = reader.num_record_batches
    print(f"Total record batches: {num_batches}")

    # Remove existing Parquet file if exists
    if os.path.exists(parquet_path):
        os.remove(parquet_path)

    for i in range(num_batches):
        batch = reader.get_batch(i)
        df = pl.from_arrow(batch)

        # Cast all columns to float32
        df = df.with_columns([pl.col(c).cast(pl.Float32) for c in df.columns])

        # Append to Parquet
        if i == 0:
            df.write_parquet(parquet_path)  # first batch creates the file
        else:
            df.write_parquet(parquet_path, append=True)

        print(f"Processed batch {i} ({len(df)} rows)")

    print(f"Conversion finished: {parquet_path}")

# ----------------------------
# CLI using argparse
# ----------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Chunked ArrowIPC / Feather to Parquet (float32)")
    parser.add_argument("ipc_path", help="Input ArrowIPC / Feather file path")
    parser.add_argument("parquet_path", help="Output Parquet file path")

    args = parser.parse_args()
    arrowipc_to_parquet_chunked(args.ipc_path, args.parquet_path)
