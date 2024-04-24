from fastapi import FastAPI
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langserve import add_routes
import os

os.environ["OPENAI_API_KEY"] = "sk-xMC8z5QZoN9GdrUp724a2fBdC3C44aE68e51D2732377E2Be"
os.environ["OPENAI_API_BASE"] = "https://ai-yyds.com/v1"

app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="A simple api server using Langchain's Runnable interfaces",
)

add_routes(
    app,
    ChatOpenAI(),
    path="/openai",
)


model = ChatOpenAI()
prompt = ChatPromptTemplate.from_template("tell me a joke about {topic}")
add_routes(
    app,
    prompt | model,
    path="/joke",
)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
