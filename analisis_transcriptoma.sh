#!/bin/bash
# -*- ENCODING: UTF-8 -*-

FICHERO=$1	#/home/eric/Escritorio/TFM/Resultado_deseq
CSV=$2	#/home/eric/Escritorio/TFM/bases_de_datos/miRNA_database_filtered.csv
type=$3	#gene		

#comprobar que se han introducido 3 argumentos
if [ "$#" != "3" ]; then
    echo "Debe introducir 3 argumentos"
    echo "Argumento 1 = Nombre de un directorio para crearlo y guardar los resultados"
    echo "Argumento 2 = Archivo CSV con los datos de los genes"
    echo "Argumento 3 = Tipo de datos"
    exit
else
    echo "Se han introducido 3 argumentos"
fi

#Comprobamos que el fichero no existe y crear el fichero
if [ -d ./$FICHERO ]
then
	echo "El fichero $FICHERO existe"
	exit
else
	mkdir $FICHERO
	mkdir -p $FICHERO/figuras
   	echo "El fichero $FICHERO se ha creado"
fi



#Rscript analisis_miRNA_TFM.R
R=$(Rscript analisis_transcriptoma.R $CSV $FICHERO /$type)	#csv con los datos normalizados 

python3 hierarchical_clustering.py $R $FICHERO/figuras /$type

echo 'analisis_transcriptoma.sh finalizado '

