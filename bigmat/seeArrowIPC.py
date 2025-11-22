#python3 seeArrowIPC.py ---.arrow

import argparse
import pyarrow.ipc as ipc
import polars as pl

def seeArrowIPC(path, nrows=10):
    """
    Show number of rows, columns, and first 10 rows of an Arrow IPC file.
    """
    df = pl.read_ipc(path)
    n_rows = df.height
    n_cols = df.width
    print(f'File: {path}')
    print(f'Rows: {n_rows}, Columns: {n_cols}')
    print('First rows:')
    print(df.head(nrows))



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Quickly inspect an Arrow IPC file.")
    parser.add_argument("arrow", help="Path to Arrow IPC file")
    args = parser.parse_args()

    seeArrowIPC(args.arrow)