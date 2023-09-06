import uvicorn


def main() -> None:
    """Entrypoint of the application."""
    uvicorn.run("api.application:get_app")


if __name__ == "__main__":
    main()
