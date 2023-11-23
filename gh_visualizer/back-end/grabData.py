import concurrent.futures
import json
import time

import requests
from github import Github
from tqdm import tqdm


class GitHubRepoAnalyzer:
    def __init__(self, access_token, owner, repo_name):
        self.__access_token = access_token
        self.__owner = owner
        self.__repo_name = repo_name
        self.__repo = Github(access_token).get_repo(f"{owner}/{repo_name}")
        self.__output_file_path = "../src/output.json"
        self.__all_pr_data = []

    def __get_file_tree(self, commit_sha):
        files = self.__repo.get_commit(commit_sha).files
        file_tree = set()
        for file in files:
            file_tree.add(file.filename)
        return file_tree

    def __generate_pull_request_data(self, pull_request):
        head_commit = pull_request.head.sha
        labels_data = [{"color": label.color, "name": label.name} for label in pull_request.labels]

        # Get files changed in the pull request
        files_changed_url = f'https://api.github.com/repos/{self.__owner}/{self.__repo_name}/pulls/{pull_request.number}/files'
        headers = {'User-Agent': 'request', 'Authorization': 'Bearer {}'.format(self.__access_token)}
        response = requests.get(files_changed_url, headers=headers)
        filetree = []
        changed_files = []
        if response.status_code == 200:
            files_changed = response.json()
            modified_files_data = []
            changed_files = [file['filename'] for file in files_changed]

            for file_changed in files_changed:
                filename = file_changed['filename']
                additions = file_changed['additions']
                deletions = file_changed['deletions']
                changes = file_changed['changes']

                # Additional request to get commit information for the file
                commit_info_url = f'https://api.github.com/repos/{self.__owner}/{self.__repo_name}/commits/{head_commit}'
                commit_info_response = requests.get(commit_info_url, headers=headers)
                if commit_info_response.status_code == 200:
                    commit_info = commit_info_response.json()
                    num_commits = len(commit_info['files'])
                else:
                    print(f"Failed to get commit information. Status code: {commit_info_response.status_code}")
                    num_commits = 0

                file_data = {
                    "filename": filename,
                    "additions": additions,
                    "deletions": deletions,
                    "changes": changes,
                    "num_commits": num_commits
                }

                modified_files_data.append(file_data)

        else:
            print(f"Failed to get files changed. Status code: {response.status_code}")
            modified_files_data = []

        pull_request_data = {
            "number": pull_request.number,
            "created_at": str(pull_request.created_at),
            "author": str(pull_request.user.login),
            "title": pull_request.title,
            "head_commit_sha": list(self.__get_file_tree(head_commit)),
            "modified_files_data": modified_files_data,
            "file_tree": changed_files,
            "labels_data": labels_data,
        }

        return pull_request_data

    def __process_pull_request(self, pr):
        pr_data = self.__generate_pull_request_data(pr)
        self.__all_pr_data.append(pr_data)

    def analyze_repo(self):
        start_time = time.time()
        print("Processing pull request...")

        # modified this such that the status is not merged
        pull_requests = list(self.__repo.get_pulls(sort="created", direction="desc"))
        with tqdm(total=len(pull_requests), desc="Processing Pull Requests") as pbar:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                for _ in executor.map(self.__process_pull_request, reversed(pull_requests)):
                    pbar.update()

        print("Writing file...")
        with open(self.__output_file_path, "w", encoding="utf-8") as output_file:
            json.dump(self.__all_pr_data, output_file, indent=2)
        end_time = time.time()
        print(f"Output written to {self.__output_file_path}, take {end_time - start_time:.2f} seconds")
        return json.dumps(self.__all_pr_data, indent=2)
