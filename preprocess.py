import re

class PrePro():

    @staticmethod
    def filter(text: str) -> str:
        """
        Remove all comments in the code.
        @param `text`: str
        """
        return re.sub(pattern=r"#.*", repl="", string=text)


    @staticmethod
    def add_eof(text: str) -> str:
        """
        Add the EOF to the given string.
        """
        return text + "\0"