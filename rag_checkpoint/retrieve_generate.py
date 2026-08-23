from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from index import index
import os
load_dotenv()
key = os.getenv("OPENAI_API_KEY")

if not key:
    raise ValueError("There is no API KEY provided")
client = ChatOpenAI(api_key=key, base_url="https://openrouter.ai/api/v1")
vectore_store= index()
def format_doc(docs):
    return "\n\n".join(doc.page_content for doc in docs)
def generate(query,k_top = 5):
    prompt = PromptTemplate.from_template(
        """ \
        {question}
        answer from the provided context 
        # CONTEXT
        {context}
        """
    )
    retriever = vectore_store.as_retriever(search_kwargs = {"k":k_top})
    chain = (
        {   "question" : RunnablePassthrough(),
            "context" : retriever | format_doc,
            
        }
        | prompt
        | client
        | StrOutputParser()
    )
    return chain.invoke(input = query)
print(generate("what is this book"))
