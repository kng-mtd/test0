import polars as pl
import argparse

def transpose_parquet(input_path, output_path):
    """
    Transpose a Parquet numeric matrix created without headers.
    No extra header row is inserted.
    """

    # Read entire Parquet (pure numeric matrix)
    df = pl.read_parquet(input_path)

    # Transpose WITHOUT header row
    dfT = df.transpose(include_header=False)

    # Rename columns: col0, col1, ...
    dfT.columns = [f"col{i}" for i in range(dfT.width)]

    # Save
    dfT.write_parquet(output_path)

    print(f"Transposed written to: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transpose a Parquet numeric matrix.")
    parser.add_argument("input", type=str, help="Input Parquet file path")
    parser.add_argument("output", type=str, help="Output Parquet file path")

    args = parser.parse_args()

    transpose_parquet(args.input, args.output)
