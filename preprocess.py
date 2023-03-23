import re

class PrePro():

    @staticmethod
    def filter(text: str) -> str:
        """
        Remove all comments in the code.
        @param `text`: str
        """
        removed_comments = re.sub(pattern=r"#.*", repl="", string=text)
        # removed_final_white_spaces = re.sub(pattern=r"\s+$", repl="", string=removed_comments)
        return removed_comments


    @staticmethod
    def add_eof(text: str) -> str:
        """
        Add the EOF to the given string.
        """
        return text + "\0"