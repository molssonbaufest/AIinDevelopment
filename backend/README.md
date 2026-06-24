# FastAPI JWT Backend

Aplicacion Web API construida con FastAPI que implementa autenticacion JWT con un usuario de demostracion.

## Caracteristicas

- Endpoint de autenticacion con credenciales `admin` / `admin123`.
- Access token JWT con expiracion de 300 segundos.
- Endpoint para refrescar el token.
- Frontend de bienvenida en `GET /` con cards de certificaciones Microsoft 2026.
- Hashing de contrasenas con `passlib[bcrypt]`.
- Dependencia `bcrypt` fijada a `>=3.2,<4.0` por compatibilidad con `passlib 1.7.x`.
- Gestion de dependencias con Poetry y `package-mode = false`.
- Despliegue mediante Docker y Docker Compose.

## Estructura

```text
backend/
├── app/
│   ├── auth.py
│   ├── main.py
│   └── schemas.py
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
└── README.md
```

## Requisitos

- Python 3.11 o superior
- Poetry
- Docker y Docker Compose (opcional, para despliegue containerizado)

## Instalacion local

```bash
cd backend
poetry install
poetry run uvicorn app.main:app --reload
```

La API quedara disponible en `http://127.0.0.1:8000`.

## Endpoints

### `GET /health`

Verifica que la API este operativa.

### `GET /`

Muestra la pagina de bienvenida del frontend con cards de certificaciones de Microsoft Learn.

### `POST /auth/token`

Genera un access token de 300 segundos y un refresh token.

Request:

```json
{
  "username": "admin",
  "password": "admin123"
}
```

Response:

```json
{
  "access_token": "<jwt>",
  "refresh_token": "<jwt>",
  "token_type": "bearer",
  "expires_in": 300
}
```

### `POST /auth/refresh`

Recibe un refresh token valido y devuelve un nuevo access token junto con un nuevo refresh token.

Request:

```json
{
  "refresh_token": "<jwt>"
}
```

## Ejemplos con `curl`

Obtener tokens:

```bash
curl -X POST http://127.0.0.1:8000/auth/token \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

Refrescar tokens:

```bash
curl -X POST http://127.0.0.1:8000/auth/refresh \
  -H "Content-Type: application/json" \
  -d '{"refresh_token":"<jwt>"}'
```

## Uso con Docker

Construir y levantar el servicio:

```bash
cd backend
docker compose up --build
```

La aplicacion quedara expuesta en `http://localhost:8000`.

## Notas

- La clave secreta JWT en `app/auth.py` es solo para demostracion y debe externalizarse en un entorno real.
- En este entorno no estaba instalado Poetry, por lo que no se genero `poetry.lock`. El proyecto queda listo para generarlo ejecutando `poetry lock` o `poetry install`.
