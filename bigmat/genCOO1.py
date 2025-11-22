# make a sparse COO CSV by probabilistic sampling, no duplicate checking

import csv
import random

def generate_coo_csv(path, nrows, ncols, density=1e-6):
    """
    Generate ultra-sparse COO CSV for very large matrices using pure probabilistic sampling.
    No memory-heavy set for duplicate checking.
    Suitable for very low density matrices.
    """
    print(f"Generating ultra-sparse COO CSV (~{density*100:.4f}% density)")

    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["row", "col", "val"])

        for i in range(nrows):
            # Expected number of non-zeros in this row
            nnz_row = int(ncols * density)
            for _ in range(nnz_row):
                j = random.randint(0, ncols - 1)
                v = round(random.uniform(1, 10), 2)
                writer.writerow([i, j, v])

    print(f"sparse CSV generated: {path}")

if __name__ == "__main__":
    generate_coo_csv("A_coo.csv", nrows=2000, ncols=1000, density=1e-3)
    generate_coo_csv("B_coo.csv", nrows=1000, ncols=2000, density=1e-3)