"""Entry point for `server` command — runs uvicorn."""

import uvicorn


def main():
    uvicorn.run(
        "db_migration_env.server.app:app",
        host="0.0.0.0",
        port=8000,
        workers=1,
    )


if __name__ == "__main__":
    main()
