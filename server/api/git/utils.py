import requests
from fastapi import HTTPException
from pathlib import Path
from .schemas import Repository
import git

# Updated API URL for fetching user repositories (not organizations)
GITHUB_API_URL = 'https://api.github.com/user/repos'


def fetch_repositories(access_token: str):
    """Fetch all repositories (public, private, and forked) from GitHub using username and access token."""
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Accept': 'application/vnd.github+json',
        "X-GitHub-Api-Version": "2022-11-28"

    }

    # Initialize the repositories list
    all_repositories = []

    # Add the 'type' filter to the URL to specify the type of repositories
    url = f"{GITHUB_API_URL}?visibility=all"
    print(f"Fetching from: {url}")

    while url:
        response = requests.get(url, headers=headers)

        # Debugging response status code and content
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Content: {response.text}")

        if response.status_code == 200:
            repos_data = response.json()
            print(f"Received {len(repos_data)} repositories.")

            # Convert the raw repo data to a list of Repository objects
            all_repositories.extend([Repository(**repo)
                                    for repo in repos_data])

            # Check if there is a next page in the response header
            if 'link' in response.headers and 'rel="next"' in response.headers['link']:
                # Get the URL for the next page of results
                url = response.headers['link'].split(';')[0][1:-1]
                print(f"Next page URL: {url}")
            else:
                break
        else:
            # Raise an HTTP exception with detailed error
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Error fetching repositories: {response.json()}"
            )

    return all_repositories


def clone_repo(repo_url, access_token):
    # Modify the URL to include the access token for authentication
    clone_url = repo_url.replace('https://', f'https://{access_token}@')

    # Define the base server directory where repositories will be cloned
    server_directory = Path(__file__).parent.parent.parent / 'cloned-repos'

    # Create the 'cloned-repos' directory if it doesn't exist
    server_directory.mkdir(parents=True, exist_ok=True)

    # Extract the repository name (assuming the repo URL is in GitHub format)
    repo_name = repo_url.split('/')[-1].replace('.git', '')

    # Define the destination path for the cloned repository
    repo_directory = server_directory / repo_name

    # Check if the directory already exists
    if repo_directory.exists():
        return f"Repository folder '{repo_name}' already exists. Skipping clone."

    # Clone the repository into its respective subdirectory
    try:
        git.Repo.clone_from(clone_url, repo_directory)
        return f"Repository cloned successfully to {repo_directory}"
    except git.exc.GitCommandError as e:
        return f"Error cloning repository: {e}"
