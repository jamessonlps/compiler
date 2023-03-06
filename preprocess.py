import re

class PrePro():

    @staticmethod
    def filter(text: str) -> str:
        """
        Remove all comments in the code.
        @param `text`: str
        """
        return re.sub(pattern=r"#.*", repl="", string=text)