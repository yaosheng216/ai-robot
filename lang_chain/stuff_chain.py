import os
from dotenv import load_dotenv
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.document_loaders import PyPDFLoader
from langchain.chat_models import ChatOpenAI

load_dotenv("openai.env")
api_key = os.getenv("OPENAI_API_KEY")
api_base = os.getenv("OPENAI_API_BASE")
os.environ["OPENAI_API_KEY"] = api_key
os.environ["OPENAI_API_BASE"] = api_base


# 加载pdf文档
loader = PyPDFLoader("loader.pdf")
prompt_template = """对以下文字做简洁的总结:
                    {text}
                    简洁的总结:"""

prompt = PromptTemplate.from_template(prompt_template)
llm = ChatOpenAI(
    temperature=0,
    model="gpt-4-1106-preview",
)
llm_chain = LLMChain(llm=llm, prompt=prompt)

stuff_chain = StuffDocumentsChain(
    llm_chain=llm_chain,
    document_variable_name="text",
)
docs = loader.load()
print(stuff_chain.run(docs))
