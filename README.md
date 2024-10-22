# AI-Robot

### 介绍
AI Agent使用ChatGPT作为底层大模型，通过LangChain实现个性化AI模型开发

### 服务器端：接口 -> LangChain -> OpenAI/ollama
#客户端：电报机器人、微信机器人、website。
#接口：http,https,websocket

### 服务器：
1. 接口访问，Python选型FastAPI
2. /chat的接口，post请求
3. /add_urls 从url中学习知识
4. /add_pdfs 从pdf里学习知识
5. /add_texts 从txt文本里学习

#人性化
1. 用户输入 -> AI判断一下当前问题的情绪倾向 -> 判断 -> 反馈 -> Agent判断
2. 工具调用： 用户发起请求 -> Agent判断使用哪个工具 -> 带着相关的参数去请求工具 -> 得到观察结果

### 截止目前：
1. Api
2. Agent框架
3. Tools:搜索、查询信息、专业知识库
4. 记忆，长时记忆
5. 学习能力

### 从url来学习，实现增强
1. 输入url
2. 地址的html变成文本
3. 向量化
4. 检索 -> 相关文本块
5. LLM回答

### 软件架构
软件架构说明
1. 采用ChatGPT作为底层大模型
2. 采用LangChain实现个性化AI模型开发
3. 采用Docker容器化部署
4. 使用Vector Database存储数据，实现个性化数据
5. 使用Redis + LangChain memory实现AI记忆能力
