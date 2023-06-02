# reading in the fastq file
# using self-defined dictionary
import os

# define a dictionary to save different types data accordingly
def process_read(lines):
    ks = ['name', 'sequence', 'optional', 'quality']
    return {k:v for k ,v in zip(ks, lines)}
    
# extract the sequences of the fastq file
def get_sequence(fastq_file):
    if not os.path.exists(fastq_file):
        raise SystemError("Error: File does not exist.  Check spelling? ¯\_(ツ)_/¯ \n")
        
    
    seqs = []
    n_lines_per_record = 4
    with open(fastq_file, 'r') as fq:
        lines = []
        for line in fq:
            lines.append(line.rstrip())
            if len(lines) == n_lines_per_record:
                record = process_read(lines)
                seqs.append(record['sequence'])
                lines = []
            
    return seqs
    
    
    
    
    
s = get_sequence("sequenced_guides.fastq")
print(s)