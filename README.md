# osu-pp

Proyecto para recolectar, guardar y visualizar progreso de osu! usando FastAPI, SQLite y una interfaz web estática.

## Qué hace

- Consulta datos de usuario desde la API de osu! con ossapi.
- Guarda snapshots de estadísticas por modo en SQLite.
- Guarda historial de daily challenges.
- Expone una API para leer usuario, estadísticas y daily challenges.
- Sirve una interfaz web estática en la ruta raíz.

## Tecnologías

- Python 3.12+
- FastAPI
- SQLite
- ossapi
- uvicorn
- Tailwind CSS por CDN en el frontend

## Estructura

```text
osu-pp/
├── app/
│   ├── database.py
│   ├── main.py
│   ├── recolector.py
│   ├── routers/
│   │   ├── stats.py
│   │   └── user.py
│   └── services/
│       └── ossapi.py
├── public/
│   ├── index.html
│   ├── script.js
│   └── style.css
├── docker-compose.yml
├── Dockerfile
└── pyproject.toml
```

## Variables de entorno

Crea un archivo `.env` en la raíz del proyecto con estas variables:

```env
CLIENT_ID=tu_client_id
CLIENT_SECRET=tu_client_secret
USERNAME=tu_usuario_de_osu
MODOS=osu,mania
```

`MODOS` debe ir separado por comas. Si quieres otros modos, agrega más valores, por ejemplo `osu,mania,taiko,fruits`.

## Instalación local

Instala las dependencias con `uv`:

```bash
uv sync
```

## Ejecutar la API

Levanta el servidor desde la raíz del proyecto:

```bash
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8051
```

La aplicación quedará disponible en:

```text
http://127.0.0.1:8051
```

## Ejecutar el recolector

Para guardar snapshots en SQLite, ejecuta el recolector como módulo:

```bash
uv run python -m app.recolector
```

## Ejecutar con Docker

Construye y levanta el contenedor:

```bash
docker compose up --build
```

La app se expone en el puerto `8051`.

## Endpoints

### GET /

Sirve el frontend estático desde `public/index.html`.

### GET /user

Devuelve el usuario configurado en `USERNAME`.

### GET /daily_challenges

Devuelve el historial de daily challenges guardado en SQLite.

### GET /stats

Devuelve todos los snapshots guardados.

### GET /stats/{modo}

Devuelve el historial filtrado por modo.

Ejemplo:

```text
/stats/osu
```

## Base de datos

La base de datos SQLite se crea automáticamente en:

```text
app/data/osu_historial.db
```

Las tablas principales son:

- `snapshots`
- `daily_challenges`

## Frontend

El frontend está en `public/` y usa Tailwind CSS por CDN junto con estilos propios para una apariencia tipo magical girl.

## Notas

- El servidor FastAPI monta `public/` como contenido estático en la raíz.
- Si cambias la estructura del proyecto, revisa la ruta de `StaticFiles` en `app/main.py`.
- El recolector y los routers usan imports del paquete `app`, así que conviene ejecutar siempre desde la raíz del proyecto.
