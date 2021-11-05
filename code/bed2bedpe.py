import os
import sys

bedf = sys.argv[1]
bedpe = sys.argv[2]
namecol = int(sys.argv[3])
resolution = int(sys.argv[4])

if resolution >0:
	bed_dict = {}
	name_list = []
	for line in open(bedf):
			cols = line.rstrip().split("\t")
			start = int((int(cols[1]) + int(cols[2]))/2) - int(resolution)/2
			end = int((int(cols[1]) + int(cols[2]))/2) + int(resolution)/2
			bed_dict[cols[namecol-1]] = [cols[0], start, end]
			name_list.append(cols[namecol-1])

	out = open(bedpe, "w")
	name_len = len(name_list)
	for k1i in range(0,name_len):
			key1 = name_list[k1i]
			for k2i in range(k1i+1,name_len):
					key2 = name_list[k2i]
					out.write("%s\t%d\t%d\t%s\t%d\t%d\t%s\n" %(bed_dict[key1][0], bed_dict[key1][1], bed_dict[key1][2],
						bed_dict[key2][0],bed_dict[key2][1],bed_dict[key2][2],key1+"_"+key2))
	out.close()
else:
	bed_dict = {}
	name_list = []
	for line in open(bedf):
			cols = line.rstrip().split("\t")
			start = cols[1]
			end = cols[2]
			bed_dict[cols[namecol-1]] = [cols[0], start, end]
			name_list.append(cols[namecol-1])

	out = open(bedpe, "w")
	name_len = len(name_list)
	for k1i in range(0,name_len):
			key1 = name_list[k1i]
			for k2i in range(k1i+1,name_len):
					key2 = name_list[k2i]
					out.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\n" %(bed_dict[key1][0], bed_dict[key1][1], bed_dict[key1][2],
						bed_dict[key2][0],bed_dict[key2][1],bed_dict[key2][2],key1+"_"+key2))
	out.close()
