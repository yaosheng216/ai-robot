import os
from doctran import Doctran

os.environ['OPENAI_KEY'] = 'sk-xMC8z5QZoN9GdrUp724a2fBdC3C44aE68e51D2732377E2Be'
os.environ['OPENAI_API_BASE'] = 'https://ai-yyds.com/v1'
api_base = os.getenv("OPENAI_API_BASE")
api_key = os.getenv("OPENAI_KEY")
OPENAI_MODEL = "gpt-3.5-turbo-16k"
OPENAI_TOKEN_LIMIT = 8000

# 加载文档
with open("test.txt") as f:
    content = f.read()

doctrans = Doctran(
    openai_api_key=api_key,
    openai_model=OPENAI_MODEL,
    openai_token_limit=OPENAI_TOKEN_LIMIT,
)
documents = doctrans.parse(content=content)

# 总结文档
summary = documents.summarize(token_limit=100).execute()
summary = summary.translate(language="chinese").execute()
print('总结文档是:', summary.transformed_content)

# 翻译一下文档
translation = documents.translate(language="chinese").execute()
print('翻译文档是:', translation.transformed_content)

# 精炼文档，删除除了某个主题或关键词之外的内容，仅保留与主题相关的内容
refined = documents.refine(topics=["marketing","Development"]).execute()
refined = refined.translate(language="chinese").execute()
print('精炼文档是:', refined.transformed_content)
