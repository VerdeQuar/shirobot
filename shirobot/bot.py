import os
import sys
import discord
from discord.ext import commands
import logging
import logging.handlers


def run():
    logger = logging.getLogger("discord")
    logger.setLevel(logging.DEBUG)
    logging.getLogger("discord.http").setLevel(logging.INFO)

    dt_fmt = "%d.%m.%Y %H:%M:%S"
    formatter = logging.Formatter(
        "[{asctime}] [{levelname:^8}] {name}: {message}", dt_fmt, style="{"
    )
    file_handler = logging.handlers.RotatingFileHandler(
        filename="discord.log",
        encoding="utf-8",
        maxBytes=32 * 1024 * 1024,  # 32 MiB
        backupCount=5,  # Rotate through 5 files
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    std_handler = logging.StreamHandler(sys.stdout)
    std_handler.setFormatter(formatter)
    logger.addHandler(std_handler)

    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(command_prefix="!", intents=intents)

    cogs = ["basic", "eval"]
    for cog in cogs:
        bot.load_extensions(f"shirobot.cogs.{cog}")

    bot.run(os.environ.get("DISCORD_TOKEN"))
