from langchain.prompts import PromptTemplate
from langchain.document_loaders import PyPDFLoader
from langchain.chat_models import ChatOpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain


loader = PyPDFLoader("loader.pdf")
docs = loader.load()
# 文本切分
text_split = CharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=1000,
    chunk_overlap=0
)
split_docs = text_split.split_documents(docs)

prompt_template = """对以下文字做简洁的总结:
                    {text}
                    简洁的总结:"""

prompt = PromptTemplate.from_template(prompt_template)

refine_template = (
    "你的任务是产生最终摘要\n"
    "我们已经提供了一个到某个特定点的现有回答:{existing_answer}\n"
    "我们有机会通过下面的一些更多上下文来完善现有的回答(仅在需要时使用).\n"
    "------------\n"
    "{text}\n"
    "------------\n"
    "根据新的上下文，用中文完善原始回答.\n"
    "如果上下文没有用处,返回原始回答."
)

refine_prompt = PromptTemplate.from_template(refine_template)
llm = ChatOpenAI(
    temperature=0,
    model="gpt-3.5-turbo",
)

chain = load_summarize_chain(
    llm=llm,
    chain_type="refine",
    question_prompt=prompt,
    refine_prompt=refine_prompt,
    return_intermediate_steps=True,
    input_key="documents",
    output_key="output_text",
)

result = chain({"documents":split_docs},return_only_outputs=True)
print(result["output_text"])
