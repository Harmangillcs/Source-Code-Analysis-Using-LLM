from flask import Flask, render_template, request, jsonify
import os
from langchain.vectorstores import FAISS
from langchain.llms import CTransformers
from langchain.memory import ConversationSummaryMemory
from langchain.chains import ConversationalRetrievalChain
from src.helper import load_embedding, repo_repsitry

app = Flask(__name__)

# Load Embeddings
embeddings = load_embedding()

# Load FAISS DB (initial dummy until updated from repo)
vectordb = FAISS.load_local("research/faiss_index", embeddings)

# Load LLM
llm = CTransformers(
    model=r"G:\Source-Code-Analysis-Using-LLM\model\tinyllama-1.1b-chat-v1.0.Q5_0.gguf",
    model_type="llama",
    config={
        "max_new_tokens": 350,
        "temperature": 0.7,
        "context_length": 2048
    }
)

# Memory and chain
memory = ConversationSummaryMemory(llm=llm, memory_key="chat_history", return_messages=True)
qa = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=vectordb.as_retriever(search_type="mmr", search_kwargs={"k": 3}),
    memory=memory,
)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/chatbot", methods=["POST"])
def git_repo():
    try:
        print("Received request to /chatbot")
        print("Request JSON:", request.json)

        user_input = request.json.get("url")
        if not user_input:
            return jsonify({"error": "No URL provided"}), 400

        print(f"Cloning repo: {user_input}")
        repo_repsitry(user_input)
        os.system("python store_index.py")

        return jsonify({"message": "Repository processed successfully"})

    except Exception as e:
        print("🔥 Error in /chatbot route:", str(e))  
        return jsonify({"error": str(e)}), 500


@app.route("/get", methods=["POST"])
def chat():
    try:
        msg = request.json.get("msg")
        if not msg:
            return jsonify({"answer": "No message provided."})
        if msg.lower() == "clear":
            os.system("rm -rf repo")
            return jsonify({"answer": "Repository cleared."})

        result = qa(msg)
        return jsonify({"answer": result["answer"]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
