# 🧠 Networking RAG Chatbot

A Retrieval-Augmented Generation (RAG) chatbot designed to help users troubleshoot network-related issues using OpenAI's API. Built with Flask and a simple web interface.

## ✨ Features

-  Context-aware responses via RAG pipeline
-  Natural language generation using OpenAI API
-  Prompt engineering for better answer accuracy
-  Conversational memory for multi-turn chats
-  Lightweight, Flask-based frontend


## 📁 Project Structure

```
RAG_TEST/
├── app.py           # Flask web app
├── fill_db.py       # Vector DB setup script
├── utils.py         # Utility functions
├── requirements.txt # Python dependencies
├── templates/       # HTML frontend
├── static/          # CSS & JS
├── chroma_db/       # Vector DB (local, optional)
├── data/            # Input docs (e.g., PDFs)
```


## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/miayaaa/networking-rag-chatbot.git
cd networking-rag-chatbot
```

### 2. Set Up Virtual Environment

```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API Key

Create a `.env` file in the root directory and add your OpenAI API key:

```env
OPENAI_API_KEY=your_openai_key_here
```

### 5. Run the App

```bash
python app.py
```

Then open your browser at [http://localhost:5000](http://localhost:5000)


## 📌 Notes

- If you're using PDF/text files as sources, place them in the `data/` folder.
- The vector store (`chroma_db/`) is generated after running `fill_db.py`.

