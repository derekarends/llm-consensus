import logging
import sys

from fastapi import FastAPI
from .agent import invoke_agent
from .models import SearchCommand

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

logger = logging.getLogger(__name__)

app = FastAPI()


@app.post("/search")
async def search(req: SearchCommand):
    logger.info(f"Received search request: {req}")
    return await invoke_agent(req.chat_id, req.question)
