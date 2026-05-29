# AERI | Servicio de Control de Calidad del Aire

Servicio de colección, depuración, almacenamiento, análisis y predicción de los datos de los sensores de Ciudadanos Científicos SIATA ubicados en todo el Valle de Aburrá (Medellín, Colombia).

Este proyecto consta de tres componentes principales:
1. **Consumer (Python)**: Ingiere datos en tiempo real de la API de SIATA cada 5 minutos y los almacena en MongoDB.
2. **Exposer (Flask/Waitress)**: API REST que sirve modelos predictivos (ARIMA, etc.) y consultas de datos históricos.
3. **Frontend (Node/Express)**: Dashboard interactivo premium con mapas oscuros en tiempo real, widgets glassmorphic y analítica de datos históricos.

---

## 🛠️ Requisitos del Sistema

* **Base de datos**: MongoDB (corriendo en el puerto estándar `27017`)
* **Backend**: Python 3.10+ (probado exitosamente en Python 3.13)
* **Frontend**: Node.js v20+ (probado exitosamente en Node v24)

---

## 🚀 Guía de Instalación y Despliegue Rápido

Sigue estos pasos para levantar la solución completa en tu máquina local:

### 1. Preparar la Base de Datos (MongoDB)
Asegúrate de tener MongoDB instalado y activo:
```bash
sudo systemctl start mongod
sudo systemctl enable mongod
```

### 2. Configurar el Backend (Python)
Se recomienda aislar las dependencias utilizando un entorno virtual:
```bash
# Crear el entorno virtual
python3 -m venv .venv

# Activar el entorno
source .venv/bin/activate

# Instalar dependencias requeridas (incluyendo requests, flask, waitress, paste, matplotlib, pymongo)
pip install -r requirements.txt
```

### 3. Configurar el Frontend (Node.js)
1. Ingresa al directorio del cliente:
   ```bash
   cd Forest
   ```
2. Instala las dependencias seguras sin vulnerabilidades:
   ```bash
   npm install
   ```
3. Configura las variables de entorno en el archivo `.env` creado por defecto:
   * `PORT`: Puerto de la interfaz web (def: `3000`).
   * `BACKEND_URL`: Ruta de la API Python exposer (def: `http://localhost:5000`).

---

## 🏁 Instrucciones de Ejecución

Para iniciar el sistema completo, abre **tres terminales independientes** y ejecuta:

### Terminal 1: Ingestor de Datos (Consumer)
Ingesta la información en tiempo real desde SIATA hacia MongoDB.
```bash
source .venv/bin/activate
python3 start_consumer.py
```

### Terminal 2: API & Servidor de Predicción (Exposer)
Levanta la API REST en el puerto `5000` con calidad de producción (Waitress + Paste loggers).
```bash
source .venv/bin/activate
python3 start_exposer.py
```

### Terminal 3: Cliente Web Dashboard (Node.js)
Levanta la interfaz web interactiva en el puerto `3000`.
```bash
cd Forest
npm run dev
```

*Una vez iniciados los tres componentes, accede desde tu navegador a:* **`http://localhost:3000`**

---

## 📐 Evaluación de Arquitectura Senior: ¿Por qué la carpeta `Forest` es un "Smell"?

Como acertadamente notaste, estructurar el frontend dentro de una carpeta llamada `Forest` en la raíz de un servicio de Python es un patrón clásico de proyectos académicos que genera **acoplamiento innecesario**.

Un análisis de arquitectura senior revela lo siguiente:

### 1. El rol redundante del servidor Express (`Forest`)
Actualmente, el servidor Node.js/Express actúa meramente como un **proxy intermediario** que recibe peticiones del navegador y las redirige hacia la API de SIATA o hacia el backend en Python.
Con la modernización realizada:
* El cliente web ahora consume directamente la API externa de SIATA mediante `fetch()` asíncrono nativo en el navegador.
* Al resolver los problemas de CORS y configurar hostnames dinámicos, el cliente web también puede consumir directamente la API de Python en el puerto `5000`.

### 2. Propuesta de Arquitectura Optimizada
Para simplificar el despliegue al máximo para tu profesor o futuros desarrolladores, proponemos **dos caminos de desacoplamiento**:

#### Opción A: Servir el Frontend directamente desde Flask (Monolito Liviano)
Dado que el frontend es ahora una aplicación web puramente estática (HTML5, CSS3 y JS nativo, sin dependencias complejas), **no requiere un servidor Node.js en absoluto**.
* Se pueden mover los archivos de `Forest/src/public/*` a la carpeta `main/services/exposer/static/` de tu app de Flask.
* Se puede mover `index.html` a `main/services/exposer/templates/`.
* Con esto, **eliminas el 100% de la infraestructura de NodeJS** de la ecuación. El proyecto pasa a requerir solo **Python + MongoDB**, y tu profesor solo tendría que levantar un único servidor web en el puerto `5000` que sirva tanto la API como el visor del mapa.

#### Opción B: Desacoplamiento SPA + Servidor API (Arquitectura Moderna)
Separar el frontend en un repositorio independiente o carpeta `/frontend` y compilarlo como un cliente estático puro (SPA usando herramientas modernas como Vite).
* El frontend se despliega gratuitamente en CDNs globales de alto rendimiento (GitHub Pages, Vercel, Netlify).
* El backend de Python se despliega en un VPS o plataforma Cloud independiente.
* Ambos se comunican mediante HTTP REST de forma segura y veloz, facilitando el mantenimiento y permitiendo el escalado independiente de cada servicio.
