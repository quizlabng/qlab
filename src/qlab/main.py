from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from qlab.api.request import ChatRequest
from qlab.api.response import BaseResponse, ChatResponse
from qlab.rag.chat import chat

app = FastAPI()

@app.get("/")
async def status():
    return BaseResponse(message="Quizlab AI server is running")

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    # /vercel.svg is served automatically from public/vercel.svg.
    return RedirectResponse("/favicon.svg", status_code=307)


@app.post("/chat")
async def chat_request(request: ChatRequest):

    response = chat(user=request.user, prompt=request.message)

    return ChatResponse(content=response.content)