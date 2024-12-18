from flask import Flask, request, jsonify
# 3. security: env,bearer
# from dotenv import load_dotenv
# 4. Retry mechanism
from retry_utils import make_post_request, make_get_request
from limiter_utils import init_limiter, limiter
from scheduler_utils import setup_scheduler 

# load_dotenv()
app = Flask(__name__)

# 1. Rate limiter(to handle throttling)
init_limiter(app)

# 2. Scheduler
scheduler = setup_scheduler(app)

@app.route("/")
def home():
    return jsonify({"message": "Welcome to the Salesforce Connector API"}), 200

# Login Post Request
@app.route('/api/salesforce/token', methods=['POST'])
@limiter.limit("5 per minute")  # Limit this route to 5 requests per minute per IP
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

# 5. Error and Exception Handling 
    try:
        # Use the retryable POST request
        response = make_post_request(url, data=form_data, headers=headers)

        if response.status_code != 200:
            return jsonify({
                "error": response.json(),
                "message": "Failed to get the token from Salesforce"
            }), response.status_code

        return jsonify(response.json()), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500

#GET Request
@app.route('/api/salesforce/query', methods=['GET'])
@limiter.limit("5 per minute")  # Limit this route to 5 requests per minute per IP
def salesforce_query():
    query = request.args.get('q')
    if not query:
        return jsonify({"error": "Missing required parameter: q"}), 400

    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Missing or invalid Authorization header"}), 401

    bearer_token = auth_header.split(" ")[1]

    url = f"https://smartshore5-dev-ed.develop.my.salesforce.com/services/data/v56.0/query/"

    headers = {
        "Authorization": f"Bearer {bearer_token}"
    }

    try:
        # Use the retryable GET request
        response = make_get_request(url, headers=headers, params={"q": query})

        if response.status_code != 200:
            return jsonify({
                "error": response.json(),
                "message": "Failed to fetch data from Salesforce"
            }), response.status_code

        return jsonify(response.json()), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=6000, debug=True)


