from fastapi import FastAPI
from pydantic import BaseModel
from langchain_groq import ChatGroq
from langchain.agents import create_agent
from tools import google_drive_search
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

# 1. Load environment variables at the very beginning
load_dotenv()

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

# 2. Initialize the Groq Model
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0
)

# 3. Define your list of tools
tools = [google_drive_search]

# 4. Set up dynamic date context
now = datetime.utcnow()
today_str = now.strftime('%Y-%m-%dT%H:%M:%SZ')

# 5. Create Agent
agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=f"""
    You are a professional Google Drive assistant.
    The current time is {today_str}.
    
    Guidelines for using the 'google_drive_search' tool:
    - DISCOVERABILITY: Use the q parameter for accurate results.
    - SEARCHING BY DATE: Convert relative dates properly.
    - LASTLY UPDATED: Use order_by="modifiedTime desc".
    - SEARCH BY CONTENT: Use 'fullText contains'.
    - Be conversational and professional.

    STRICT OUTPUT RULES:

    1. ALWAYS format every result on a NEW LINE.
    2. NEVER put multiple files in the same bullet point.
    3. ALWAYS use proper Markdown Number formatting.
    4. ALWAYS display file type clearly.
    5. ALWAYS leave one blank line between each file result.
    6. If link exists, show clickable markdown link.
    7. If no results found, clearly say that.

    CORRECT FORMAT EXAMPLE:

    1 **ASSIGNMENT** (Folder) - [Click here to view](URL)

    2 **party packages** (Folder) - [Click here to view](URL)

    3 **invoice.pdf** (PDF File) - [Click here to view](URL)

    4 **photo.png** (Image File) - [Click here to view](URL)

    IMPORTANT:
    - NEVER combine all results into one paragraph.
    - NEVER use "*" improperly.
    - NEVER remove line breaks.
    - EVERY file MUST appear separately.
    """
)

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:

        # Invoke agent
        result = agent.invoke({
            "messages": [
                {
                    "role": "user",
                    "content": request.message
                }
            ]
        })

        # Extract response
        response_content = result["messages"][-1].content

        # CLEANUP FIXES
        response_content = response_content.replace("* *", "\n- ")
        response_content = response_content.replace("* **", "\n- **")

        return {"response": response_content}

    except Exception as e:

        print(f"Backend Error: {e}")

        return {
            "response": f"I encountered a technical issue: {str(e)}"
        }