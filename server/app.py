"""Root-level server entry point for OpenEnv compatibility."""

import uvicorn

from db_migration_env.server.app import app

__all__ = ["app"]


def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
