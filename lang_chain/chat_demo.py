from dotenv import load_dotenv
from langchain.document_loaders import UnstructuredExcelLoader,Docx2txtLoader,PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import os

load_dotenv("openai.env")
api_key = os.getenv("OPENAI_API_KEY")
api_base = os.getenv("OPENAI_API_BASE")
os.environ["OPENAI_API_KEY"] = api_key
os.environ["OPENAI_API_BASE"] = api_base
print(f"API Key: {api_key}")
print(f"API Base URL: {api_base}")


class ChatDoc():
    def __init__(self):
        self.doc = None
        self.splitText = []  # 分割后的文本
        self.template = [
            ("system",
             "你是一个处理文档的秘书,你从不说自己是一个大模型或者AI助手,你会根据下面提供的上下文内容来继续回答问题.\n 上下文内容\n {context} \n"),
            ("human", "你好！"),
            ("ai", "你好"),
            ("human", "{question}"),
        ]
        self.prompt = ChatPromptTemplate.from_messages(self.template)

    def getFile(self):
        doc = self.doc
        loaders = {
            "docx": Docx2txtLoader,
            "pdf": PyPDFLoader,
            "xlsx": UnstructuredExcelLoader,
        }
        file_extension = doc.split(".")[-1]
        loader_class = loaders.get(file_extension)
        if loader_class:
            try:
                loader = loader_class(doc)
                text = loader.load()
                return text
            except Exception as e:
                print(f"Error loading {file_extension} files:{e}")
        else:
            print(f"Unsupported file extension: {file_extension}")
            return None

    # 处理文档的函数
    def splitSentences(self):
        full_text = self.getFile()  # 获取文档内容
        if full_text is not None:
            # 对文档进行分割
            text_split = CharacterTextSplitter(
                chunk_size=150,
                chunk_overlap=20,
            )
            texts = text_split.split_documents(full_text)
            self.splitText = texts

    # 向量化与向量存储
    def embeddingAndVectorDB(self):
        embeddings = OpenAIEmbeddings()
        db = Chroma.from_documents(
            documents=self.splitText,
            embedding=embeddings
        )
        print('===========================')
        return db

    # 提问并找到相关的文本块
    def askAndFindFiles(self, question):
        db = self.embeddingAndVectorDB()
        # retriever = db.as_retriever(search_type="mmr")
        retriever = db.as_retriever(search_type="similarity_score_threshold",
                                    search_kwargs={"score_threshold": .5, "k": 1})
        return retriever.get_relevant_documents(query=question)

    # 用自然语言和文档聊天
    def chatWithDoc(self, question):
        _content = ""
        context = self.askAndFindFiles(question)
        for i in context:
            _content += i.page_content

        messages = self.prompt.format_messages(context=_content, question=question)
        chat = ChatOpenAI(
            model="gpt-4",
            temperature=0,
        )
        return chat.invoke(messages)


chat_doc = ChatDoc()
chat_doc.doc = "fake.docx"
chat_doc.splitSentences()
chat_doc.chatWithDoc("公司注册地址是哪里？")
