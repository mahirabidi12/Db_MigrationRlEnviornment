"""Root-level client — re-exports from the package for OpenEnv compatibility."""

from db_migration_env.client import MigrationClient

__all__ = ["MigrationClient"]
