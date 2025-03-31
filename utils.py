import chromadb
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def init_chroma_client(path):
    chroma_client = chromadb.PersistentClient(path=path)
    return chroma_client


def query_chroma(collection, user_query):
    results = collection.query(
        query_texts=[user_query],
        n_results=10,
    )
    return results


def construct_prompt(retrieved_data, user_query):
    return f"""
    You are a Networking Performance Expert. Your role is to provide accurate and helpful answers based strictly on the retrieved information from the knowledge base. The knowledge base contains detailed information on network performance, customer feedback, performance metrics, issues, recommendations, and actionable insights.

Guidelines for answering:
1. Use the retrieved data provided below to construct your response:
   {str(retrieved_data)}
2. Do not rely on your internal knowledge or make assumptions.
3. If the retrieved data does not contain enough information, respond with: "I could not find sufficient information in the knowledge base to answer your question."
4. Provide clear, concise, and professional responses.
5. If applicable, include region-specific or section-specific context in your answer.

Begin your response based on the user's query:
    """


def generate_response(client, system_prompt, user_query, model="gpt-4o", max_tokens=500, temperature=0.2):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_query}
        ],
        max_tokens=max_tokens,  # Limit the response length
        temperature=temperature  # Control the randomness of the response
    )
    return response.choices[0].message.content
