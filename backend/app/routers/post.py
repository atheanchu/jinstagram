import logging
import os

from fastapi import APIRouter
from pydantic import BaseModel

from app.configs.database import database, post_table
from app.models.post import UserPost, UserPostIn
from app.utils.bedrock import ask_claude, generate_image_for_post

router = APIRouter()

logger = logging.getLogger(__name__)

IMAGE_PATH = "./app/assets/images/"


class GeneratePostIn(BaseModel):
    prompt: str
    user_id: str


@router.post("/post", response_model=UserPost, status_code=201)
async def create_post(
    post: UserPostIn,
    current_user: int = 0,
):
    logger.info("Creating post")
    data = {**post.model_dump()}
    query = post_table.insert().values(data)
    logger.debug(query)
    last_record_id = await database.execute(query)
    return {**data, "id": last_record_id}


@router.post("/generate_post")
async def generate_post(request: GeneratePostIn):
    prompt = request.prompt
    current_user = request.user_id

    logger.info(f"Generating post with prompt: {prompt}")

    body = ask_claude(request.prompt)
    generated_text = body["generated_content"]

    # Generate an image for this post
    # output_filename should be a randomly generated string using uuid
    output_filename = f"{IMAGE_PATH}{current_user}_{os.urandom(16).hex()}.png"
    image_path = generate_image_for_post(
        generated_text, output_filename=output_filename
    )

    data = {"body": generated_text, "user_id": current_user, "image": image_path}

    query = post_table.insert().values(data)
    logger.debug(f"Generating post with prompt: {prompt}")
    last_record_id = await database.execute(query)

    return {**data, "id": last_record_id, "image": image_path}


@router.get("/post", response_model=list[UserPost])
async def get_posts(current_user: int = 0):
    logger.info("Getting posts")
    query = post_table.select()
    logger.debug(query)
    return await database.fetch_all(query)


# Get a post by id
@router.get("/post/{post_id}", response_model=UserPost)
async def get_post(post_id: int, current_user: str = 0):
    logger.info(f"Getting post with id: {post_id}")
    query = post_table.select().where(post_table.c.id == post_id)
    logger.debug(query)
    return await database.fetch_one(query)


# Delete all posts
@router.delete("/post", status_code=201)
async def delete_posts(current_user: str = 0):
    logger.info("Deleting posts")
    query = post_table.delete()
    logger.debug(query)
    await database.execute(query)

    # Delete all images in the IMAGE_PATH
    for filename in os.listdir(IMAGE_PATH):
        if filename.endswith(".png"):
            os.remove(os.path.join(IMAGE_PATH, filename))

    return {"message": "All posts deleted"}


# Delete post by id
@router.delete("/post/{post_id}", status_code=201)
async def delete_post(post_id: int, current_user: int = 0):
    logger.info(f"Deleting post with id: {post_id}")
    query = post_table.delete().where(post_table.c.id == post_id)
    logger.debug(query)
    await database.execute(query)
    return {"message": f"Post with id: {post_id} deleted"}


# Update post by id
@router.put("/post/{post_id}", status_code=201)
async def update_post(post_id: int, post: UserPostIn, current_user: int = 0):
    logger.info(f"Updating post with id: {post_id}")
    data = {**post.model_dump()}
    query = post_table.update().where(post_table.c.id == post_id).values(data)
    logger.debug(query)
    await database.execute(query)
    return {**data, "id": post_id}
