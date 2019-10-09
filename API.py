from flask import Flask
from flask import request
from flask import jsonify

from Service import Service

app = Flask(__name__)
service = Service()


@app.route("/find_resource", methods=["POST"])
def find_repositories():
    if not request.is_json:
        return jsonify({"message": "Request is not json"}), 400
    parameters = request.get_json()
    repo_urls = service.scrape_results_urls(parameters)
    if isinstance(repo_urls, IOError):
        return jsonify({"message": str(repo_urls)}), 408
    if repo_urls is None:
        return jsonify({"message": "Bad request"}), 400
    return prepare_response(repo_urls)


def prepare_response(repo_urls):
    urls_list = []
    for repo_url in repo_urls:
        urls_list.append({"url": repo_url})
    return jsonify(urls_list)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)