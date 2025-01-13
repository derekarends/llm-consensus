import logging

from typing import List
from uuid import UUID, uuid4
from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse
from app import settings
from .gpt import execute as execute_gpt
from .phi import execute as execute_phi

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

app = FastAPI()


@app.get("/ping")
async def pong():
    print("llm")
    print(settings.llm)
    if settings.llm == "phi":
        execute_phi()
        return {"ping": "pong! from phi"}
    else:
        execute_gpt()
        return {"ping": "pong! from gpt"}


# @app.get("/songs", response_model=list[Song])
# async def get_songs(session: AsyncSession = Depends(get_session)):
#     result = await session.exec(select(Song))
#     songs = result.all()
#     return [Song(name=song.name, artist=song.artist, id=song.id) for song in songs]


# @app.post("/songs")
# async def add_song(song_req: SongCreate, session: AsyncSession = Depends(get_session)):
#     song = Song(name=song_req.name, artist=song_req.artist)
#     session.add(song)
#     await session.commit()
#     await session.refresh(song)
#     return song


# @app.get("/heros", response_model=List[Hero])
# async def get_heros(session: AsyncSession = Depends(get_session)):
#     cmd = GetHerosQuery()
#     heros = await cmd.execute(session=session)
#     return heros


# @app.get("/heros/{hero_id}", response_model=Hero)
# async def get_hero(hero_id: UUID, session: AsyncSession = Depends(get_session)):
#     cmd = GetHeroByIdQuery(id=hero_id)
#     hero = await cmd.execute(session=session)
#     return hero


# @app.post("/heros", response_model=Hero)
# async def add_hero(cmd: CreateHeroCommand, session: AsyncSession = Depends(get_session)):
#     hero = await cmd.execute(session=session)
#     return hero


# @app.post("/heros/kafka", response_model=bool)
# async def add_hero_kafka(cmd: CreateHeroCommand, session: AsyncSession = Depends(get_session)):
#     msg = ProducerMessage(message_id=uuid4(), name=cmd.name, timestamp=datetime.now().isoformat())
#     await kp.produce("heros", msg, key=str(msg.message_id))
#     return True
