from __future__ import with_statement
import sys
import os
from alembic import context
from sqlalchemy import create_engine
from sqlalchemy import pool
from sqlalchemy.ext.declarative import declarative_base

# Import your model here
from App.models import Base  # Adjust the path to where your Base is defined

# This is the metadata object from your models
target_metadata = Base.metadata

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = context.config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = create_engine(
        context.config.get_main_option("sqlalchemy.url"), 
        poolclass=pool.NullPool
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()

# Main logic to determine which mode to run
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
