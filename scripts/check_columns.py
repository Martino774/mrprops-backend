from database import engine
from sqlalchemy import inspect

insp = inspect(engine)
for t in ['users', 'properties', 'bookings', 'payments']:
    try:
        cols = [c['name'] for c in insp.get_columns(t)]
        print(f"{t}: {cols}")
    except Exception as e:
        print(f"Error inspecting {t}: {e}")
