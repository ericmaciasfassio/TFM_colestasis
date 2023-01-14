#genes <- read.csv('/home/eric/Escritorio/TFM/DEG/resultado_25_04_deseq2.csv')
#genes <- read.csv('/home/eric/Escritorio/TFM/DEG/genes_datos_correlacion_final.csv')
require(biomaRt)

biomart <- function(file, path, type){
genes <- read.csv(file, header = TRUE)
mart <- useMart("ENSEMBL_MART_ENSEMBL")
mart <- useDataset("hsapiens_gene_ensembl", mart)
annotLookup <- getBM(
  mart = mart,
  attributes = c(
    "hgnc_symbol",
    "ensembl_gene_id",
    "gene_biotype"),
  filter = "ensembl_gene_id",
  values = genes$Gene,
  uniqueRows=TRUE)

annotLookup
path = paste(path, type, sep='/')
write.csv(annotLookup, file = paste(path, "_biomart.csv", sep=''))} 

args <- commandArgs(trailingOnly = TRUE)

a <- biomart(args[1], args[2], args[3])
#'/home/eric/Escritorio/TFM/DEG/resultado_25_04_deseq2.csv','/home/eric/Escritorio/TFM/DEG'