# mrprops-backend

Backend en **FastAPI** para la aplicación MrProps (gestión de propiedades, reservas y pagos).  

---

## 🔧 Requisitos
- Python 3.11+
- MySQL (o una instancia compatible)
- pip

---

## Instalación (local)
1. Crear y activar entorno virtual:
```bash
python -m venv .venv
# Windows (PowerShell)
.venv\Scripts\Activate.ps1
# Unix / Mac
source .venv/bin/activate
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Crear `.env` en la raíz con (ejemplo):
```
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=password
MYSQL_DB=mrprops
SECRET_KEY=una_clave_segura
ACCESS_TOKEN_EXPIRE_MINUTES=60
FORCE_SEED=0
```
> **No** subir `.env` al repositorio — añádelo a `.gitignore`.

---

## Ejecutar (desarrollo)
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
Docs automáticas: http://127.0.0.1:8000/docs

---

## 🗃️ Migraciones (Alembic)
- Aplicar migraciones:
```bash
alembic upgrade head
```
- Crear una nueva migración (autogenerada):
```bash
alembic revision --autogenerate -m "Descripción del cambio"
```
- Ver estado:
```bash
alembic current
```

---

## 🧪 Seed de datos
- Ejecutar el seed script:
  - Linux / Mac:
    ```bash
    FORCE_SEED=1 python seed.py
    ```
  - PowerShell:
    ```powershell
    $env:FORCE_SEED = '1'; python seed.py
    ```

---

## ✅ Verificaciones y utilidades
- Chequear columnas (útil tras migraciones):
```bash
python -m scripts.check_columns
```

---

## Tests
```bash
pytest -q
```

---

## 🔐 Seguridad
- Contraseñas hasheadas (passlib, pbkdf2_sha256 por defecto en dev).
- JWT para endpoints protegidos.
- Ajustá `SECRET_KEY` en `.env` para producción.

---

## 🐳 CI / Docker (opcional)
- Para CI/PRs: levantar MySQL como servicio en el pipeline y exportar `DATABASE_URL`.
- Ejemplo (GitHub Actions) en la documentación o si querés que lo agregue, puedo prepararlo.

---

## Contribuir
- Usar ramas: `feat/...`, `fix/...`, `chore/...`
- Abrir PRs y ejecutar tests localmente antes de pedir revisión

---

Si querés, puedo también crear el archivo `.github/workflows/ci.yml` de ejemplo o guiarte con los comandos para commitear estos cambios; decime cómo preferís continuar.