# Estudio del perfil transcripcional y metabólico de la disfunción hepática en la colestasis infantil.
En este repositorio se recoge el código empleado durante la realización del TFM.

El objetivo de este estudio es analizar los cambios metabólicos y transcripcionales que subyacen a la colestasis infantil desde un abordaje poliómico. Para ello, se ha escrito código en R, Python y Bash que permiten analizar los datos procedentes del lipidoma y del transcriptoma de las muestras, empleando los principales paquetes de R y las principales librerías de Python.

## Tabla de Contenidos
* [Información General](#Información-General)
* [Scripts](#Scripts)
* [Setup](#Setup)
* [Ejemplo de ejecución del código](#Ejemplo-de-ejecución-del-código)
* [Contacto](#Contacto)

## Información General
El código desarrollado en este TFM está pensando para ser ejectutado directamente desde la terminal (no interactivo) añadiendo los argumentos necesarios en cada script. Se han desarrollado 4 scripts princiaples en bash que agrupan a una serie de scripts de R y Python para facilitar la ejecución. 
Estos scripts nos permiten realizar los siguientes análisis: 
  - Clasificar genes. 
  - Realizar análisis de expresión diferencial. 
  - Realizar correlaciones no paramétricas de Spearman. 
  - Realizar análisis de abundancia. 
  - Construir figuras: PCAs, dendrogramas, volcanos plot y heatmaps. 
  
## Scripts
Los scripts se ejecutan desde la terminal indicando 3 argumentos: 
1. Directorio en el que se desea guardar los resultados: Se creará un directorio (comprobando previamente que no existe) en el que se guardarán las figuras y los archivos .csv de salida de los scripts. 
2. Archivo .csv: Se especificará la ruta del archivo .csv con los datos que se desean analizar. 
3. String con el tipo de datos a analizar: Esta string se añadirá al nombre de los .csv de salida para facilitar su identificación. Por ejemplo: miRNA. 

Scripts principales: 
1. Biomart.sh: Este script permite clasificar los genes en función de la categoría a la que pertenecen (codificantes de proteínas, de lncRNA...). Además, permite cambiar el ENSEMBL id por el Gene Symbol. Dentro de este script encontramos el script: 
  - Biomart.R

2. Analisis_transcriptoma.sh: Este script permite realizar el análisis de expresión diferencial y construir las figuras del PCA, dendrograma, volcano plot y heatmap. Dentro de este script encontramos los scripts:
  - analisis_transcriptoma.R
  - hierarchical_clustering.py 
  
3. Analisis_lipidoma.sh: Este script permite realizar el análisis de abundancia del lipidoma y construir las figuras del PCA, dendrograma, volcano plot y heatmap. Dentro de este script encontramos los scripts: 
  - analisis_lipidoma.py 
  - heatmap_lipidoma.py 
  - lipidoma_final.R 
  - hierarchical_clustering.py 
  
4. Correlaciones.sh: Este script permite calcular los coeficientes de correlación no paramétricos de Spearman entre los genes y miRNAs (todas las posibles combinaciones). En este script se debe indicar como segundo argumento la ruta del archivo .csv de los genes y en el tercer argumento se debe indicar la ruta del archivo .csv de los miRNAs. Dentro de este script encontramos el script: 
  - correlaciones.py  

Tras ejecutar los scripts obtendremos los archivos .csv de salida con los resultados del análisis seleccionado en el directorio indicado. Las figuras se guardarán en el directorio figuras, dentro del directorio indicado.
## Setup
Primero se debe clonar el repositorio:
```console
git clone https://github.com/ericmaciasfassio/TFM_colestasis.git

```
También se deberán instalar los paquetes de R y las librerías de Python siguientes:
```R
install.packages("BiocManager")
BiocManager::install("biomaRt")
BiocManager::install("ComplexHeatmap")
BiocManager::install("DESeq2")
BiocManager::install("EnhancedVolcano")
install.packages("RColorBrewer")
```
```console
pip install pandas
pip install numpy
pip install scipy
pip install matplotlib
```

## Ejemplo de ejecución del código
Para poder ejecutar los scripts debemos darles permiso.

```console
chmod u+x *.sh
```
1. Script Biomart.sh:

```console
./Biomart.sh ./Resultado_biomart ./csv_ejemplos/biomart.csv genes
```
Al finalizar la ejecución obtenemos un mensaje por pantalla y en el directorio Resultado_biomart se guardará el csv de salida.

```
Script Biomart.sh finalizado
```
2. Script analisis_transcriptoma.sh:

```console
./analisis_transcriptoma.sh ./resultados_transcriptoma ./csv_ejemplos/genes.csv genes
```
Al finalizar la ejecución obtenemos un mensaje por pantalla y en el directorio resultados_transcriptoma se guardarán los csv de salida y las figuras.

```
Script analisis_transcriptoma.sh finalizado 
```

3. Script correlaciones.sh:

```console
./correlaciones.sh ./resultado_correlaciones ./csv_ejemplos/genes_correlacion.csv ./csv_ejemplos/mirnas_correlacion.csv 
```
Al finalizar la ejecución obtenemos un mensaje por pantalla y en el directorio resultado_correlaciones se guardarán los csv de salida.

```
Script correlaciones.sh finalizado 
```
4. Script lipidoma.sh:

```console
./lipidoma.sh ./resultado_lipidoma_2 ./csv_ejemplos/datos_lipidoma.csv lipidoma
```
Al finalizar la ejecución obtenemos un mensaje por pantalla y en el directorio ./resultado_correlaciones se guardarán los csv de salida y las figuras.

```
Script lipidoma.sh finalizado 
```
## Contacto
Creado por [@ericmacias](https://www.linkedin.com/in/eric-mac%C3%ADas-fassio-594850215) - feel free to contact me!

 


