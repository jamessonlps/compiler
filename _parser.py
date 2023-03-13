from preprocess import PrePro
from tokenizer import Tokenizer
from tokens import *
from node import *


class Parser():
    tokenizer: Tokenizer = None

    @staticmethod
    def parseExpression() -> Node:
        """
        Starting point: get the next token and call parse term.
        """
        
        # Get the next token
        Parser.tokenizer.selectNext()
        
        # Next instance must be compatible with Factor (num, '+', '-' and '(' )
        if isinstance(Parser.tokenizer.next, (NumberToken, PlusToken, MinusToken, LeftParenthesisToken)):
            term = Parser.parseTerm()
            valid_term = True
            
            # After receive the result from parse term, the next token
            # must be '+', '-' or none (return the term calculated), following
            # by another term when we request the next token.
            while valid_term:
                if isinstance(Parser.tokenizer.next, PlusToken):
                    Parser.tokenizer.selectNext()
                    if isinstance(Parser.tokenizer.next, (NumberToken, PlusToken, MinusToken, LeftParenthesisToken)):
                        term2 = Parser.parseTerm()
                        term = BinUp(value="+", children=[term, term2])
                        # term += Parser.parseTerm()
                    else:
                        raise SyntaxError
                
                if isinstance(Parser.tokenizer.next, MinusToken):
                    Parser.tokenizer.selectNext()
                    if isinstance(Parser.tokenizer.next, (NumberToken, PlusToken, MinusToken, LeftParenthesisToken)):
                        term2 = Parser.parseTerm()
                        term = BinUp(value="-", children=[term, term2])
                        # term -= Parser.parseTerm()
                    else:
                        raise SyntaxError
                
                if isinstance(Parser.tokenizer.next, (PlusToken, MinusToken)):
                    # Parser.tokenizer.selectNext()
                    pass
                else:
                    valid_term = False

            return term
        else:
            raise SyntaxError("Error on parseExpression")



    @staticmethod
    def parseTerm() -> Node:
        """
        Call `parseFactor` and apply multiplication and division
        if necessary.
        """

        # Factor can receive '+, '-', number and '(' tokens.
        if isinstance(Parser.tokenizer.next, (NumberToken, PlusToken, MinusToken, LeftParenthesisToken)):
            factor = Parser.parseFactor()
            Parser.tokenizer.selectNext()
            
            # After receive the result from parse factor, the next token
            # must be '*', '/' or none (return the factor calculated), following
            # by another factor when we request the next token.
            valid_factor = True
            while valid_factor:
                if isinstance(Parser.tokenizer.next, MultiplicationToken):
                    Parser.tokenizer.selectNext()
                    if isinstance(Parser.tokenizer.next, (NumberToken, PlusToken, MinusToken, LeftParenthesisToken)):
                        factor2 = Parser.parseFactor()
                        factor = BinUp(value="*", children=[factor, factor2])
                        # factor *= Parser.parseFactor()
                        Parser.tokenizer.selectNext()
                    else:
                        raise SyntaxError("Multiplication Error")
                
                if isinstance(Parser.tokenizer.next, DivisionToken):
                    Parser.tokenizer.selectNext()
                    if isinstance(Parser.tokenizer.next, (NumberToken, PlusToken, MinusToken, LeftParenthesisToken)):
                        factor2 = Parser.parseFactor()
                        factor = BinUp(value="/", children=[factor, factor2])
                        # factor //= Parser.parseFactor()
                        Parser.tokenizer.selectNext()
                    else:
                        raise SyntaxError("Division Error")
                
                if not isinstance(Parser.tokenizer.next, (MultiplicationToken, DivisionToken)):
                    valid_factor = False
                
            return factor
        else:
            raise SyntaxError("Error on parseTerm")



    @staticmethod
    def parseFactor() -> Node:
        """
        A factor must start with `number`, `+`, `-` or `(`.
        Then, can call `parseFactor` or `parseExpression` to calculate
        the return value.
        """
        if isinstance(Parser.tokenizer.next, NumberToken):
            return IntVal(value=Parser.tokenizer.next.value)
            # return Parser.tokenizer.next.value
        
        elif isinstance(Parser.tokenizer.next, PlusToken):
            Parser.tokenizer.selectNext()
            factor = Parser.parseFactor()
            return UnOp(value="+", children=[factor])
        
        elif isinstance(Parser.tokenizer.next, MinusToken):
            Parser.tokenizer.selectNext()
            factor = Parser.parseFactor()
            return UnOp(value="-", children=[factor])
        
        elif isinstance(Parser.tokenizer.next, LeftParenthesisToken):
            expression = Parser.parseExpression()
            if isinstance(Parser.tokenizer.next, RightParenthesisToken):
                return expression
            raise SyntaxError("An opened parenthesis must be closed.")
        
        else:
            raise SyntaxError("Error on parseFactor!")



    @staticmethod
    def run(code) -> int:
        remove_comments = PrePro.filter(text=code)
        code_processed = PrePro.add_eof(text=remove_comments)
        
        Parser.tokenizer = Tokenizer(source=code_processed)
        
        result = Parser.parseExpression().evaluate()
        print(result)

        if isinstance(Parser.tokenizer.next, EndOfFileToken):
            return result
        raise SyntaxError("Where is EOF?")