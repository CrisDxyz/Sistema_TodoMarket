CREATE DATABASE TODOMARKET_VIP;

USE TODOMARKET_VIP;

CREATE TABLE Producto (
	id_prod int not null auto_increment,
    nom varchar(100),
    cant int,
    cod_bar bigint,
    prec int,
    marca varchar(1000),
activo boolean,
primary key (id_prod)
);

CREATE TABLE Locall (
	id_loc int not null,
    nom varchar(100),
    direc varchar(100),
primary key (id_loc)
);

CREATE TABLE Stock_Local(
	id_prod int,
    id_loc int,
    cant int,
primary key (id_prod,id_loc)
);

CREATE TABLE Venta_diaria(
	cod_ven int not null,
    fecha date,
    hora time,
    mon_tot int,
    id_loc int,
primary key (cod_ven)
);

CREATE TABLE Producto_vendido (
	id_prod int,
    cant int,
    cod_ven int,
primary key (id_prod, cod_ven)
);

CREATE TABLE Bodega (
	id_bod int,
    direcb varchar(100),
primary key (id_bod)
);

CREATE TABLE Stock_bodega(
	id_prod int,
    id_bod int,
    cant int,
primary key (id_bod,id_prod)
);

ALTER TABLE stock_local
    ADD CONSTRAINT fk_prod_st FOREIGN KEY (id_prod)
	REFERENCES Producto(id_prod);

ALTER TABLE stock_local
    ADD CONSTRAINT fk_loc FOREIGN KEY (id_loc)
	REFERENCES locall(id_loc);
    
ALTER TABLE venta_diaria
    ADD CONSTRAINT fk_loc_ven FOREIGN KEY (id_loc)
	REFERENCES locall(id_loc);
    
ALTER TABLE producto_vendido
    ADD CONSTRAINT fk_ven FOREIGN KEY (cod_ven)
	REFERENCES venta_diaria(cod_ven);

ALTER TABLE producto_vendido
    ADD CONSTRAINT fk_prod_ven FOREIGN KEY (id_prod)
	REFERENCES producto(id_prod);
    
ALTER TABLE  stock_bodega
    ADD CONSTRAINT fk_bod FOREIGN KEY (id_bod)
	REFERENCES bodega(id_bod);
    
ALTER TABLE stock_bodega
    ADD CONSTRAINT fk_prod FOREIGN KEY (id_prod)
	REFERENCES producto(id_prod);

INSERT INTO locall VALUES (1,"Local 1","Manuel Montt");
INSERT INTO bodega VALUES (1,"Manuel Montt");

