from fastapi import APIRouter, HTTPException
from .schemas import GitHubRequest, GitHubResponse, CloneRequest
from .utils import fetch_repositories, clone_repo

router = APIRouter()


@router.post("/repos/", response_model=GitHubResponse)
async def get_repositories(data: GitHubRequest):
    try:
        # Fetch repositories using the provided access token and username
        repos = fetch_repositories(data.access_token)
        return GitHubResponse(repositories=repos)
    except HTTPException as e:
        raise e


@router.post("/clone")
async def clone_repository(request: CloneRequest):
    try:
        result = clone_repo(
            request.repo_url,  request.access_token)
        return {"message": result}
    except HTTPException as e:
        raise e
