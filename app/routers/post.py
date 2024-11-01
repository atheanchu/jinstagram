from fastapi import APIRouter, HTTPException
import boto3
import os
import json
from pydantic import BaseModel
from utils.bedrock import ask_claude

router = APIRouter()


class PromptRequest(BaseModel):
    prompt: str


@router.post("/generate_post")
async def generate_post(request: PromptRequest):
    return ask_claude(request.prompt)
