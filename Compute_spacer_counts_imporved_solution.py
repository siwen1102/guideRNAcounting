import os
import pandas as pd
import sqlalchemy
import sqlite3


def process_data(lines):
    kv = ['name', 'sequence', 'optional', 'quality']
    return {k:v for k,v in zip(kv, lines)}

def extract_sequences(fastq_file):
    if not os.path.exists(fastq_file):
        raise SystemError("Error: there is no fastq_file in the current directory")
    
    seqs = []
    n_lines_per_record = 4
    with open(fastq_file, 'r') as f:
        lines = []
        for line in f:
            lines.append(line.rstrip())
            if(len(lines) == n_lines_per_record):
                record = process_data(lines)
                seqs.append(record['sequence'])
                lines = []
    return seqs


spacer_list = []
with open("guide_RNA_seq.txt", 'r') as in_f:
    for line in in_f:
        spacer_list.append(line.rstrip())

spacer_length = 20
scaffold_sequence = 'GTTTAAGAGCTAAGCTGGA'
# define a spacer_dict with key is each spacer, value is 0
spacer_dict = {}
for spacer in spacer_list:
    spacer_dict[spacer] = 0

seqs = extract_sequences("sequenced_guides.fastq")
for seq in seqs:
    scaf_pos = seq.find(scaffold_sequence)
    spacer_pos = scaf_pos - spacer_length
    # to test if the spacer position valid
    if spacer_pos >= 0:
        spacer_test = seq[spacer_pos:(spacer_pos+spacer_length)]
        if spacer_test in spacer_dict:
            spacer_dict[spacer_test] += 1

# build the counter dataframe
counter_df = pd.DataFrame(spacer_dict.items(), columns = ['seq', 'count'])
#print(counter_df.head())
#counter_df.to_excel("spacer_counter.xlsx")

# create an in-memory SQLite database
engine = sqlalchemy.create_engine('sqlite:///counter_sql.db')
# write DataFrame to database table
counter_df.to_sql('counter_sql', con = engine, if_exists='replace')
#from sqlalchemy import text
#with engine.connect() as conn:
#    print(conn.execute(text("select * from counter_sql")).fetchall())
counter_sql = pd.read_sql('counter_sql', engine)
print(counter_sql)