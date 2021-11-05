import sys
import os

###Input: 1.genelist 
#		  2. ABC model output in specific cell line (e.g.GM12878)
###Output: a bed file with promoter and Enhancer regions for each gene

def retrieve_enhancer_region(ABCModel_Input):
	promoter_dict = {} ###gene: [[chr,start,end]...]
	enhancer_dict = {} ###gene: [[chr,start,end]...]
	for line in open(ABCModel_Input):
		cols = line.rstrip().split("\t")
		region_type = cols[4]
		gene_id = cols[6]
		chrom = cols[0]
		start = cols[1]
		end = cols[2]
		###isSelfPromoter
		if region_type=="promoter" and cols[12] == "True":
			if not promoter_dict.has_key(gene_id):
				promoter_dict[gene_id] = []
			promoter_dict[gene_id].append([chrom, start, end])
		else:
			if not enhancer_dict.has_key(gene_id):
				enhancer_dict[gene_id] = []
			enhancer_dict[gene_id].append([chrom, start, end])
	return promoter_dict, enhancer_dict

def output_EP(GeneList_Input, promoter_dict, enhancer_dict, OutputPath):
	for line in open(GeneList_Input):
		gene_id = line.rstrip()
		os.popen("mkdir %s/%s" %(OutputPath, gene_id))
		EP_output_file = "%s/%s/Promoter_enhancers.bed" %(OutputPath, gene_id)
		E_output_file = "%s/%s/Enhancers.bed" %(OutputPath, gene_id)
		EP_out = open(EP_output_file, "w")
		E_out = open(E_output_file, "w")
		pn = 0
		en = 0
		if promoter_dict.has_key(gene_id):
			for p in promoter_dict[gene_id]:
				pn += 1
				EP_out.write("%s\t%s\t%s\t%s%d\t%s\n" %(p[0],p[1],p[2],"Promoter_",pn,gene_id))
		else: print "Error!! Can't find gene %s!!" %gene_id
		if enhancer_dict.has_key(gene_id):
			for e in enhancer_dict[gene_id]:
				en += 1
				EP_out.write("%s\t%s\t%s\t%s%d\t%s\n" %(e[0],e[1],e[2],"Enhancer_",en,gene_id))
				E_out.write("%s\t%s\t%s\t%s%d\t%s\n" %(e[0],e[1],e[2],"Enhancer_",en,gene_id))
		else: print "Error!! Can't find gene %s!!" %gene_id
		EP_out.close()
		E_out.close()

def main():
	GeneList_Input = sys.argv[1]
	ABCModel_Input = sys.argv[2]
	OutputPath = sys.argv[3]
	promoter_dict, enhancer_dict = retrieve_enhancer_region(ABCModel_Input)
	output_EP(GeneList_Input, promoter_dict, enhancer_dict, OutputPath)

if __name__=='__main__':
	main()
