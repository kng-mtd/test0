# make a dense COO CSV by looping over all positions, avoiding duplicates 

import csv
import random

def generate_coo_csv(path, nrows, ncols, density=1e-3):
    print(f"Generating COO CSV with ~{density*100:.3f}% density ({nrows}x{ncols})")
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["row", "col", "val"])

        for i in range(nrows):
            for j in range(ncols):
                if random.random() < density:
                    v = round(random.uniform(1, 10), 2)
                    writer.writerow([i, j, v])

    print(f"CSV generated: {path}")


if __name__ == "__main__":
    generate_coo_csv("A_coo.csv", nrows=2000, ncols=1000, density=1e-3)
    generate_coo_csv("B_coo.csv", nrows=1000, ncols=2000, density=1e-3)
