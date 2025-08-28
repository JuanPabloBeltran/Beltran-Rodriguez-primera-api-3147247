from database import engine, Base
from models import UserDB  # Aquí se importan los modelos

print("📌 Creando tablas en la base de datos...")
Base.metadata.create_all(bind=engine)
print("✅ Tablas creadas correctamente")
