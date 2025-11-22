# python3 COOtoParquet.py A_coo.csv A_coo.parquet

import pyarrow as pa
import pyarrow.csv as csv
import pyarrow.parquet as pq
import argparse
import os

def csv_coo_to_parquet(csv_path, parquet_path, block_size=32*1024*1024):
    """
    Convert a huge COO CSV (row, col, val) into Parquet using pure PyArrow streaming.
    row/col -> int32, val -> float32
    """

    if not os.path.exists(csv_path):
        print(f"Error: CSV file not found: {csv_path}")
        return

    # overwrite old parquet
    if os.path.exists(parquet_path):
        os.remove(parquet_path)

    print(f"Converting {csv_path} → {parquet_path}")
    print(f"Block size: {block_size} bytes")

    # schema
    schema = pa.schema([
        ("row", pa.int32()),
        ("col", pa.int32()),
        ("val", pa.float32()),
    ])

    # CSV conversion options
    convert_opts = csv.ConvertOptions(
        column_types={
            "row": pa.int32(),
            "col": pa.int32(),
            "val": pa.float32(),
        }
    )

    read_opts = csv.ReadOptions(
        block_size=block_size,
        use_threads=True
    )

    # create streaming CSV reader
    reader = csv.open_csv(
        csv_path,
        read_options=read_opts,
        convert_options=convert_opts
    )

    writer = None
    total_rows = 0

    for i, batch in enumerate(reader):
        # convert RecordBatch to Table
        table = pa.Table.from_batches([batch], schema=schema)

        if writer is None:
            writer = pq.ParquetWriter(parquet_path, schema)

        writer.write_table(table)

        total_rows += table.num_rows
        print(f"  Batch {i+1}: {table.num_rows} rows (total {total_rows})")

    if writer:
        writer.close()

    print(f"Done. Total rows: {total_rows}")
    print(f"Output: {parquet_path}")


# ----------------------------
# CLI
# ----------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert huge COO CSV (header: row,col,val) to Parquet (float32, chunked)."
    )
    parser.add_argument("csv_path", help="Input CSV file")
    parser.add_argument("parquet_path", help="Output Parquet file")
    parser.add_argument("--chunksize", type=int, default=1_000_000,
                        help="Rows per chunk (default: 1M)")
    args = parser.parse_args()

    csv_coo_to_parquet(args.csv_path, args.parquet_path, args.chunksize)
