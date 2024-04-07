from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
import os

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
    prompt = PromptTemplate.from_template("你是一个起名大师,请给孩子起3个名字,爸爸叫做{father},妈妈叫做{mother}")
    message = prompt.format(father="姚圣", mother="刘新盼")
    print(message)
    msg = llm.predict(message)
    print('名字生成结果:', msg)


if __name__ == '__main__':
    main()
