import os
import sys

def retrieve_interaction(region1_dict, region1_region2_dict, raw_matrix, expected_list, resolution):
	region1_keys = region1_dict.keys()

	for line in open(raw_matrix):
		cols = line.rstrip().split()
		r1 = cols[0]
		r2 = cols[1]
		interaction = cols[2]
		if r1 in region1_keys and r2 in region1_keys:	
			expected = expected_list[(int(r2)-int(r1))/resolution] ###(((41000000-40000000)/5000)+1=21)
			#region1_region2_dict[r1][r2] = [interaction, float(interaction)/float(expected)]
			#print interaction
			#print expected
			region1_region2_dict[r1][r2] = [interaction, float(interaction)/(float(expected)+0.0001)]
		else:
			continue
	return region1_region2_dict


def output(region1_region2_dict, region1_dict, output_file):
	out = open(output_file, "w")
	region_keys = region1_region2_dict.keys()
	region_keys.sort()
	out.write("%s\t%s" %("",region_keys[0]+"_"+region1_dict[region_keys[0]]))
	for rk in region_keys[1:]:
		#print rk + "_"+ region1_dict[rk]
		out.write("\t%s" %(rk + "_"+ region1_dict[rk]))
	out.write("\n")

	for rk1 in region_keys:
		out.write("%s" %(rk1+"_"+region1_dict[rk1]))
		for rk2 in region_keys:
			if region1_region2_dict[rk1].has_key(rk2):
				if region1_region2_dict[rk1][rk2]!=0:
					###each have O O/E output observe
					out.write("\t%s" %(region1_region2_dict[rk1][rk2][0]))
				else:
					out.write("\t%s" %("NA"))
			else:
				if region1_region2_dict[rk2][rk1]!=0:
					out.write("\t%s" %(region1_region2_dict[rk2][rk1][0]))
				else:
					out.write("\t%s" %("NA"))
		out.write("\n")
	out.close()

def main():
	region_inf = sys.argv[1]
	raw_matrix = sys.argv[2]
	expected_file = sys.argv[3]
	output_file = sys.argv[4]
	resolution = int(sys.argv[5])
	region1_dict = {}
	region1_region2_dict = {}
	for line in open(region_inf):
		cols = line.rstrip().split("\t")
		region1_center = str((int(cols[1]) + int(cols[2]))/2/resolution*resolution)
		region1_dict[region1_center] = cols[3]
	keys = region1_dict.keys()
	keys.sort()
	for ki in range(0,len(keys)):
		region1_region2_dict[keys[ki]] = {}
		for kj in range(ki,len(keys)):
			region1_region2_dict[keys[ki]][keys[kj]] = 0

	expected_list = []
	for line in open(expected_file):
		expected_list.append(line.rstrip())
		
	#print region1_region2_dict
	region1_region2_dict = retrieve_interaction(region1_dict,region1_region2_dict,raw_matrix,expected_list, resolution)
	output(region1_region2_dict, region1_dict, output_file)


if __name__=="__main__":
	main()
