import requests
from langchain_text_splitters import RecursiveCharacterTextSplitter
url = "https://gutenberg.org/cache/epub/79438/pg79438.txt"
text = requests.get(url).text
with open("docs/book.txt", "w", encoding="utf-8") as f:
    f.write(text)
def chunk():

    chuncker = RecursiveCharacterTextSplitter(chunk_size=100,chunk_overlap=20,length_function=len,is_separator_regex=False)
    texts = chuncker.split_text(text)
    return texts
