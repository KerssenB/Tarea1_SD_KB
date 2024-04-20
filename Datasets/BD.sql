CREATE DATABASE reclamos_sernac;

CREATE TABLE reclamos_2010 (
id integer,
comuna_consumidor varchar(250),
region_consumidor integer,
nombre_region_consumidor varchar(250),
nombre_mercado varchar(250),
nombre_categoria_mercado varchar(250),
tipo_prod varchar(250),
motivo_legal varchar(250),
categoria_ml varchar(250),
resultado varchar(250));

CREATE TABLE reclamos_2011 (
id integer,
comuna_consumidor varchar(250),
region_consumidor integer,
nombre_region_consumidor varchar(250),
nombre_mercado varchar(250),
nombre_categoria_mercado varchar(250),
tipo_prod varchar(250),
motivo_legal varchar(250),
categoria_ml varchar(250),
resultado varchar(250));

COPY reclamos_2010(id, comuna_consumidor, region_consumidor, nombre_region_consumidor, nombre_mercado, nombre_categoria_mercado, tipo_prod, motivo_legal, categoria_ml, resultado) FROM '/home/kerssen/Documentos/Sistemas_Distribuidos/Other_Tarea_1/Datasets/Reclamos_2010.csv' csv DELIMITER ';';
COPY reclamos_2011(id, comuna_consumidor, region_consumidor, nombre_region_consumidor, nombre_mercado, nombre_categoria_mercado, tipo_prod, motivo_legal, categoria_ml, resultado) FROM '/home/kerssen/Documentos/Sistemas_Distribuidos/Other_Tarea_1/Datasets/Reclamos_2011.csv' csv DELIMITER ';';
