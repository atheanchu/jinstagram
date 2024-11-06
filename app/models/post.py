from typing import Optional

from pydantic import BaseModel, ConfigDict


class UserPostIn(BaseModel):
    body: str
    user_id: str


class UserPost(UserPostIn):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: str
    # image field can be either Optional or str
    image: Optional[str] = None
