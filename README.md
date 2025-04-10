# Fecit
ugly wraper that runs Fec(https://github.com/zhangjuncsu/Fec) itteratively for each chromosome/contig larger than 1000000 bases.
Mainly intended for using on ONT data prior to de novo assembly through tools such as hifiasm.

    python fecit.py input.bam output_dir

The tool will perform error correction on reads aligned to each contig larger than 1mbp, the rest will not be error corrected.
The final output is stored in output_dir/combined_and_corrected.fasta.gz

# Requirements
make a conda environment containing samtools, Fec and minimap2

Fecit requires pysam and python 3

# Preprocessing
the input of fecit is an indexed and sorted bam file containing the reads to be corrected. Alignment may be performed using minimap2
