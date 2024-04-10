# 使用最大余弦相似度来检索相关示例，以使示例尽量符合输入
from langchain.prompts.example_selector import SemanticSimilarityExampleSelector
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.prompts import FewShotPromptTemplate, PromptTemplate
import os

os.environ['OPENAI_KEY'] = 'sk-xMC8z5QZoN9GdrUp724a2fBdC3C44aE68e51D2732377E2Be'
os.environ['OPENAI_API_BASE'] = 'https://ai-yyds.com/v1'

api_base = os.getenv("OPENAI_API_BASE")
api_key = os.getenv("OPENAI_KEY")


example_prompt = PromptTemplate(
    input_variables=["input", "output"],
    template="原词: {input}\n反义: {output}",
)

# Examples of a pretend task of creating antonyms.
examples = [
    {"input": "happy", "output": "sad"},
    {"input": "tall", "output": "short"},
    {"input": "energetic", "output": "lethargic"},
    {"input": "sunny", "output": "gloomy"},
    {"input": "windy", "output": "calm"},
]

example_selector = SemanticSimilarityExampleSelector.from_examples(
    # 传入示例组.
    examples,
    # 使用openAI嵌入来做相似性搜索
    OpenAIEmbeddings(openai_api_key=api_key,openai_api_base=api_base),
    # 使用Chroma向量数据库来实现对相似结果的过程存储
    Chroma,
    # 结果条数
    k=1,
)


# 使用小样本提示词模板
similar_prompt = FewShotPromptTemplate(
    # 传入选择器和模板以及前缀后缀和输入变量
    example_selector=example_selector,
    example_prompt=example_prompt,
    prefix="给出每个输入词的反义词",
    suffix="原词: {adjective}\n反义:",
    input_variables=["adjective"],
)

# 输入一个形容感觉的词语，应该查找近似的 happy/sad 示例
print(similar_prompt.format(adjective="worried"))
