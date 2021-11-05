import straw
import os
import sys

hicf = sys.argv[1]
chrom_list = sys.argv[2].split(",")
resolution = int(sys.argv[3])
norm_method = sys.argv[4]
outf = sys.argv[5]

out = open(outf, "w")
for chrom in chrom_list:
	result = straw.straw(norm_method, hicf, chrom, chrom, 'BP', resolution)
	# the values returned are in x / y / counts
	for i in range(len(result[0])):
		out.write("chr{0}\t{1}\t{2}\tchr{3}\t{4}\t{5}\t{6}\n".format(chrom,result[0][i], result[0][i]+resolution,chrom, result[1][i], result[1][i]+resolution,  result[2][i]))
out.close()
