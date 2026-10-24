from flask import Flask, jsonify, request
import logging
import sqlite3

# Base de datos SQLite
DB_NAME = "biblioteca.db"

def obtener_conexion():
    """Crea y retorna una conexión a la base de datos."""
    conexion = sqlite3.connect(DB_NAME)
    conexion.row_factory = sqlite3.Row
    return conexion

def inicializar_db():
    """Crea las tablas necesarias si no existen."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS libros (
        libro_id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        autor TEXT NOT NULL,
        leido INTEGER DEFAULT 0
        )
    ''')

    conexion.commit()
    conexion.close()
    logging.info("Base de datos iniciada correctamente")

# Configuración básica de logs
logging.basicConfig(
    level=logging.INFO, # Nivel mínimo de logs a registrar (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s [%(levelname)s] %(message)s', # Formato: Fecha/Hora [NIVEL] Mensaje
    handlers=[
        logging.FileHandler("app.log"), # Guarda los logs en un archivo físico
        logging.StreamHandler()         # Imprime los logs también en la consola/terminal
    ]
)

# Inicializamos la aplicación
app = Flask(__name__)
logging.info("La aplicación se ha iniciado correctamente.")

# Definimos una ruta accesible vía HTTP GET
@app.route('/', methods=['GET'])
def inicio():
    return jsonify({"mensaje": "¡Servidor en línea!"})


@app.route('/libros', methods=['POST'])
def crear_libro():
    
    datos = request.get_json()
    
    titulo = datos.get('titulo')
    autor = datos.get('autor')
    leido = datos.get('leido', 0)

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute('''
        INSERT INTO libros (titulo, autor, leido)
        VALUES (?, ?, ?)
    ''', (titulo, autor, leido))

    conexion.commit()
    nuevo_id = cursor.lastrowid
    conexion.close()

    logging.info(f"Item creado exitosamente con ID: {nuevo_id}")

    logging.info("Se ha creado el libro de forma correcta")
    return jsonify({
        "libro_id": nuevo_id,
        "titulo": titulo,
        "autor": autor,
        "leido": leido
    }), 201

@app.route('/libros', methods=['GET'])
def obtener_libros():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute('SELECT * FROM libros')
    filas = cursor.fetchall()
    conexion.close()

    libros = [dict(fila) for fila in filas]
    logging.info(f"Se consultaron {len(libros)} libros.")
    return jsonify(libros), 200

@app.route('/libros/<int:libro_id>', methods=['GET'])
def obtener_libro(libro_id):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute('SELECT * FROM libros WHERE libro_id = ?', (libro_id,))
    fila = cursor.fetchone()
    conexion.close()

    if fila is None:
        logging.warning(f"Libro con ID {libro_id} no encontrado.")
        return jsonify({"error": "Recurso no encontrado"}), 404
    return jsonify(dict(fila)), 200

    # Punto de entrada para ejecutar el servidor
if __name__ == '__main__':
    # host='0.0.0.0' permite que sea accesible desde otros dispositivos en tu red (como tu Ubuntu Server)
    inicializar_db()
    app.run(host='0.0.0.0', port=5000, debug=True)