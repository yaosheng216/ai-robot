from langchain.schema import SystemMessage
from langchain.schema import HumanMessage
from langchain.schema import AIMessage


def main():
    sy = SystemMessage(
        content="你是一个起名大师",
        additional_kwargs={"大师姓名": "陈瞎子"}
    )
    hu = HumanMessage(
        content="请问大师叫什么?"
    )
    ai = AIMessage(
        content="我叫陈瞎子"
    )
    print([sy, hu, ai])