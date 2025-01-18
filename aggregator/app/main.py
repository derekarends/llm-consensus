import logging
import sys

from fastapi import FastAPI
from .llm_caller import invoke
from .models import SearchCommand

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

logger = logging.getLogger(__name__)

app = FastAPI()


@app.post("/search")
async def search(cmd: SearchCommand):
    logger.info(f"Received search request: {cmd}")
    return await cmd.execute()
