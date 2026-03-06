# 🤖 AI Customer Support Copilot (End-to-End Agent)

This project is a sophisticated **AI-powered Customer Support Agent** built during the NVIDIA workshop series. It transitions from simple prompt engineering to a full-stack AI application featuring a **ReAct Agent**, **FastAPI** backend, and a **Streamlit** user interface.

## 🚀 Overview
The agent is designed to analyze customer messages, extract structured data (JSON), and autonomously decide when to use external tools (like order tracking) to provide accurate, real-time responses.

## 🏗️ Technical Stack
* **LLM Orchestration:** LangChain & LCEL (LangChain Expression Language).
* **Inference:** Groq Cloud (Llama 3.3 70B) & NVIDIA NIM.
* **Agent Logic:** ReAct (Reason + Act) pattern with Tool Calling.
* **Data Validation:** Pydantic for structured JSON output.
* **Backend:** FastAPI (Python).
* **Frontend:** Streamlit Chat UI.

## ✨ Key Features
* **Structured Output:** Automatically parses unstructured customer queries into valid JSON objects including `sentiment`, `issue_type`, and `order_id`.
* **Autonomous Tool Use:** The agent identifies when a user is asking about order status and triggers the `check_order_status` tool.
* **RAG Ready:** Integrated with FAISS vector store and HuggingFace embeddings for knowledge retrieval.
* **Professional UI:** A clean, interactive chat interface for seamless user interaction.

## 📂 Project Structure
```text
ai-support-copilot/
├── app.py              # FastAPI Backend & Agent Logic
├── ui.py               # Streamlit Frontend UI
├── requirements.txt    # Project Dependencies
├── kb.txt              # Knowledge Base for RAG (Optional)
└── README.md           # Project Documentation
🛠️ Installation & Setup
Clone the repository:

Bash
git clone [https://github.com/h-salah1117/ai-support-copilot.git](https://github.com/h-salah1117/ai-support-copilot.git)
cd ai-support-copilot
Install dependencies:

Bash
pip install -r requirements.txt
Set up Environment Variables:
Create a .env file or export your API key:

Bash
export GROQ_API_KEY="your_groq_api_key"
🚀 How to Run
You need to run the Backend API and the Frontend UI in two separate terminals.

Terminal 1: Start the FastAPI Server

Bash
python app.py
The API will be live at http://127.0.0.1:8000

Terminal 2: Start the Streamlit Interface

Bash
streamlit run ui.py
🤖 Reasoning Logic (ReAct)
The agent follows the Thought-Action-Observation loop:

Thought: Analyzes if the user's query requires an external tool (e.g., checking an order ID).

Action: Calls the check_order_status function if an ID is present.

Observation: Receives real-time data from the tool.

Final Response: Generates a friendly, human-like response injected with the retrieved data.

Built with ❤️ by Hazem Mohammad Salah