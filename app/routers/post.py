import logging

from fastapi import APIRouter
from pydantic import BaseModel

from app.utils.bedrock import ask_claude

router = APIRouter()

logger = logging.getLogger(__name__)


class PromptRequest(BaseModel):
    prompt: str


@router.post("/generate_post")
async def generate_post(request: PromptRequest):
    prompt = request.prompt
    logger.info(f"Generating post with prompt: {prompt}")
    return ask_claude(request.prompt)
