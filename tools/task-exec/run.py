from browser_use.browser.browser import BrowserConfig
from langchain_openai import ChatOpenAI
from browser_use import Agent, Browser
from pydantic import SecretStr
from browser_use.browser.context import BrowserContext
from asyncio import run as execute

model = ChatOpenAI(
    base_url='https://localhost:3000/api/v1',
    model='jarvis:latest',
    api_key=SecretStr("sk-ac2b9ae7ef8f4a199ee43ac6598fcd6b"),
)
myBrowser = Browser().playwright_browser

myBrowser=Browser().playwright_browser
def execute_assignment(assignment: str):
    agent = Agent(
        task=assignment,
        llm=model,
        use_vision=False,
        browser=myBrowser
    )
    execute(agent.run())

def launch(args: []):
    return execute_assignment(args["prompt"])

# Testing inputs

# message = input()
# while message.lower != "exit":
#     execute_assignment(message)
#     message = input()
