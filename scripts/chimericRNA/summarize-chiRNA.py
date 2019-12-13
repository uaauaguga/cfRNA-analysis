import pandas as pd
import numpy as np
import os
from tqdm import tqdm


parser = argparse.ArgumentParser(description='Summarize chimeric RNA Results')
parser.add_argument('--indir', '-i', type=str, required=True, help='input dir contain all results, *abridged.tsv')
parser.add_argument('--output','-o',type=str,required=True,help='output path')
args = parser.parse_args()


