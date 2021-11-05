gene_list=$1
Enhancer_region=$2
HiChIP_hic=$3
HiChIP_res=$4
HM_TF_BigWig_Folder=$5
Output_Path=$6

mkdir $Output_Path
####1. Retrieve enhancer regions for target genes
echo "Retrieving enhancer regions..."
python2 generate_regions.py $gene_list $Enhancer_region $Output_Path
echo "Done!!"

####2. Calculate normalized spatial contacts between enhancer pairs
#####2.1 process .hic and retrieve VC_SQRT_norm.txt for each chromosome 
mkdir $Output_Path/"HiChIP_VC_SQRT"
echo "Retrieving VC_SQRT normalized interaction..."
for chrom_num in 1 2 3 4 5 6 7 X 8 9 10 11 12 13 14 15 16 17 18 20 Y 19 22 21
do
	java -jar juicer_tools.jar dump observed VC_SQRT $HiChIP_hic $chrom_num $chrom_num BP $HiChIP_res $Output_Path/"HiChIP_VC_SQRT"/"GM12878_chr"$chrom_num"_matrix_"$HiChIP_res"bp_Cohesin_VC_SQRT_norm.txt"
	java -jar juicer_tools.jar dump expected VC_SQRT $HiChIP_hic $chrom_num BP $HiChIP_res $Output_Path/"HiChIP_VC_SQRT"/"GM12878_chr"$chrom_num"_expected_"$HiChIP_res"bp_Cohesin_VC_SQRT_norm.txt"
	###need python3
	python3 retrieve_hic_pets.py  $HiChIP_hic $chrom_num $HiChIP_res VC_SQRT $Output_Path/"HiChIP_VC_SQRT"/"GM12878_chr"$chrom_num"_"$HiChIP_res"bp_Cohesin_VC_SQRT.bedpe" 
done	
echo "Done!!"

###Process for each gene
cat $gene_list | while read gene 
do
#####2.2  Calculate normalized spatial contacts between enhancer pairs
echo "Calculating normalized spatial contacts between enhancer pairs for " $gene "..."
chrom=`head -n 1 $Output_Path/$gene"/Enhancers.bed"|cut -f 1`
python2 retrive_HiCinteraction_simple.py $Output_Path/$gene"/Enhancers.bed"  $Output_Path/"HiChIP_VC_SQRT"/"GM12878_"$chrom"_matrix_"$HiChIP_res"bp_Cohesin_VC_SQRT_norm.txt"  $Output_Path/"HiChIP_VC_SQRT"/"GM12878_"$chrom"_expected_"$HiChIP_res"bp_Cohesin_VC_SQRT_norm.txt"  $Output_Path/$gene/"Enhancers_HiChIP_matrix_"$HiChIP_res"bp_VC_SQRT_norm.txt" 10000
echo "Done!!"

#####2.3 Generate tracks of spatial contacts for visulization in WashU Epigenome Browser
echo "Generating WashU Epigenome Browser tracks of spatial contacts for " $gene "..."
python2 bed2bedpe.py $Output_Path/$gene"/Promoter_enhancers.bed" $Output_Path/$gene"/Promoter_enhancers.bedpe" 4 -10
bedtools pairtopair -type both -a $Output_Path/$gene"/Promoter_enhancers.bedpe" -b $Output_Path/"HiChIP_VC_SQRT"/"GM12878_"$chrom"_"$HiChIP_res"bp_Cohesin_VC_SQRT.bedpe" -is > $Output_Path/$gene"/Promoter_enhancers_HiChIP_"$HiChIP_res"bp_VC_SQRT.bedpe"
awk '{OFS="\t"; print $1,$2,$3, $4":"$5"-"$6","$14, NR,"."}' $Output_Path/$gene"/Promoter_enhancers_HiChIP_"$HiChIP_res"bp_VC_SQRT.bedpe" > $Output_Path/$gene"/Promoter_enhancers_HiChIP_"$HiChIP_res"bp_VC_SQRT_WashU.txt"
echo "Done!!"

####3. Calculate co-occupancy of chromatin features
echo "Calculating co-occupancy of chromatin features for " $gene "..."
python2 retrieve_TF_HMs_DoubleElement_matrix.py $Output_Path/$gene"/Enhancers.bed" $Output_Path/$gene"/Enhancers_selected_TFs_HMs_Zscore" $HM_TF_BigWig_Folder 0 1
echo "Done!!"

###4. Apply trained model to compute interaction score to rank enhancer pairs as SREs
echo "Predicting SRE for " $gene "..."
Rscript SRE_Predictor.r $Output_Path/$gene"/Enhancers_selected_TFs_HMs_Zscore.txt" $Output_Path/$gene"/Enhancers_HiChIP_matrix_"$HiChIP_res"bp_VC_SQRT_norm.txt" $Output_Path/$gene/"SRE_Rank"
echo "Done!!"
done


