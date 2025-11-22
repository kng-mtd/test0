import pyarrow as pa
import pyarrow.parquet as pq
import polars as pl
import os
import argparse

def transpose_parquet_blockwise(input_path, output_path, block_cols=1000):
    # Read full table to get row/col counts
    table = pq.read_table(input_path)
    total_rows = table.num_rows
    total_cols = table.num_columns
    col_names = table.column_names
    if not col_names:
        col_names = [f"col{i}" for i in range(total_cols)]

    if os.path.exists(output_path):
        os.remove(output_path)

    print(f"Transposing {input_path} ({total_rows}x{total_cols}) in blocks of {block_cols} columns")

    # Create ParquetWriter for output
    writer = None

    for start_col in range(0, total_cols, block_cols):
        end_col = min(total_cols, start_col + block_cols)
        cols = col_names[start_col:end_col]

        # Load block with Polars
        df_block = pl.read_parquet(input_path).select(cols)

        # Transpose block
        dfT = df_block.transpose(include_header=False)

        # Convert Polars -> PyArrow Table
        tableT = pa.Table.from_arrays([dfT[col].to_numpy() for col in dfT.columns],
                                      names=[f"col{i}" for i in range(dfT.width)])

        # Initialize writer
        if writer is None:
            writer = pq.ParquetWriter(output_path, tableT.schema)
        
        # Write block
        writer.write_table(tableT)

        print(f"Processed columns {start_col}-{end_col}")

    writer.close()
    print(f"Transposed Parquet written: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transpose a Parquet numeric matrix.")
    parser.add_argument("input", type=str, help="Input Parquet file path")
    parser.add_argument("output", type=str, help="Output Parquet file path")

    args = parser.parse_args()

    transpose_parquet_blockwise(args.input, args.output)
