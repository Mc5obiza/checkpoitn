
from langchain.prompts import PromptTemplate

from langchain.output_parsers import JsonOutputParser

from pydantic import BaseModel, Field

from langchain.chat_models import ChatOpenAI

 

 

class DocumentMetadata(BaseModel):

    title: str = Field(..., description="Title of the document")

    author: str = Field(..., description="Author of the document")

    publication_date: str = Field(..., description="Date in YYYY-MM-DD format")

    keywords: list[str] = Field(..., description="List of keywords")

    document_type: str = Field(..., description="Type of the document, e.g., report, article")

 

 

parser = JsonOutputParser(pydantic_object=DocumentMetadata)

 

 

prompt = PromptTemplate(

    template="""

    Extract the following metadata from the document text:

    title, author, publication_date, keywords, and document_type.

 

    Return the result in JSON strictly matching this schema:

    {format_instructions}

 

    Document text:

    {document_text}

    """,

    input_variables=["document_text"],

    partial_variables={"format_instructions": parser.get_format_instructions()}

)

 

 

model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

 

 

documents = [

    """This report, 'AI Trends 2025', was written by Dr. Sarah Lee and published on 2025-05-01.

       It covers topics like artificial intelligence, deep learning, and ethics in AI.""",

    """The article 'Climate Change and Agriculture' by John Smith was released on 2024-09-15.

       It discusses sustainability, farming practices, and environmental policy."""

]

 

 

structured_metadata = []

for doc in documents:

    prompt_text = prompt.format(document_text=doc)

    response = model.invoke(prompt_text)

    metadata = parser.parse(response.content)

    structured_metadata.append(metadata.dict())

for idx, data in enumerate(structured_metadata, start=1):

    print(f"Document {idx} metadata:")

    print(data)