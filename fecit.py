import sys
import pysam
import os

#ugly wraper that runs Fec(https://github.com/zhangjuncsu/Fec) itteratively for each chromosome/contig larger than 1000000 bases

#accepts a bam file and an output dir

#python fecit.py input.bam output_dir

min_ctg_length=1000000
threads=16

if os.path.isdir(sys.argv[2]):
	print("error folder exists")
	print("delete the folder or change the output dir name")
	quit()

os.system(f"mkdir {sys.argv[2]}")

samfile = pysam.AlignmentFile(sys.argv[1], "rb" )
header=samfile.header



os.system(f"samtools fasta -f 4 {sys.argv[1]} | bgzip -@ {threads} -c - > {sys.argv[2]}/unaligned.fasta.gz")

chromosomes=[]
for contig in header["SQ"]:
	if contig["LN"] > min_ctg_length:
		chromosomes.append(contig["SN"])
		continue

	os.system(f"samtools view -buh {sys.argv[1]} {contig["SN"]} | samtools fasta - | bgzip -@ {threads} -c - >> {sys.argv[2]}/unaligned.fasta.gz")

awk_cmd="awk '{ if($4 - $3 >= 0.2 * $2 || $9 - $8 >= 0.2 * $7) print $0}'"
for chromosome in chromosomes:
	os.system(f"samtools view -buh {sys.argv[1]} {chromosome} | samtools fastq - > {sys.argv[2]}/reads.fq")
	os.system(f"minimap2 -x ava-ont -w 20 -K 2g -f 0.0005 -t {threads} {sys.argv[2]}/reads.fq {sys.argv[2]}/reads.fq | {awk_cmd} > {sys.argv[2]}/ovlp.paf")
	os.system(f"Fec -x 1 -t {threads} -r 0.6 -a 400 -c 0 -l 1000 -m 0.005 -f 0.2 {sys.argv[2]}/ovlp.paf {sys.argv[2]}/reads.fq {sys.argv[2]}/corrected_{chromosome}.fasta")
	os.system(f"bgzip -@ {threads} {{sys.argv[2]}/corrected_{chromosome}.fasta}")

os.system(f"cat {sys.argv[2]}/corrected_* {sys.argv[2]}/unaligned.fasta.gz > {sys.argv[2]}/combined_and_corrected.fasta.gz")
