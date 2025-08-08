from langchain_google_genai import ChatGoogleGenerativeAI
import asyncio
from dotenv import load_dotenv

from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from browser_use import Agent

load_dotenv()

def launch(args: {}):

    llm=ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-exp",
        transport="grpc"
    )

    # llm=ChatOpenAI(
    #     base_url='http://localhost:3000/api',
    #     model='deepseek/deepseek-r1:free',
    # )

    # llm=ChatOllama()

    agent = Agent(
        task=args["task"],
        llm=llm,
    )
    asyncio.run(agent.run())

# task = input("What do you want me to do?: ")
# launch({"task": task})
