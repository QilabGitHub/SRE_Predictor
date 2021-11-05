import os
import sys
import glob
from scipy import stats
import numpy as np

def bw_signal(chr,start,end,bw_file,calculation_type):
	shell = 'bigWigSummary %s %s %s %s 1 -type=%s' %(bw_file, chr, str(start), str(end),calculation_type)
	#print shell
	if os.popen(shell).read() == '':
		#signal_value = "NaN"
		signal_value = 0.0
	else:
		signal_value = float(os.popen(shell).read().rstrip())
	return signal_value

def main():
	bedf = sys.argv[1]
	outn = sys.argv[2]
	bwf_path = sys.argv[3]
	flank = int(sys.argv[4])
	zscore_cal = int(sys.argv[5])
	#out = open(outf, 'w')
	region_dict = {}
	region_lists = []
	for line in open(bedf):
		cols = line.rstrip().split('\t')
		region_name = cols[3]
		chrom, start, end = cols[0], int(cols[1])-flank, int(cols[2]) + flank
		region_dict[region_name] = [chrom, start, end]
		region_lists.append(region_name)	
	out_max_m = open(outn + ".txt", "w") 
	for r1 in region_lists:
		for r2 in region_lists:
			rp = r1 + "|" + r2
			out_max_m.write("%s\t" %rp)
	out_max_m.write("\n")

	for bwf in glob.glob(bwf_path + '/*.bigWig'):
		#print bwf
		tf_hm_name = bwf.split("/")[-1].split("_")[1]
		out_max_m.write(tf_hm_name)
		region_bw_mean_dict = {}
		region_bw_max_dict = {}
		for r in region_lists:
			chrom, start, end = region_dict[r][0], region_dict[r][1], region_dict[r][2]
			signal_value_mean = bw_signal(chrom, start, end, bwf, "mean")
			signal_value_max = bw_signal(chrom, start, end, bwf, "max")
			region_bw_mean_dict[r] = signal_value_mean
			region_bw_max_dict[r] = signal_value_max
		if zscore_cal==1:
			region_bw_mean_zscore = stats.zscore(np.array(region_bw_mean_dict.values()))
			region_bw_max_zscore = stats.zscore(np.array(region_bw_max_dict.values()))

		for r1 in region_lists:
			for r2 in region_lists:
				if zscore_cal==1:
					r1_index = region_dict.keys().index(r1)
					r2_index = region_dict.keys().index(r2)
					out_max_m.write("\t%.2f" %(region_bw_max_zscore[r1_index] * region_bw_max_zscore[r2_index]))
				else:
					out_max_m.write("\t%.2f" %(region_bw_max_dict[r1] * region_bw_max_dict[r2]))

		out_max_m.write("\n")
	
if __name__=='__main__':
	main()
