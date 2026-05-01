import os
import asyncio
import json
from typing import AsyncIterable, Any, Dict, List
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel
from langchain_community.llms import Ollama
from langchain.agents import create_react_agent, AgentExecutor
from langchain.prompts import PromptTemplate
from langchain.callbacks.base import BaseCallbackHandler
from tools import agent_tools

app = FastAPI()

# Mount the static directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Define the request model
class ChatRequest(BaseModel):
    message: str

# Initialize the Ollama model
MODEL_NAME = "dolphin-llama3" 
try:
    llm = Ollama(model=MODEL_NAME, temperature=0.1)
except Exception as e:
    print(f"Error connecting to Ollama: {e}")
    llm = None

template = """You are a highly capable autonomous cybersecurity agent designed for Capture The Flag (CTF) competitions and ethical hacking. 
You are equipped with a vast array of capabilities:
- You can use the `cyberchef_recipe` tool for operations like: ROT, Caesar, XOR, ASCII shift, base64, hex, hexdump, Regex, url decode, and common encryption methods.
- You can use the `execute_command` tool to run advanced forensics and reversing tools available in your environment, such as: hashcat (with popular dictionaries), pwntools (via python), steganography tools (steghide, zsteg, binwalk, exiftool), extract audio metadata, detect file types, extract RGBA data, and other forensic tools.

You have access to the following tools to help you investigate, enumerate, and analyze:

{tools}

To use a tool, please use the following exact format:

Thought: Do I need to use a tool? Yes
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action

When you have gathered enough information to answer the question or complete the task, use this format:

Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}"""

prompt = PromptTemplate.from_template(template)

# Global queue for SSE broadcasting
clients = set()

async def broadcast_event(data: dict):
    message = f"data: {json.dumps(data)}\n\n"
    for queue in clients:
        await queue.put(message)

class SSECallbackHandler(BaseCallbackHandler):
    """Callback handler that broadcasts agent events via SSE."""
    
    def on_llm_start(self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any) -> None:
        asyncio.create_task(broadcast_event({"type": "llm_start", "content": "LLM starting thought process..."}))

    def on_tool_start(self, serialized: Dict[str, Any], input_str: str, **kwargs: Any) -> None:
        tool_name = serialized.get("name", "tool")
        asyncio.create_task(broadcast_event({"type": "tool_start", "tool": tool_name, "input": input_str}))

    def on_tool_end(self, output: str, **kwargs: Any) -> None:
        asyncio.create_task(broadcast_event({"type": "tool_end", "output": output[:500] + ('...' if len(output) > 500 else '')}))

    def on_agent_action(self, action: Any, **kwargs: Any) -> Any:
        asyncio.create_task(broadcast_event({"type": "agent_action", "tool": action.tool, "tool_input": action.tool_input, "log": action.log}))

    def on_agent_finish(self, finish: Any, **kwargs: Any) -> None:
        asyncio.create_task(broadcast_event({"type": "agent_finish", "log": finish.log}))
        
    def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        pass # We don't stream tokens directly for ReAct unless parsing them, as ReAct output is structured

prompt = PromptTemplate.from_template(template)

if llm:
    agent = create_react_agent(llm, agent_tools, prompt)
    agent_executor = AgentExecutor(
        agent=agent, 
        tools=agent_tools, 
        verbose=True, 
        handle_parsing_errors=True,
        max_iterations=15
    )
else:
    agent_executor = None

@app.get("/")
def read_root():
    return FileResponse("static/index.html")

@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    if not agent_executor:
        return {"response": "Error: Agent is not initialized. Make sure Ollama is running and the model is pulled."}
    
    try:
        # Run with SSE callbacks
        response = agent_executor.invoke(
            {"input": request.message},
            config={"callbacks": [SSECallbackHandler()]}
        )
        return {"response": response.get("output", "No output generated.")}
    except Exception as e:
        return {"response": f"An error occurred: {str(e)}"}

@app.get("/api/stream")
async def stream_logs(request: Request):
    """SSE endpoint for streaming agent logs to the frontend terminal."""
    queue = asyncio.Queue()
    clients.add(queue)

    async def event_generator():
        try:
            while True:
                # Disconnect logic
                if await request.is_disconnected():
                    break
                # Wait for new message
                message = await queue.get()
                yield message
        except asyncio.CancelledError:
            pass
        finally:
            clients.remove(queue)

    return StreamingResponse(event_generator(), media_type="text/event-stream")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
