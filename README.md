# EcoRopa API (versión estable)

Implementación limpia y funcional, lista para levantar sin modificar nada.

## Requisitos

* Docker y Docker Compose ≥ v2  
*(o Python 3.11 + PostgreSQL si prefieres local)*

## Arranque rápido

```bash
git clone <repo> ecoropa_api
cd ecoropa_api
docker compose up --build
```

- API: http://localhost:8000  
- Swagger UI: http://localhost:8000/docs

## Cambios clave respecto al primer prototipo

* Retrocedemos a **Pydantic 1.10.15** — máxima compatibilidad.
* Eliminado el atributo `version:` en _docker‑compose.yml_ (ya no se necesita).
* Endpoint `/recycle-points/nearby` declara manualmente `response_model` con `RecyclePointOut` para evitar errores de validación.
