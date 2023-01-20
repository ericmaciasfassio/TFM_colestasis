#!/bin/bash
# -*- ENCODING: UTF-8 -*-

FICHERO=$1 	#/home/eric/Escritorio/github/prueba_3
CSV=$2	#/home/eric/Escritorio/github/datos_lipidoma.csv
type=$3	#lipidoma			

#comprobar que se han introducido 3 argumentos
if [ "$#" != "3" ]; then
    echo "Debe introducir 3 argumentos"
    echo "Argumento 1 = Nombre de un directorio para crearlo y guardar los resultados"
    echo "Argumento 2 = Archivo CSV con los datos de los genes"
    echo "Argumento 3 = Tipo de datos (gen, miRNA, lipidoma)"
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
	mkdir -p $FICHERO
   	echo "El fichero $FICHERO se ha creado"
fi

#R script para analizar que tipo de genes son y cambiar los ensembl id por Gene Symbol
Rscript biomart.R $CSV $FICHERO $type

echo 'Script Biomart.sh finalizado '
