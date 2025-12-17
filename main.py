from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
from routers import properties, bookings, payments, auth

# 🔹 Crear tablas
Base.metadata.create_all(bind=engine)

app = FastAPI(title="MrProps API", version="1.0.0")

# 🔹 Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ ENDPOINTS TEST
@app.get("/")
def read_root():
    return {"message": "Backend is running"}

@app.get("/health")
def health():
    return {"status": "ok"}

# 🔹 Incluir routers
app.include_router(properties.router, prefix="/api", tags=["Properties"])
app.include_router(bookings.router, prefix="/api", tags=["Bookings"])
app.include_router(payments.router, prefix="/api", tags=["Payments"])
app.include_router(auth.router, prefix="/api", tags=["Auth"])