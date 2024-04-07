import openai
from flask import Flask

# 实例化Flask
app = Flask(__name__)


@app.route('/gpt/search/<message>', methods=['GET'])
def gptService(message):
    print('message is:', message)
    # 调用openai的API
    client = openai.OpenAI(api_key='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')
    chat_completion = client.chat.completions.create(
        # 发送的消息内容
        messages=[
            {"role": "user", "content": message},
        ],
        # 选择模型(模型可以在openai官网查到)
        model='gpt-3.5-turbo-1106',
        # 结果生成结束以后，同步返回
        stream=False,
        timeout=3000
    )
    # 结果
    print('ChatGPT result is:', chat_completion.choices[0].message)
    return chat_completion.choices[0].message


if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
