from flask import Flask, render_template, request, jsonify
from utils import init_chroma_client, query_chroma, construct_prompt, generate_response
from openai import OpenAI

app = Flask(__name__)

# Initialize ChromaDB and OpenAI
CHROMA_PATH = r"chroma_db"
COLLECTION_NAME = "networkperformance"

chroma_client = init_chroma_client(CHROMA_PATH)
collection = chroma_client.get_or_create_collection(name='networkperformance')
client = OpenAI()


@app.route("/")
def index():
    return render_template("index.html")  # Serve the front-end page


@app.route("/chat", methods=["POST"])
def chat():
    user_query = request.json.get("query")
    if not user_query:
        return jsonify({"error": "No query provided"}), 400

    try:
        # Query the Chroma database
        retrieved_data = query_chroma(collection, user_query)

        # Construct the system prompt
        system_prompt = construct_prompt(retrieved_data, user_query)

        # Generate a response using OpenAI
        bot_response = generate_response(client, system_prompt, user_query)
        return jsonify({"response": bot_response})

    except Exception as e:
        return jsonify({"error": f"Something went wrong: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True)
