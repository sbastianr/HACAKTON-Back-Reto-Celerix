BEGIN TRANSACTION;
DROP TABLE IF EXISTS "ASIGNACIONES";
CREATE TABLE "ASIGNACIONES" (
"ASI_ID"INTEGER NOT NULL UNIQUE,
"USU_ID_USUARIO"INTEGER NOT NULL,
"PRO_ID_PROCESO"INTEGER NOT NULL,
"ASI_FECHA_CREACION"DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
"ASI_FECHA_ACTUALIZACION"DATETIME DEFAULT NULL,
PRIMARY KEY("ASI_ID" AUTOINCREMENT),
CONSTRAINT "FK_PRO_ID_PROCESO" FOREIGN KEY("PRO_ID_PROCESO") REFERENCES "PROCESOS"("PRO_ID_PROCESO"),
CONSTRAINT "FK_USU_ID_USUARIO" FOREIGN KEY("USU_ID_USUARIO") REFERENCES "USUARIOS"("USU_ID_USUARIO")
);
DROP TABLE IF EXISTS "EMPRESAS";
CREATE TABLE "EMPRESAS" (
"EMP_ID"INTEGER NOT NULL UNIQUE,
"EMP_NIT_EMPRESA"INTEGER NOT NULL UNIQUE,
"EMP_NOMBRE_RAZON_SOCIAL"TEXT NOT NULL,
"USU_ID_USUARIO"TEXT NOT NULL,
"EMP_FECHA_CREACION"DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
"EMP_FECHA_ACTUALIZACION"DATETIME DEFAULT NULL,
PRIMARY KEY("EMP_ID" AUTOINCREMENT)
);
DROP TABLE IF EXISTS "ESTADOS";
CREATE TABLE "ESTADOS" (
"EST_ID"INTEGER NOT NULL UNIQUE,
"EST_ID_ACTUACION"INTEGER NOT NULL UNIQUE,
"EST_CONSTANCIA_ACTUACION"INTEGER NOT NULL UNIQUE,
"EST_ACTUACION"TEXT NOT NULL,
"EST_ANOTACION"TEXT NOT NULL,
"EST_FECHA_ACTUACION"DATETIME NOT NULL,
"EST_FECHA_REGISTRO"DATETIME NOT NULL,
"EST_TIENE_DOCUMENTOS"TEXT,
"EST_ID_DOCUMENTO"TEXT,
"EST_NOMBRE_DOCUMENTO"TEXT,
"EST_DESCRIPCION_DOCUMENTO"TEXT,
"PRO_ID_PROCESO"TEXT NOT NULL,
"EST_FECHA_CREACION"DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
"EST_FECHA_ACTUALIZACION"DATETIME DEFAULT NULL,
PRIMARY KEY("EST_ID" AUTOINCREMENT),
CONSTRAINT "FK_PRO_ID_PROCESO" FOREIGN KEY("PRO_ID_PROCESO") REFERENCES "PROCESOS"("PRO_ID_PROCESO")
);
DROP TABLE IF EXISTS "PROCESOS";
CREATE TABLE "PROCESOS" (
"PRO_ID"INTEGER NOT NULL UNIQUE,
"PRO_ID_PROCESO"INTEGER NOT NULL UNIQUE,
"PRO_LLAVE_PROCESO"TEXT NOT NULL,
"PRO_FECHA_PROCESO"DATETIME NOT NULL,
"PRO_FECHA_ULTIMA_ACTUACION"DATETIME NOT NULL,
"PRO_DESPACHO"TEXT NOT NULL,
"PRO_DEPARTAMENTO"TEXT NOT NULL,
"POR_ES_PRIVADO"TEXT NOT NULL,
"EMP_NIT_EMPRESA"INTEGER NOT NULL,
"PRO_URGENCIA"TEXT,
"PRO_FECHA_CREACION"DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
"PRO_FECHA_ACTUALIZACION"DATETIME DEFAULT NULL,
PRIMARY KEY("PRO_ID" AUTOINCREMENT),
CONSTRAINT "FK_EMP_NIT_EMPRESA" FOREIGN KEY("EMP_NIT_EMPRESA") REFERENCES "EMPRESAS"("EMP_NIT_EMPRESA")
);
DROP TABLE IF EXISTS "USUARIOS";
CREATE TABLE "USUARIOS" (
"USU_ID"INTEGER NOT NULL UNIQUE,
"USU_ID_USUARIO"INTEGER NOT NULL UNIQUE,
"USU_NOMBRE"TEXT NOT NULL,
"USU_CORREO"TEXT NOT NULL,
"USU_USUARIO"TEXT,
"USU_ESTADO"TEXT,
"USU_FECHA_CREACION"DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
"USU_FECHA_ACTUALIZACION"DATETIME DEFAULT NULL,
PRIMARY KEY("USU_ID" AUTOINCREMENT)
);
COMMIT;