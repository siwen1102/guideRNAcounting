import re
import sys
import pandas as pd

spacer_df = pd.read_csv('guide_RNA_seq.txt', header = None, names = ['spacer'])
spacer_df['count'] = 0

fastq_file = 'sequenced_guides.fastq'
file = open(fastq_file, "r")

for line in file:
    for i in range(spacer_df.shape[0]):
        s = spacer_df['spacer'][i]
        if re.search(s, line):
            spacer_df.loc[i, 'count'] = spacer_df.loc[i, 'count'] + 1


print(spacer_df)
