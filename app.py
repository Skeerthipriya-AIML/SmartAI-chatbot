"""
==================================================================
🧠 Smart AI Chatbot using Flask & Google Gemini
------------------------------------------------------------------
Author  : S.Keerthi Priya 
GitHub  : https://github.com/Skeerthipriya-AIML
Project : A free AI chatbot powered by Python Flask and Gemini API
License : MIT License

Feel free to use, modify, and share with credit.
==================================================================
"""

import logging
from flask import Flask,render_template, request, jsonify
from gemini_setup import get_gemini_response

# Setup logging for the web app to capture errors and info
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler()]
)

app = Flask(__name__)

@app.route('/')
def index():
    logging.info("Rendering main page.")
    try:
        return render_template("index.html")
    except Exception as e:
        logging.error(f"Error rendering index.html file: {e}")
        return "Error rendering page.", 500

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        logging.info(f"Received chat message: {user_message}")
        response = get_gemini_response(user_message)
    
        return jsonify({'response': response})
    except Exception as e:
        logging.error(f"Error in chat(): {e}")
        return jsonify({'response': "An error occurred while processing your message."})


#------------- RUN the Flask app -------------
if __name__ == '__main__':
    app.run(ssl_context=("cert.pem", "key.pem"))
    try:
        logging.info("Starting Flask app...")
        app.run(debug=True)
    except Exception as e:
        logging.error(f"Error starting Flask app: {e}")

