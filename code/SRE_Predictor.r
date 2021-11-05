library(reshape)
library(glmnet)

args <- commandArgs(TRUE)

hm_tf_cooccurance = args[1]
hic_interaction = args[2]
output_file_name = args[3]

process_feature_data <- function(hichip_file, tf_hm_file, feature_names){
		hichip_m = read.table(hichip_file,header=T,row.names = 1)
		new_rowcol_names = c()
		for (n in rownames(hichip_m)){
				  new_rowcol_names = c(new_rowcol_names, strsplit(n, "000_")[[1]][2])
		}
		rownames(hichip_m) <- new_rowcol_names; colnames(hichip_m) <- new_rowcol_names
		hichip_m_melt = melt(as.matrix(hichip_m))
		rnames = colnames(hichip_m)
		tf_hm_mean_multiply = read.table(tf_hm_file, header=T, row.names = 1)
		selected_pnames = c()
		selected_index = c()
		for (i in seq(1,length(rnames))){
				  if (i< length(rnames)) {
						 for (j in seq(i+1, length(rnames))){
							selected_pnames = c(selected_pnames, paste(as.character(rnames[i]), as.character(rnames[j]), sep="."))
		      selected_index = c(selected_index,seq(1,nrow(hichip_m_melt))[hichip_m_melt$X2==rnames[i] & hichip_m_melt$X1==rnames[j]])
			      }}}
		feature_length = 47
		ep_length = length(selected_pnames)
		x = matrix(rep(0,feature_length*ep_length), nrow = ep_length, ncol = feature_length, byrow = T,
				              dimnames = list(c(selected_pnames),c(feature_names)))
		colnames(x)[6] <- "HCFC1-human"
		colnames(x)[38] <- "CTCF-human"
		for (feature in rownames(tf_hm_mean_multiply)){
				  x[,feature] <- c(unlist(tf_hm_mean_multiply[feature,selected_index]))
		}
		x[,"HiChIP"] = unlist(hichip_m_melt[selected_index,3])
		x_scale = apply(x,2,scale)
		rownames(x_scale) <- rownames(x)
		x_scale = ifelse(is.na(x_scale),0,x_scale)
		newlist <- list(x_scale,selected_pnames)
		return(newlist)
}


final_model = readRDS("Elastic_Net_alpha0.5_TrainedModel.rds")
feature_names = readRDS("FeaturesName.rds")
cutoff=0.3732945
gene_feature_list = process_feature_data( hic_interaction, hm_tf_cooccurance, feature_names)
predict_giscore =  predict(final_model, newx = gene_feature_list[[1]], s = "lambda.min")
names(predict_giscore) <- gene_feature_list[[2]]
predict_giscore_sorted = predict_giscore[order(predict_giscore)]
pdf(paste(c(output_file_name,"pdf"),collapse="."),8,8)
plot(seq(1,length(predict_giscore_sorted)), predict_giscore_sorted,
     pch=20,ylab="Predicted Interaction", xlab="Rank", xlim=c(-2,length(predict_giscore_sorted)+1),
     ylim=c(min(predict_giscore_sorted) - 0.2,max(predict_giscore_sorted))+0.2)
abline(h=cutoff,col="red")
text(seq(1,length(predict_giscore_sorted))-5, predict_giscore_sorted,
     names(predict_giscore_sorted),cex = 0.5)
dev.off()
write.table(predict_giscore_sorted[length(predict_giscore_sorted):1], file=paste(c(output_file_name,"txt"),collapse="."),row.names = T,quote = F,sep="\t")
