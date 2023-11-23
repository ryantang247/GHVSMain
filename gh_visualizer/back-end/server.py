import ast
import json

from flask import Flask, jsonify, request, session
import grabData
from flask_cors import CORS, cross_origin

app = Flask(__name__)

# Secret key for session
my_dict = {
    'my_owner': '',
    'my_repo_name': ''
}
cors = CORS(app, resources={r"/": {"origins": "*"}})

def extract_github_token(file_path):

    # this ast converts a file to a graph structure
    with open(file_path, 'r') as file:
        file_content = file.read()
        module = ast.parse(file_content, filename=file_path)
        for node in module.body:
            # module.exports.githubToken = '';, module.exports.githubToken is a type of target
            if isinstance(node, ast.Assign):
                dictionary_node = node.value

                for key_node, value_node in zip(dictionary_node.keys, dictionary_node.values):
                    if key_node.id == 'githubToken':
                        return value_node.value
    return None  # Return None if githubToken is not found


@app.route('/send_repo', methods=['POST'])
@cross_origin()
def process_data():
    print("Received POST!")
    username = request.form.get('username')
    repo = request.form.get('repo')
    my_dict['my_owner'] = username
    my_dict['my_repo_name'] = repo

    github_token = extract_github_token('../src/auth_config.js')

    # Use the values stored in the session
    my_owner = my_dict.get('my_owner')
    my_repo_name = my_dict.get('my_repo_name')

    # Create an instance of GitHubRepoAnalyzer
    analyzer = grabData.GitHubRepoAnalyzer(github_token, my_owner, my_repo_name)

    # Call the analyze_repo method to perform the analysis
    jsonfile = analyzer.analyze_repo()

    # Return the data as a JSON response
    return jsonfile


if __name__ == '__main__':
    app.run(host='127.0.0.2', port=8080)
