from langchain.document_loaders import TextLoader

loader = TextLoader("loader.md")
msg = loader.load()
print(msg)
