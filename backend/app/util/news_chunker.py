from langchain_text_splitters import RecursiveCharacterTextSplitter


class NewsChunker:

    def __init__(self):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100,
            separators=[
                "\n\n",
                "\n",
                ". ",
                " "
            ]
        )


    def split(self, text: str) -> list[str]:
        return self.splitter.split_text(text)