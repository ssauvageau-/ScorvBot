import logging
from logging import handlers
import os
import sys

from dotenv import load_dotenv

load_dotenv()
ENV = os.getenv(key="ENV", default="dev")
LOG_FOLDER = os.getenv(key="LOG_FOLDER", default="logs")


def setup_logging() -> None:
    discord_logger = logging.getLogger("discord")  # Logger for API events
    discord_http_logger = logging.getLogger("discord.http")  # Logger for http events
    bot_logger = logging.getLogger("bot")  # Logger for bot things

    # DEBUG is ultra-spammy for these two loggers
    discord_logger.setLevel("INFO")
    discord_http_logger.setLevel("INFO")

    if ENV == "dev":
        bot_logger.setLevel("DEBUG")
        handler = logging.StreamHandler(sys.stdout)
    elif ENV == "prod":
        bot_logger.setLevel("INFO")
        handler = logging.handlers.RotatingFileHandler(
            filename=f"{LOG_FOLDER}/scorv.log",
            encoding="utf-8",
            maxBytes=32 * 1024 * 1024,  # 32 MiB
            backupCount=5,  # Rotate through 5 files
        )
    else:
        raise EnvironmentError(f"Unrecognized environment '{ENV}' for logging")

    dt_fmt = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter(
        "[{asctime}] [{levelname:<8}] {name}: {message}", dt_fmt, style="{"
    )
    handler.setFormatter(formatter)

    discord_logger.addHandler(handler)
    discord_http_logger.addHandler(handler)
    bot_logger.addHandler(handler)
