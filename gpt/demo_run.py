from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from lang_chain.demo import wiki_article_chain


chain = wiki_article_chain(
    prompt=PromptTemplate(
        template="写一篇关于{topic}的维基百科形式的文章",
        input_variables=["topic"]
    ),
    llm=ChatOpenAI(
        temperature=0
    ),
)

result = chain.run({"topic":"降本增效"})
print(result)
