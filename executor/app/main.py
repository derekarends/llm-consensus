import logging
import sys

from fastapi import FastAPI

from .agent import invoke_agent
from .models import ExecuteCommand

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
     handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


app = FastAPI()

@app.get("/execute")
async def execute(req: ExecuteCommand):
    return invoke_agent(req.chat_id, req.question)
