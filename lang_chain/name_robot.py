from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
import os
from langchain.schema import BaseOutputParser


# 自定义类
class CommaSeparatedListOutputParser(BaseOutputParser):
    """Parse the output of an LLM call to a comma-separated list."""

    def parse(self, text: str):
        """Parse the output of an LLM call."""
        print(text)
        return text.strip().split(",")


os.environ['OPENAI_KEY'] = 'sk-xMC8z5QZoN9GdrUp724a2fBdC3C44aE68e51D2732377E2Be'
os.environ['OPENAI_API_BASE'] = 'https://ai-yyds.com/v1'

api_base = os.getenv("OPENAI_API_BASE")
api_key = os.getenv("OPENAI_KEY")


def main():
    llm = OpenAI(
        model="gpt-3.5-turbo-instruct",
        temperature=0,
        openai_api_key=api_key,
        openai_api_base=api_base
    )
    # LangChain提词器
    prompt = PromptTemplate.from_template(
        "你是一个起名大师,请模仿示例起3个具有{county}特色的名字,示例：男孩常用名{boy},女孩常用名{girl}。请返回以逗号分隔的列表形式。仅返回逗号分隔的列表，不要返回其他内容")
    message = prompt.format(county="美国男孩", boy="sam", girl="lucy")
    print(message)
    strs = llm.predict(message)
    msg = CommaSeparatedListOutputParser().parse(strs)
    print('名字是:', msg)


if __name__ == '__main__':
    main()
