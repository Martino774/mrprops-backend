from decimal import Decimal
from datetime import date
from passlib.context import CryptContext
import os
from sqlalchemy import text

from database import SessionLocal

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
from models import User, Property, Booking, Payment, PropertyType, BookingStatus, PaymentStatus

def hash_pwd(pwd: str) -> str:
    return pwd_context.hash(pwd)

def run():
    db = SessionLocal()
    try:
        # evitar duplicados si ya hay datos
        if db.query(User).first():
            force = os.getenv("FORCE_SEED", "").lower() in ("1", "true", "yes")
            env = os.getenv("ENV", "development").lower()

            if not force:
                # Si estamos en producción (o no-development), pedir confirmación interactiva
                if env != "development":
                    try:
                        # comprobar que estamos en un terminal interactivo
                        import sys
                        if not sys.stdin.isatty():
                            print("Shell no interactivo y FORCE_SEED no está establecido. Aborting reseed.")
                            return
                    except Exception:
                        print("No se pudo verificar terminal interactivo. Aborting reseed.")
                        return

                    print("ATENCIÓN: Estás a punto de TRUNCAR tablas en la base de datos. Esto eliminará TODOS los datos existentes.")
                    print("Escribe 'YES' (mayúsculas) y pulsa Enter para confirmar, o cualquier otra cosa para cancelar:")
                    confirm = input().strip()
                    if confirm != "YES":
                        print("Confirmación no recibida. Aborting reseed.")
                        return
                    print("Confirmación recibida. Procediendo a truncar tablas...")
                else:
                    # En entorno de desarrollo, no forzar, pedir que usen FORCE_SEED para seguridad
                    print("La base ya contiene datos. Si quieres resemear, exporta FORCE_SEED=1 y reejecuta el script.")
                    return

            # Truncate tables to reseed
            db.execute(text("SET FOREIGN_KEY_CHECKS=0;"))
            db.execute(text("TRUNCATE TABLE payments;"))
            db.execute(text("TRUNCATE TABLE bookings;"))
            db.execute(text("TRUNCATE TABLE properties;"))
            db.execute(text("TRUNCATE TABLE users;"))
            db.execute(text("SET FOREIGN_KEY_CHECKS=1;"))
            db.commit()
            print("Reseed: tablas truncadas, continuando...")

        # Users
        users = [
            User(full_name="María López", email="maria.lopez@example.com", phone="+5491122334455", password_hash=hash_pwd("Passw0rd!")),
            User(full_name="Juan Pérez", email="juan.perez@example.com", phone="+549116667788", password_hash=hash_pwd("Secret123")),
        ]
        db.add_all(users)
        db.commit()
        db.refresh(users[0]); db.refresh(users[1])

        # Properties
        props = [
            Property(
                title="Departamento céntrico 2 ambientes",
                description="Luminoso, cerca del subte, ideal para pareja.",
                price=Decimal("85000.00"),
                location="CABA, Palermo",
                image_url="https://example.com/images/depto1.jpg",
                property_type=PropertyType.alquiler,
                bedrooms=1,
                bathrooms=1,
                area=45
            ),
            Property(
                title="Casa en las afueras",
                description="Pileta y jardín amplio.",
                price=Decimal("3500000.00"),
                location="Zona Norte",
                image_url="https://example.com/images/casa1.jpg",
                property_type=PropertyType.venta,
                bedrooms=3,
                bathrooms=2,
                area=200
            ),
            Property(
                title="Monoambiente moderno",
                description="Ideal para estudiante, amoblado.",
                price=Decimal("60000.00"),
                location="CABA, Congreso",
                image_url="https://example.com/images/mono1.jpg",
                property_type=PropertyType.alquiler,
                bedrooms=0,
                bathrooms=1,
                area=30
            ),
        ]
        db.add_all(props)
        db.commit()
        for p in props:
            db.refresh(p)

        # Bookings
        booking1 = Booking(
            user_id=users[0].id,
            property_id=props[0].id,
            start_date=date(2025, 12, 15),
            end_date=date(2025, 12, 20),
            total_amount=Decimal("425000.00"),
            status=BookingStatus.confirmed
        )
        booking2 = Booking(
            user_id=users[1].id,
            property_id=props[2].id,
            start_date=date(2025, 11, 1),
            end_date=date(2025, 11, 30),
            total_amount=Decimal("60000.00"),
            status=BookingStatus.pending
        )
        db.add_all([booking1, booking2])
        db.commit()
        db.refresh(booking1); db.refresh(booking2)

        # Payments
        payment1 = Payment(
            booking_id=booking1.id,
            amount=Decimal("425000.00"),
            payment_method="tarjeta",
            status=PaymentStatus.approved
        )
        payment2 = Payment(
            booking_id=booking2.id,
            amount=Decimal("60000.00"),
            payment_method="transferencia",
            status=PaymentStatus.pending
        )
        db.add_all([payment1, payment2])
        db.commit()

        print("Seed completado: usuarios, propiedades, bookings y payments creados.")
    finally:
        db.close()

if __name__ == "__main__":
    run()