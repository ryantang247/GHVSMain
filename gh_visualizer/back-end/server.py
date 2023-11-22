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


@app.route('/send_repo', methods=['POST'])
@cross_origin()
def process_data():
    print("Received POST!")
    username = request.form.get('username')
    repo = request.form.get('repo')
    my_dict['my_owner'] = username
    my_dict['my_repo_name'] = repo

    data = {'message': 'Done importing all information! Redirecting...'}
    my_access_token = "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"

    # Use the values stored in the session
    my_owner = my_dict.get('my_owner')
    my_repo_name = my_dict.get('my_repo_name')

    # Create an instance of GitHubRepoAnalyzer
    analyzer = grabData.GitHubRepoAnalyzer(my_access_token, my_owner, my_repo_name)

    # Call the analyze_repo method to perform the analysis
    analyzer.analyze_repo()

    # Return the data as a JSON response
    return jsonify(data)


if __name__ == '__main__':
    app.run()
