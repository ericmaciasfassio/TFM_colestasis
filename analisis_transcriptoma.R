#descargar los paquetes si es necesario
#chooseCRANmirror()
#install.packages("BiocManager")
#BiocManager::install("DESeq2")
#BiocManager::install("EnhancedVolcano")
#BiocManager::install("ComplexHeatmap")
#install.packages("RColorBrewer")

library("DESeq2")
library("EnhancedVolcano")
library(ComplexHeatmap)
library(RColorBrewer)
library(circlize)

#función para realizar en el análisis de expresión diferencial
analisis_deseq2 <-function(file, path, type){
  file <- as.character(file)
  #cargamos el dataset
  count_matrix <- read.csv(file= file, 
                           sep=',', 
                           header = TRUE)
    
  Genes <- count_matrix$id
  count_matrix$id <- NULL
  #NA = 0
  haz.cero.na <- function(x){ifelse(is.na(x), 0, x)}
  count_matrix <- apply(count_matrix, MARGIN=2, FUN = haz.cero.na)
  count_matrix <- apply(count_matrix, MARGIN=2, FUN = round)
  
  row.names(count_matrix) <- Genes
  
  #Ajustamos el coldata de DESeq2
  coldata <- data.frame(
    sample = colnames(count_matrix),
    condition =  factor(c(rep('control',3), rep('colestasis',26))), #esto se deberá ajustar manualmente en función del dataset
    row.names = "sample" )
  
  #verificación 
  all(rownames(coldata) %in% colnames(count_matrix))
  all(rownames(coldata) == colnames(count_matrix))
  
  #creamos el objeto dds
  dds <- DESeqDataSetFromMatrix(countData = count_matrix, colData = coldata, 
                                design = ~ condition)
  #ajustamos los controles como condición de referencia
  dds$condition <- relevel(dds$condition, ref= "control")
  
  #filtro: quitamos filas con menos de 10 lecturas
  dds <- dds[rowSums(counts(dds)) >= 10,]
  dds <- DESeq(dds)
  
  #ajustamos el método de FDR
  res <- results(dds, pAdjustMethod= 'fdr')
  resdata <- merge(as.data.frame(res), as.data.frame(counts(dds, normalized= TRUE)), by='row.names', sort=FALSE)
  names(resdata)[1] <- 'id'
  
  #alpha = 0.05
  res05 <- results(dds, alpha=0.05)
  
  
  #los genes down-regulated
  resSig <- subset(resdata, padj <= 0.05)
  
  #up
  up <- subset(resSig, log2FoldChange >0)
  
  #down
  down <- subset(resSig, log2FoldChange < 0)
  

  #guardamos en csv
  save_result = paste(path, type, sep = '')
  write.csv(resdata, file= paste(save_result, '_resultado_completo_deseq2.csv', sep = "" ))
  write.csv(up, file= paste(save_result, '_up.csv', sep = "" ))
  write.csv(down, file= paste(save_result, '_down.csv', sep = ""))
  write.csv(resSig, file= paste(save_result, '_up_down.csv', sep = ""))
  vsd <-varianceStabilizingTransformation(dds, blind = FALSE)
  write.table(assay(vsd), file= paste(save_result, '_vst.csv', sep=''), row.names = TRUE, col.names = NA,sep=',')
  path_vst = paste(save_result, '_vst.csv', sep='')
  #volcano plot
  volcano_plot <- read.csv(file=paste(save_result, '_resultado_completo_deseq2.csv', sep = "" ) , 
                           sep=',', 
                           header = TRUE,
  )
  
  save_image = paste(path,'figuras', sep ='/')
  save_result_1 =paste(save_image,type, sep='/')
  png(paste(save_result_1,'_volcano_plot.png', sep = '') ,res = 300, width = 2000, height = 2500)
    p <- EnhancedVolcano(resdata,
                    lab = resdata$id,
                    x = 'log2FoldChange',
                    y = 'padj',
                    pCutoff = 0.05,
                    FCcutoff = 0,
                    legendLabels=c('Not sig.','Padj > 0.05','Padj > 0.05',
                                   'Padj <= 0.05'),
                    col=c('black', 'black', 'black', 'red3'),
                    pointSize = 1.5,
                    labSize = 4.5,
                    legendPosition = 'top',
                    legendLabSize = 16,
                    legendIconSize = 4.0,
                    max.overlaps= 14,
                    drawConnectors = TRUE,
                    widthConnectors = 0.4,
                    colConnectors = 'black')
    print(p)
  dev.off()

  
  #PCA
  png(paste(save_result_1,'_pca_plot.png', sep=''), res = 300, width = 2000, height = 2500)
  pcaData <- plotPCA(vsd,intgroup=c("condition"), returnData=TRUE)
  percentVar <- round(100 * attr(pcaData, "percentVar"))
  pca <- ggplot(pcaData, aes(PC1, PC2, color=condition)) +
    geom_point(size=3) +
    xlab(paste0("PC1: ",percentVar[1],"% variance")) +
    ylab(paste0("PC2: ",percentVar[2],"% variance")) + 
    ggtitle("Análisis de Componentes Principales") +
    theme(plot.title = element_text(hjust = 0.5))+
    coord_fixed()+
    geom_point(color='black')+
    scale_color_manual(values=c("coral3", "#56B4E9"))+
    geom_text_repel(aes(label=name),min.segment.length = 0, max.overlaps = Inf)
  print(pca)
  dev.off()
  
  
  #Heatmap
  sigs <- na.omit(res)
  sigs <- sigs[sigs$padj < 0.05,]
  write.csv(sigs, file= paste(save_result, '_heatmap.csv', sep = ""))
  sigs <- read.csv(file= paste(save_result, '_heatmap.csv', sep = ""))
  rownames(sigs) <- sigs[, 1]  ## set rownames
  df <- as.data.frame(sigs)
  df.top <- df[ (df$baseMean > 0) & (abs(df$log2FoldChange) > 0),]
  df.top <- df.top[order(df.top$log2FoldChange, decreasing = TRUE),]
  
  rlog_out <- varianceStabilizingTransformation(dds, blind=FALSE) #get normalized count data from dds object
  mat<-assay(rlog_out)[rownames(df.top), rownames(coldata)] #sig genes x samples
  colnames(mat) <- rownames(coldata)
  base_mean <- rowMeans(mat)
  mat.scaled <- t(apply(mat, 1, scale)) #center and scale each column (Z-score) then transpose
  
  colnames(mat.scaled)<-colnames(mat)
  num_keep <- 15
  #1 to num_keep len-num_keep to len
  rows_keep <- c(seq(1:num_keep), seq((nrow(mat.scaled)-num_keep + 1), nrow(mat.scaled)) )
  l2_val <- as.matrix(df.top[rows_keep,]$log2FoldChange) #getting log2 value for each gene we are keeping
  colnames(l2_val)<-"logFC"
  mean <- as.matrix(df.top[rows_keep,]$baseMean) #getting mean value for each gene we are keeping
  colnames(mean)<-"AveExpr"
  #maps values between b/w/r for min and max l2 values
  col_logFC <- colorRamp2(c(min(l2_val),0, max(l2_val)), c("blue", "white", "red")) 
  #maps between 0% quantile, and 75% quantile of mean values --- 0, 25, 50, 75, 100
  col_AveExpr <- colorRamp2(c(quantile(mean)[1], quantile(mean)[4]), c("white", "red"))
  png(paste(save_result_1,"_heatmap_v1.png", sep=''), res = 300, width = 5000, height = 5500)
  ha <- HeatmapAnnotation(summary = anno_summary(gp = gpar(fill = 2), 
                                                 height = unit(2, "cm")))
  h1 <- Heatmap(mat.scaled[rows_keep,], cluster_rows = F,
                column_labels = colnames(mat.scaled), name="Z-score",
                cluster_columns = T)
  h2 <- Heatmap(l2_val,
                cluster_rows = F, name="log2FC", top_annotation = ha, col = col_logFC, width = 2,
                cell_fun = function(j, i, x, y, w, h, col) { # add text to each grid
                  grid.text(round(l2_val[i, j],2), x, y)
                })
  h3 <- Heatmap(mean, row_labels = df.top$X[rows_keep],
                cluster_rows = F, name = "AveExpr", col=col_AveExpr, width = 2,
                cell_fun = function(j, i, x, y, w, h, col) { # add text to each grid
                  grid.text(round(mean[i, j],2), x, y)
                })
  h<-h1+h2+h3
  print(h)
  dev.off()
  cat(path_vst)
}

args <- commandArgs(trailingOnly = TRUE)

analisis <- analisis_deseq2(args[1], args[2], args[3])



