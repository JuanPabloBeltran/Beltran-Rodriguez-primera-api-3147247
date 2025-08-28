from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# Configuración de Alembic
config = context.config

# Configuración de logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ✅ Importar Base y modelos
from database import Base  # Base declarativa
from models import *        # Todos tus modelos (User, etc.)

# Metadata de los modelos para autogenerate
target_metadata = Base.metadata

# Ejecutar migraciones en modo offline
def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

# Ejecutar migraciones en modo online
def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()

# Detectar modo offline/online
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
