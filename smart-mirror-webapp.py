import logging
from flask import Flask, render_template, request, jsonify
from gemini_setup import get_gemini_response

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

app = Flask(__name__)

@app.route('/')
def index():
    logging.info("Rendering main page.")
    try:
        return render_template("index.html")
    except Exception as e:
        logging.exception("Error rendering index page.")
        return "Error loading page", 500

@app.route('/ask', methods=['POST'])
def chat():
    try:
        data = request.get_json(force=True)  # force=True handles bad headers
        user_message = data.get('message', '').strip()

        if not user_message:
            logging.warning("Empty user message received.")
            return jsonify({'response': "Please enter a question."}), 200

        logging.info(f"Received user message: {user_message}")
        response = get_gemini_response(user_message)

        return jsonify({'response': response})
    except Exception as e:
        logging.exception("Error in chat endpoint.")
        return jsonify({"error": "An error occurred while processing your message."}), 500

# Optional: alias route so /chat also works
@app.route('/chat', methods=['POST'])
def chat_alias():
    return chat()

if __name__ == '__main__':
    try:
        logging.info("Starting Flask app...")
        app.run(debug=True)
    except Exception as e:
        logging.exception("Error starting Flask app.")
