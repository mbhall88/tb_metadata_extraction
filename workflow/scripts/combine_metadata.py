import sys

sys.stderr = open(snakemake.log[0], "w")

import pandas as pd
from multiprocessing import Pool


def func(path):
    return pd.read_csv(path, sep="\t")


with Pool(snakemake.threads) as pool:
    frames = pool.map(func, snakemake.input.metadata, chunksize=100)

df = pd.concat(frames)

df.to_csv(snakemake.output.sheet, sep="\t", index=False)
