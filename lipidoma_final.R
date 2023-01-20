#rm(list = ls())
library("DESeq2")
library("EnhancedVolcano")
library("pheatmap")

#función para realizar las figuras del lipidoma
#debemos cargar un los datos en un objeto de DESeq2 similarmente al análisis de expresión diferencial
figuras_lipidoma <-function(file, path, type, result){
#cargamos el dataset
count_matrix <- read.csv(file=file, 
                         sep=',', 
                         header = TRUE)

id<- count_matrix$id
count_matrix$id <- NULL
#Na = 0
haz.cero.na <- function(x){ifelse(is.na(x), 0, x)}
count_matrix <- apply(count_matrix, MARGIN=2, FUN = haz.cero.na)
count_matrix <- apply(count_matrix, MARGIN=2, FUN = round)

row.names(count_matrix) <- id

#Creamos el objeto coldata de DESeq2
coldata <- data.frame(
  sample = colnames(count_matrix),
  condition =  factor(c(rep('control',7), rep('colestasis',27))),  #esto se deberá ajustar manualmente en función del dataset
  row.names = "sample" )

#compramos que coincide
all(rownames(coldata) %in% colnames(count_matrix))
all(rownames(coldata) == colnames(count_matrix))

#inicializamos el objeto dds
dds <- DESeqDataSetFromMatrix(countData = count_matrix, colData = coldata, 
                              design = ~ condition)
dds$condition <- relevel(dds$condition, ref= "control")
vsd <-varianceStabilizingTransformation(dds, blind = FALSE)
save_result = paste(path, type, sep = '/')
write.table(assay(vsd), file= paste(save_result, '_vst.csv', sep=''), row.names = TRUE, col.names = NA,sep=',')
#PCA
save_image = paste(path,'figuras', sep ='/')
save_result_1 =paste(save_image,type, sep='/')
png(paste(save_result_1,'_PCA_plot.png', sep = '') ,res = 300, width = 2000, height = 2500)

pcaData <- plotPCA(vsd,ntop = 45,intgroup=c("condition"), returnData=TRUE)
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

#volcano plot
volcano <- read.csv(file=result, 
                    sep=',', 
                    header = TRUE)
png(paste(save_result_1,'_volcano_plot.png', sep = '') ,res = 300, width = 2000, height = 2500)
p <- EnhancedVolcano(volcano,
                lab = volcano$id,
                x = 'Log2FC',
                y = 't_student',
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
                max.overlaps= 7,
                drawConnectors = TRUE,
                widthConnectors = 0.4,
                colConnectors = 'black',
                
)

print(p)
dev.off()

a <- paste(save_result, '_vst.csv', sep='')
cat(a)
}

args <- commandArgs(trailingOnly = TRUE)

analisis <- figuras_lipidoma(args[1], args[2], args[3], args[4])
