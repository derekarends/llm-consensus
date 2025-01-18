import logging
import sys

from fastapi import FastAPI
from .models import SearchCommand

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

logger = logging.getLogger(__name__)

app = FastAPI()


@app.get("/search")
async def search(cmd: SearchCommand):
    return cmd.execute()
