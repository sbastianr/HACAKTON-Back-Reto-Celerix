import sqlite3

# Ruta donde se creará el archivo de base de datos
db_path = "../resources/database.sqlite"

# Cargar el contenido del script SQL
with open("../resources/schema.sql", "r", encoding="utf-8") as f:
    sql_script = f.read()

# Crear y conectar la base de datos
conn = sqlite3.connect(db_path)

# Ejecutar el script
with conn:
    conn.executescript(sql_script)

print("Base de datos creada exitosamente.")
