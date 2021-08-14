from typing import List
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from discord import Client, Intents
from discord_slash import SlashCommand, SlashContext, SlashCommandOptionType

from .conf import authtoken, dbpath
from .models import Base, Movie

engine = create_engine(f'sqlite:///{dbpath}', echo=True)
Base.metadata.create_all(engine, checkfirst=True)

bot = Client(intents=Intents.default())
slash = SlashCommand(bot, sync_commands=True)


@slash.slash(name="add", guild_ids=[868603751567609936], options=[
    {
        "type": SlashCommandOptionType.STRING,
        "name": "title",
        "description": "Movie Title",
        "required": True
    }
])
async def add(ctx: SlashContext, title: str):
    movie = Movie(title=title)
    with Session(engine) as session:
        session.add(movie)
        session.commit()
    await ctx.send(f"Added {title}")


@slash.slash(name="remove", guild_ids=[868603751567609936], options=[
    {
        "type": SlashCommandOptionType.STRING,
        "name": "title",
        "description": "Movie Title",
        "required": True
    }
])
async def remove(ctx: SlashContext, title: str):
    with Session(engine) as session:
        count = session.query(Movie).filter(Movie.title == title).delete()
        session.commit()
    if count:
        reply = f"Removed {title}"
    else:
        reply = f"{title} not found"
    await ctx.send(reply)


@slash.slash(name="list", guild_ids=[868603751567609936])
async def list(ctx: SlashContext):
    with Session(engine) as session:
        movies: List[Movie] = session.query(Movie).all()
    if movies:
        movies_text = "\n".join(m.title for m in movies)
    else:
        movies_text = "No movies found"

    await ctx.send(movies_text)

bot.run(authtoken)
