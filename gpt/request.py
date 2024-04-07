import openai
from flask import Flask
import os

# 实例化Flask
app = Flask(__name__)

os.environ['OPENAI_KEY'] = 'sk-xMC8z5QZoN9GdrUp724a2fBdC3C44aE68e51D2732377E2Be'
os.environ['OPENAI_API_BASE'] = 'https://ai-yyds.com/v1'

openai.api_key = os.getenv('OPENAI_KEY')
openai.api_base = os.getenv("OPENAI_API_BASE")


@app.route('/gpt/search/<message>', methods=['GET'])
def gptService(message):
    print('message is:', message)
    # 调用openai的API
    messages = [{"role": "user", "content": message}]
    res = openai.ChatCompletion.create(
        model="gpt-4-1106-preview",
        messages=messages,
        stream=False,
        timeout=3000
    )
    # 结果
    print('GPT结果:' + res['choices'][0]['message']['content'])
    return res['choices'][0]['message']['content']


if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
