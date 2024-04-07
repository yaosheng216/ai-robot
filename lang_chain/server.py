import os
import openai

os.environ['OPENAI_KEY'] = 'sk-xMC8z5QZoN9GdrUp724a2fBdC3C44aE68e51D2732377E2Be'
os.environ['OPENAI_API_BASE'] = 'https://ai-yyds.com/v1'

openai.api_key = os.getenv('OPENAI_KEY')
openai.api_base = os.getenv("OPENAI_API_BASE")


def main():
    messages = [{"role": "user", "content": "使用Java语言实现快速排序"}]
    res = openai.ChatCompletion.create(
        model="gpt-4-1106-preview",
        messages=messages,
        stream=False,
    )
    print(res['choices'][0]['message']['content'])


if __name__ == '__main__':
    main()
