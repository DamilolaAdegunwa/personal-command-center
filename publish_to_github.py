#!/usr/bin/env python3
"""
Automated GitHub Repository Creator and Pusher for Personal Command Center.
Extracts token from ~/.git-credentials or environment, creates the GitHub repository,
pushes the main branch, and cleans up remote URLs.
"""
import os
import sys
import subprocess
import re
from pathlib import Path
import urllib.request
import json

USERNAME = "DamilolaAdegunwa"
REPO_NAME = "personal-command-center"
REPO_DESC = "Personal Operating System for an Individual Living and Working in the AI Era: Transforming scattered notes, tasks, ideas, decisions, and research into continuous situational awareness and actionable intelligence."

def get_token():
    token = os.getenv("GITHUB_TOKEN")
    if token:
        return token
    cred_path = Path.home() / ".git-credentials"
    if cred_path.exists():
        text = cred_path.read_text(encoding="utf-8")
        for line in text.splitlines():
            if "github.com" in line and USERNAME in line:
                return line.split("@github.com")[0].split(":")[-1].strip()
        for line in text.splitlines():
            if "github.com" in line:
                return line.split("@github.com")[0].split(":")[-1].strip()
    return None

def main():
    token = get_token()
    if not token:
        print("ERROR: GitHub token could not be found in ~/.git-credentials or environment.")
        sys.exit(1)

    print(f"Creating repository '{REPO_NAME}' on GitHub under user '{USERNAME}'...")
    url = "https://api.github.com/user/repos"
    payload = json.dumps({
        "name": REPO_NAME,
        "description": REPO_DESC,
        "private": False,
        "has_issues": True,
        "has_wiki": True
    }).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "Python-Git-Publisher"
        }
    )

    import ssl
    try:
        import certifi
        ssl_ctx = ssl.create_default_context(cafile=certifi.where())
    except Exception:
        ssl_ctx = ssl._create_unverified_context()

    try:
        with urllib.request.urlopen(req, context=ssl_ctx) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            print(f"Successfully created remote repository: {data.get('html_url')}")
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        if e.code == 422 and "already exists" in body:
            print("Remote repository already exists on GitHub.")
        else:
            print(f"GitHub API returned HTTP {e.code}: {body}")

    repo_dir = Path(__file__).parent.resolve()

    # Configure remote
    auth_remote = f"https://{USERNAME}:{token}@github.com/{USERNAME}/{REPO_NAME}.git"
    clean_remote = f"https://github.com/{USERNAME}/{REPO_NAME}.git"

    subprocess.run(["git", "remote", "remove", "origin"], cwd=repo_dir, capture_output=True)
    subprocess.run(["git", "remote", "add", "origin", auth_remote], cwd=repo_dir, check=True)

    print("Pushing 'main' branch to GitHub...")
    push_res = subprocess.run(["git", "push", "-u", "origin", "main", "--force"], cwd=repo_dir, capture_output=True, text=True)
    if push_res.returncode == 0:
        print(f"SUCCESS: Pushed codebase to {clean_remote}")
    else:
        print(f"Push output: {push_res.stderr.strip()}")

    # Sanitize remote URL
    subprocess.run(["git", "remote", "set-url", "origin", clean_remote], cwd=repo_dir, check=True)
    print("Cleaned remote origin URL.")
    print(f"\nLive Repository: {clean_remote}")

if __name__ == "__main__":
    main()
