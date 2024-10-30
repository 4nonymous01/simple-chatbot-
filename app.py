from flask import Flask, render_template, request, session
import random
import nltk
from nltk.tokenize import word_tokenize

# Download nltk data
nltk.download('punkt', quiet=True)

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management

# Keywords for each intent
keywords = {
    "greeting": ["hi", "hello", "hey"],
    "order_status": ["order", "status", "tracking"],
    "product_information": ["info", "details"],
    "troubleshooting": ["troubleshoot", "issue", "problem", "fix"],
    "returns": ["return", "back","give back"],
    "refunds": ["refund", "money", "payment back"],
    "payment_issues": ["payment", "issue", "card", "billing"],
    "connect": ["connect", "support", "help", "agent"]
}

# Sample responses with detailed product specifications
responses = {
    "greeting": [
        "Hello! How can I assist you today?",
        "Hi there! What can I help you with?",
        "Hey! Feel free to ask me anything.",
    ],
    "order_status": [
        "Your order is being processed and will be delivered shortly. Check your email for the tracking ID.",
        "Your order has shipped and is on its way! You can track the progress with the tracking ID sent to your email.",
    ],
    "product_information": [
        """<div>
            <h3>Specifications of the requested product:</h3>
            <ul>
                <li><strong>Model ID:</strong> 181 Pro</li>
                <li><strong>Color:</strong> Mocha Elegance</li>
                <li><strong>Headphone Type:</strong> True Wireless</li>
                <li><strong>Sweat Proof:</strong> Yes</li>
                <li><strong>Deep Bass:</strong> Yes</li>
                <li><strong>Microphone:</strong> Yes</li>
                <li><strong>Battery Life:</strong> 100 Hours</li>
                <li><strong>Compatible Devices:</strong> Laptop, Mobile, Tablet</li>
                <li><strong>Domestic Warranty:</strong> 1 Year</li>
                <li><strong>Warranty Summary:</strong> 1 Year Warranty</li>
                <li><strong>Service Type:</strong> For queries, reach out to <a href="abc1234@gmail.com">abc1234@gmail.com</a> or call 9898989898</li>
            </ul>
        </div>"""
    ],
    "troubleshooting": [
        "Try restarting the device.",
        "Ensure all cables are connected properly. If the issue persists, describe the problem in detail.",
    ],
    "returns": [
        "To initiate a return, please specify the reason:\n"
        "1. Damaged\n"
        "2. Incorrect product\n"
        "3. Different brand\n"
        "4. Poor quality\n",
        
    ],
    "refunds": [
        "Refunds are processed within 5-7 business days. You'll receive a notification once initiated.",
        "You can initiate the refund from the order section of the app"
    ],
    "payment_issues": [
        "If facing payment issues, verify card details and billing address. For persistent issues, contact your bank.",
    ],
    "connect": [
        "Connecting you to customer support. Reach us at support@example.com or 9898989898.",
    ],
    "thank_you": [
        "Thank you for providing the reason for your return. We're processing it now.",
    ],
    "default": [
        "I'm here to help! Try asking about order status, product information, or returns.",
    ]
}

# Function to generate chatbot response based on user input
def get_response(user_input):
    user_input = user_input.lower()
    tokens = word_tokenize(user_input)

    # Check for greeting intent
    if any(word in tokens for word in keywords["greeting"]):
        return random.choice(responses["greeting"])

    # Check for return intent first
    if "return" in tokens or "refund" in tokens:
        session['awaiting_return_reason'] = True
        return responses["returns"][0]

    # Check for order status intent
    if "order" in tokens and "status" in tokens:
        return random.choice(responses["order_status"])
    
    # Check for product information intent
    if "product" in tokens or "specification" in tokens:
        return random.choice(responses["product_information"])

    # Other intents
    if "troubleshoot" in tokens or "issue" in tokens:
        return random.choice(responses["troubleshooting"])
    elif session.get('awaiting_return_reason', False):
        return handle_return_reason(user_input)
    elif "payment" in tokens:
        return random.choice(responses["payment_issues"])
    elif "connect" in tokens or "help" in tokens:
        return random.choice(responses["connect"])

    return random.choice(responses["default"])

# Function to handle return reasons
def handle_return_reason(user_input):
    reasons = {
        "1": "Damaged product",
        "2": "Incorrect product",
        "3": "Different brand",
        "4": "Poor quality",
    
    }

    if user_input in reasons:
        session.pop('awaiting_return_reason', None)
        return random.choice(responses["thank_you"])
    else:
        return "Please select a valid option from 1 to 6 for your return reason."

# Flask routes
@app.route("/")
def index():
    return render_template("chat.html")

@app.route("/get")
def get_bot_response():
    user_input = request.args.get('msg')
    response = get_response(user_input)
    return response

if __name__ == "__main__":
    app.run(debug=True)
