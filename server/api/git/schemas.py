from pydantic import BaseModel
from typing import List, Optional


class Repository(BaseModel):
    id: int
    name: str
    full_name: str
    html_url: str
    description: Optional[str]
    language: Optional[str]
    created_at: str
    updated_at: str


class GitHubRequest(BaseModel):
    access_token: str


class GitHubResponse(BaseModel):
    repositories: List[Repository]


class CloneRequest(BaseModel):
    repo_url: str
    access_token: str
