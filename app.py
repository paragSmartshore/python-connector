from flask import Flask, request, jsonify
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
# TODO: add this project to a repo
app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"message": "Welcome to the Salesforce Connector API"}), 200


@app.route('/api/salesforce/token', methods=['POST'])
def get_salesforce_token():
    url = "https://smartshore5-dev-ed.develop.my.salesforce.com/services/oauth2/token"

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    form_data = request.form.to_dict()

    required_fields = ["client_id", "client_secret", "grant_type"]
    missing_fields = [field for field in required_fields if field not in form_data]
    if missing_fields:
        return jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400

    try:
        response = requests.post(url, data=form_data, headers=headers)

        if response.status_code != 200:
            return jsonify({
                "error": response.json(),
                "message": "Failed to get the token from Salesforce"
            }), response.status_code

        return jsonify(response.json()), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=6000, debug=True)


