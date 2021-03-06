# SRE_Predictor
The SRE_Predictor predicts which enhancer pairs are synergistic regulatory enhancers (SREs) and which pairs are not. For important disease relevant genes, such as oncogenes in tumors, they are more likely to be regulated by multiple enhancers in ultralong distance. This tool focus on genes which are regulated by multiple genes (>=5 enhancers) spanning in ultralong distance (>=200Kb). Our multiplexed CRISPRi screen revealed an intergrated two-layer structure of these enhancers. The SREs are critical in maintating the robustness of gene expression upon perturbation. We applied the elastic net regularized linear regression model to train the SRE_Predictor Model and apply it to predict SREs in other gene loci across cell types which are regulated by multiple genes (>=5 enhancers) spanning in large regulatory landscapes (>=200Kb).


# Running the SRE_Predictor Model
Running the SRE_Predictor model consists of the following steps:
  1. Retrieve enhancer regions for target genes
  2. Calculate normalized spatial contacts between enhancer pairs 
  3. Calculate co-occupancy of chromatin features
  4. Compute interaction score to rank enhancer pairs as SREs
  
All the main programs are in SRE_Predictor.sh file. Please run the script and get the result from the folder called Output.

## Ouput folder have one folder for each gene. Each gene folder includes:
1. Enahcer_region.bed (enhancer.bed and promoter_enhancer.bed)
2. Spatial contacts matrix for enhancer pairs (Zscore.txt)
3. The co-occupancy of chromatin features for enhancer pairs (VC_SQRT_norm.txt)
4. The track file of spatial contacts for visulization in WashU Epigenome Browser (.bedpe and WashU.txt)
5. The predcited SRE result with sorted intersction score (.txt and .pdf)

# Dependencies
The codebase relies on the following dependancies
```
java version 1.8.0_131
Juicer Tools version 1.9.9
R version 3.6.1
Bedtools version 2.29.2
Python 2.7.15
Python 3.7.6
bigWigSummary

```

# Reference
Xueqiu Lin, Yanxia Liu, Shuai Liu, Xiang Zhu, Lingling Wu, Haifeng Wang, Muneaki Nakamura, 
Yaqiang Cao, Augustine Chemparathy, Yanyu Zhu, Dehua Zhao, Xiaoshu Xu, Jasprina N. Noordermeer, Wing Hung Wong, Keji Zhao, Lei S. Qi*. Enhancer Interaction Networks for Ultralong-Distance Genome Regulation. (Under Revision)


