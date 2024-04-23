import os
from dotenv import load_dotenv
from typing import List, Dict, Any, Optional
from langchain.callbacks.manager import (
    CallbackManagerForChainRun
)
from langchain.chains.base import Chain
from langchain.prompts.base import BasePromptTemplate
from langchain.base_language import BaseLanguageModel
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

load_dotenv("openai.env")
api_key = os.getenv("OPENAI_API_KEY")
api_base = os.getenv("OPENAI_API_BASE")
os.environ["OPENAI_API_KEY"] = api_key
os.environ["OPENAI_API_BASE"] = api_base
print(f"API Key: {api_key}")
print(f"API Base URL: {api_base}")


# 自定义Chain
class wiki_article_chain(Chain):
    """开发一个wiki文章生成器"""
    prompt: BasePromptTemplate
    llm: BaseLanguageModel
    out_key: str = "text"

    @property
    def input_keys(self) -> List[str]:
        """将返回Prompt所需的所有键"""
        return self.prompt.input_variables

    @property
    def output_keys(self) -> List[str]:
        """将始终返回text键"""
        return [self.out_key]

    def _call(self, inputs: Dict[str, Any], run_manager: Optional[CallbackManagerForChainRun] = None,) -> Dict[str, Any]:
        """运行链"""
        prompt_value = self.prompt.format_prompt(**inputs)
        response = self.llm.generate_prompt(
            [prompt_value], callbacks=run_manager.get_child()
            if run_manager else None
        )
        if run_manager:
            run_manager.on_text("wiki article is written")
        return {self.out_key: response.generations[0][0].text}

    @property
    def _chain_type(self) -> str:
        """链类型"""
        return "wiki_article_chain"


if __name__ == '__main__':

    chain = wiki_article_chain(
        prompt=PromptTemplate(
            template="写一篇关于{topic}的维基百科形式的文章",
            input_variables=["topic"]
        ),
        llm=ChatOpenAI(
            temperature=0
        ),
    )
    result = chain.run({"topic": "降本增效"})
    print(result)
