import os
from langchain.llms import OpenAI

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
    msg = llm.predict("写一段入职报告")
    print(msg)


if __name__ == '__main__':
    main()
