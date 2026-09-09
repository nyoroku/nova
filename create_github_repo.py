import requests
import sys

def create_github_repo(username, token, repo_name):
    url = f"https://api.github.com/user/repos"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "name": repo_name,
        "private": True,
        "description": "Rafiki Boat Rides Platform"
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 201:
        print(f"Successfully created repository: {repo_name}")
        return True
    elif response.status_code == 422:
        print(f"Repository {repo_name} already exists.")
        return True
    else:
        print(f"Failed to create repository. Status code: {response.status_code}")
        print(response.json())
        return False

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python create_repo.py <username> <token> <repo_name>")
        sys.exit(1)
    
    create_github_repo(sys.argv[1], sys.argv[2], sys.argv[3])
