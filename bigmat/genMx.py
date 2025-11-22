import os
import numpy as np
import polars as pl
import pyarrow as pa
import pyarrow.parquet as pq
import pyarrow.ipc as ipc


def generate_dummy_csv(path, rows, cols):
    print(f'Generating headerless CSV: {path} ({rows}x{cols})')
    
    # Generate random NumPy array
    data = np.random.rand(rows, cols).astype(np.float32)
    
    # Write CSV without header
    np.savetxt(path, data, delimiter=',')
    
    print(f'CSV written: {path}')



def generate_dummy_parquet(path, rows, cols):
    print(f'Generating Parquet with PyArrow: {path} ({rows}x{cols})')

    # Generate random NumPy array
    data = np.random.rand(rows, cols).astype(np.float32)

    # Convert each column to Arrow array
    arrays = [pa.array(data[:, i], type=pa.float32()) for i in range(cols)]

    # Create Arrow Table
    table = pa.Table.from_arrays(arrays, names=[f'col{i}' for i in range(cols)])

    # Write Parquet (compressed, very fast)
    pq.write_table(table, path, compression='snappy')

    print(f'Parquet written: {path}')



def generate_parquet_row_chunked(path, rows, cols, row_chunk=10000):
    """
    Generate a huge Parquet file by chunking over rows.
    Best when rows are huge but columns are reasonable.
    """
    print(f"Generating Parquet (row-chunked): {path} ({rows} x {cols})")

    # Remove existing file
    if os.path.exists(path):
        os.remove(path)

    writer = None

    for start in range(0, rows, row_chunk):
        end = min(rows, start + row_chunk)
        n_rows = end - start

        print(f"Generating rows {start}–{end}")

        # Generate only row chunk
        data_chunk = np.random.rand(n_rows, cols).astype(np.float32)

        # Convert to Arrow Table
        arrays = [pa.array(data_chunk[:, i], type=pa.float32()) for i in range(cols)]
        table = pa.Table.from_arrays(arrays, names=[f'col{i}' for i in range(cols)])

        # Initialize Parquet writer
        if writer is None:
            writer = pq.ParquetWriter(path, table.schema, compression="snappy")

        writer.write_table(table)

    if writer:
        writer.close()

    print("Done (row-chunked).")


def generate_parquet_col_chunked(path, rows, cols, col_chunk=2000):
    """
    Generate a huge Parquet file by chunking over columns.
    Best when columns are huge (10k+).
    """
    print(f"Generating Parquet (col-chunked): {path} ({rows} x {cols})")

    # Remove existing file
    if os.path.exists(path):
        os.remove(path)

    writer = None

    for start_col in range(0, cols, col_chunk):
        end_col = min(cols, start_col + col_chunk)
        n_cols = end_col - start_col

        print(f"Generating cols {start_col}–{end_col}")

        # Generate only this column chunk
        data_chunk = np.random.rand(rows, n_cols).astype(np.float32)

        # Convert to Arrow Table
        arrays = [pa.array(data_chunk[:, i], type=pa.float32()) for i in range(n_cols)]
        table = pa.Table.from_arrays(
            arrays,
            names=[f'col{c}' for c in range(start_col, end_col)]
        )

        # Initialize Parquet writer
        if writer is None:
            writer = pq.ParquetWriter(path, table.schema, compression="snappy")

        writer.write_table(table)

    if writer:
        writer.close()

    print("Done (col-chunked).")


def generate_parquet_2d_tiled(out_dir, rows, cols,
                              row_block=5000, col_block=5000):
    """
    Generate a huge matrix in 2D tiles (row_block × col_block) Parquet files.
    Safe when both rows and cols are very large.
    """
    os.makedirs(out_dir, exist_ok=True)

    print(f"Generating HUGE matrix: {rows} x {cols}")
    print(f"Block size: {row_block} x {col_block}")

    n_row_blocks = (rows + row_block - 1) // row_block
    n_col_blocks = (cols + col_block - 1) // col_block

    for bi in range(n_row_blocks):
        row_start = bi * row_block
        row_end = min(rows, row_start + row_block)
        n_r = row_end - row_start

        for bj in range(n_col_blocks):
            col_start = bj * col_block
            col_end = min(cols, col_start + col_block)
            n_c = col_end - col_start

            print(f"Generating block ({bi}, {bj}) → rows {row_start}-{row_end}, cols {col_start}-{col_end}")

            # Create 2D tile (small enough)
            data_chunk = np.random.rand(n_r, n_c).astype('float32')

            # Convert to Arrow table
            arrays = [pa.array(data_chunk[:, j]) for j in range(n_c)]
            table = pa.Table.from_arrays(
                arrays,
                names=[f'col{col_start + j}' for j in range(n_c)]
            )

            # Save as block file
            out_file = f"{out_dir}/tile_{bi:04d}_{bj:04d}.parquet"
            pq.write_table(table, out_file, compression='zstd')

    print("✓ DONE: 2D tiled matrix generated.")



def generate_dummy_arrowIPC(path, rows, cols, compression='lz4'):
    print(f'Generating Arrow IPC: {path} ({rows}x{cols})')

    data = np.random.rand(rows, cols).astype(np.float32)
    arrays = [pa.array(data[:, i], type=pa.float32()) for i in range(cols)]
    table = pa.Table.from_arrays(arrays, names=[f'col{i}' for i in range(cols)])

    dir_name = os.path.dirname(path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)

    with ipc.new_file(path, table.schema, options=ipc.IpcWriteOptions(compression=compression)) as writer:
        writer.write(table)

    print(f'Arrow IPC written: {path}')



if __name__ == '__main__':
    generate_dummy_csv('A.csv', rows=2000, cols=1000)
    generate_dummy_csv('B.csv', rows=1000, cols=2000)

    # generate_dummy_parquet('A.parquet', rows=2000, cols=1000)
    # generate_dummy_parquet('B.parquet', rows=1000, cols=2000)

    # generate_parquet_row_chunked('A.parquet', rows=2000, cols=1000)
    # generate_parquet_row_chunked('B.parquet', rows=1000, cols=2000)

    # generate_parquet_col_chunked('A.parquet', rows=2000, cols=1000)
    # generate_parquet_col_chunked('B.parquet', rows=1000, cols=2000)

    # generate_parquet_2d_tiled('A_tiles', rows=20000, cols=15000,
    #                           row_block=5000, col_block=5000)
    # generate_parquet_2d_tiled('B_tiles', rows=15000, cols=20000,
    #                           row_block=5000, col_block=5000)

    # huge_csv_to_parquet("A.csv", "A.parquet")
    # huge_csv_to_parquet("B.csv", "B.parquet")

    # generate_dummy_arrowIPC('A.arrow', rows=2000, cols=1000)
    # generate_dummy_arrowIPC('B.arrow', rows=1000, cols=2000)

