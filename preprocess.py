class PrePro():

    @staticmethod
    def filter(text: str) -> str:
        """
        Remove comments outside double-quoted strings in the code.
        @param `text`: str
        """
        result = []
        in_string = False
        in_comment = False

        for char in text:
            if in_comment:
                if char not in "\r\n":
                    continue
                in_comment = False
            elif char == '"':
                in_string = not in_string
            elif char == "#" and not in_string:
                in_comment = True
                continue
            result.append(char)

        return "".join(result)


    @staticmethod
    def add_eof(text: str) -> str:
        """
        Add the EOF to the given string.
        """
        return text + "\0"
