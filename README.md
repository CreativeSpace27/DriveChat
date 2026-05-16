# DriveChat: AI-Powered Google Drive Assistant

DriveChat is an intelligent document discovery agent that transforms how users interact with their Google Drive. Built with a "Backend-as-Truth" architecture, it leverages Large Language Models (LLMs) to navigate complex file hierarchies, perform deep-content searches, and provide direct access links through a natural, conversational interface.

## 🚀 Live Demo
* **Frontend:** https://drivechat-fyj4zzcra8hbk6wpfqbdbh.streamlit.app/
* **Backend:** https://drivechat-***.onrender.com/chat

## 🛠️ Tech Stack
* **Inference Engine:** Groq (Llama-3.3-70B-Versatile) / Gemini 1.5 Flash.
* **Orchestration:** LangChain (Agentic Framework).
* **Backend:** FastAPI (Python).
* **Frontend:** Streamlit with Custom CSS (Gemini-inspired UI).
* **Storage API:** Google Drive API v3 (Service Account Authentication).

## 🎯 Key Discovery Features
TailorTalk is optimized for **Discoverability**, ensuring users can find files even with vague or complex criteria:

* **Recursive Sub-Folder Discovery:** Unlike standard searches, TailorTalk is configured to bypass "parent-only" constraints to find files buried deep within nested directories.
* **Temporal Queries:** Users can search for files based on time-relative requests (e.g., "modified in the last 2 days" or "latest updates"). The system dynamically calculates timestamps for the `modifiedTime` parameter.
* **Deep Content Search:** Leverages the `fullText` query parameter to find keywords located *inside* PDFs and documents, rather than just matching filenames.
* **Technical Filtering:** Support for `mimeType` filtering allows users to isolate specific file types like PDFs, Google Sheets, or Folders through natural language.
* **Direct Access Integration:** Every search result is presented with its `webViewLink`, allowing for one-click access directly from the chat interface.

## 🏗️ Architecture
The system utilizes a modular service-oriented architecture:
1.  **FastAPI Layer:** Acts as the single source of truth, managing tool execution and LLM orchestration.
2.  **Google Drive Service:** Handles secure authentication via Service Account "Secret Files" or Environment Variables and manages the construction of complex `q` parameters.
3.  **Streamlit Layer:** A minimalist, reactive frontend that communicates via REST API to the backend, featuring a right-aligned conversation flow and typewriter-effect responses.

## ⚙️ Installation & Setup

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/yourusername/tailortalk.git](https://github.com/yourusername/tailortalk.git)
    cd tailortalk
    ```

2.  **Environment Variables:**
    Create a `.env` file and include the following:
    ```env
    GROQ_API_KEY=your_key_here
    GOOGLE_CREDENTIALS={"your_service_account_json_content"}
    DRIVE_FOLDER_ID=your_shared_folder_id
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run Locally:**
    ```bash
    # Terminal 1: Backend
    uvicorn main:app --reload

    # Terminal 2: Frontend
    streamlit run streamlit_app.py
    ```

## 🔒 Security
* **Zero-Footprint Credentials:** Credentials are managed via Environment Variables and Render "Secret Files" to ensure no sensitive JSON data is ever committed to the repository.
* **Scoped Access:** The agent operates under a `drive.readonly` scope, ensuring it can only view files explicitly shared with its service account email.

---
**Developed by Piyush Bhadade**
