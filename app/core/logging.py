import logging


def get_logger(name: str) -> logging.Logger:
    """Return a logger."""
    logging.basicConfig(
        level=logging.ERROR,
        format="%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s",
        handlers=[
            logging.FileHandler("app.log", encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )
    return logging.getLogger(name)
