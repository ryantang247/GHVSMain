import concurrent.futures
import json
import time
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
        tree = self.__repo.get_git_tree(pull_request.head.sha, recursive=True)
        base_tree = [str(entry.path) for entry in tree.tree]
        pull_request_data = {
            "number": pull_request.number,
            "created_at": str(pull_request.created_at),
            "author": str(pull_request.user.login),
            "title": pull_request.title,
            "head_commit_sha": list(self.__get_file_tree(head_commit)),
            "file_tree": base_tree
        }
        return pull_request_data

    def __process_pull_request(self, pr):
        pr_data = self.__generate_pull_request_data(pr)
        self.__all_pr_data.append(pr_data)

    def analyze_repo(self):
        start_time = time.time()
        print("Processing pull request...")
        pull_requests = list(self.__repo.get_pulls(state="merged", sort="created", direction="desc"))
        with tqdm(total=len(pull_requests), desc="Processing Pull Requests") as pbar:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                for _ in executor.map(self.__process_pull_request, reversed(pull_requests)):
                    pbar.update()

        print("Writing file...")
        with open(self.__output_file_path, "w", encoding="utf-8") as output_file:
            json.dump(self.__all_pr_data, output_file, indent=2)
        end_time = time.time()
        print(f"Output written to {self.__output_file_path}, take {end_time - start_time:.2f} seconds")


