from preprocess import PrePro
from tokenizer import Tokenizer
from tokens import *
from node import *


def is_factor_token(token: Token) -> bool:
    return isinstance(token, (NumberToken, PlusToken, MinusToken, LeftParenthesisToken, IdentifierToken, DenialToken, ReadlineToken, StringToken))

def is_statement_token(token: Token) -> bool:
    return isinstance(token, (BreakLineToken, IdentifierToken, PrintlnToken, WhileToken, IfToken))

class Parser():
    tokenizer: Tokenizer = None

    @staticmethod
    def parseRelExpression() -> Node:
        """
        Starting point: get the next token and call parse term.
        """
        
        Parser.tokenizer.selectNext()
        
        if is_factor_token(Parser.tokenizer.next):
            expression = Parser.parseExpression()
            valid_expression = True
            
            while valid_expression:
                if isinstance(Parser.tokenizer.next, CompareEqualToToken):
                    Parser.tokenizer.selectNext()
                    if is_factor_token(Parser.tokenizer.next):
                        expression2 = Parser.parseExpression()
                        expression = BinUp(value="==", children=[expression, expression2])
                    else:
                        raise SyntaxError("After '==', the next token shoud be a valid factor token, but received: ", Parser.tokenizer.next)
                
                elif isinstance(Parser.tokenizer.next, CompareGreaterThenToken):
                    Parser.tokenizer.selectNext()
                    if is_factor_token(Parser.tokenizer.next):
                        expression2 = Parser.parseExpression()
                        expression = BinUp(value=">", children=[expression, expression2])
                    else:
                        raise SyntaxError("After '>', the next token shoud be a valid factor token, but received: ", Parser.tokenizer.next)
                
                elif isinstance(Parser.tokenizer.next, CompareLessThenToken):
                    Parser.tokenizer.selectNext()
                    if is_factor_token(Parser.tokenizer.next):
                        expression2 = Parser.parseExpression()
                        expression = BinUp(value="<", children=[expression, expression2])
                    else:
                        raise SyntaxError("After '<', the next token shoud be a valid factor token, but received: ", Parser.tokenizer.next)
                
                if isinstance(Parser.tokenizer.next, (CompareEqualToToken, CompareLessThenToken, CompareGreaterThenToken)):
                    pass
                else:
                    valid_expression = False

            return expression
        else:
            raise SyntaxError(f"Error on parseExpression. Token received: {Parser.tokenizer.next._value}")


    @staticmethod
    def parseExpression() -> Node:
        
        if is_factor_token(Parser.tokenizer.next):
            term = Parser.parseTerm()
            valid_term = True
            
            while valid_term:
                if isinstance(Parser.tokenizer.next, PlusToken):
                    Parser.tokenizer.selectNext()
                    if is_factor_token(Parser.tokenizer.next):
                        term2 = Parser.parseTerm()
                        term = BinUp(value="+", children=[term, term2])
                    else:
                        raise SyntaxError
                
                elif isinstance(Parser.tokenizer.next, MinusToken):
                    Parser.tokenizer.selectNext()
                    if is_factor_token(Parser.tokenizer.next):
                        term2 = Parser.parseTerm()
                        term = BinUp(value="-", children=[term, term2])
                    else:
                        raise SyntaxError
                
                elif isinstance(Parser.tokenizer.next, LogicOrToken):
                    Parser.tokenizer.selectNext()
                    if is_factor_token(Parser.tokenizer.next):
                        term2 = Parser.parseTerm()
                        term = BinUp(value="||", children=[term, term2])
                    else:
                        raise SyntaxError("After '||', the next token shoud be a factor valid token, but received: ", Parser.tokenizer.next)
                
                if isinstance(Parser.tokenizer.next, (PlusToken, MinusToken, LogicOrToken)):
                    pass
                else:
                    valid_term = False

            return term
        else:
            raise SyntaxError("Error on parseExpression")



    @staticmethod
    def parseTerm() -> Node:

        if is_factor_token(Parser.tokenizer.next):
            factor = Parser.parseFactor()
            Parser.tokenizer.selectNext()
            
            valid_factor = True
            while valid_factor:
                if isinstance(Parser.tokenizer.next, MultiplicationToken):
                    Parser.tokenizer.selectNext()
                    if is_factor_token(Parser.tokenizer.next):
                        factor2 = Parser.parseFactor()
                        factor = BinUp(value="*", children=[factor, factor2])
                        Parser.tokenizer.selectNext()
                    else:
                        raise SyntaxError("Multiplication Error")
                
                elif isinstance(Parser.tokenizer.next, DivisionToken):
                    Parser.tokenizer.selectNext()
                    if is_factor_token(Parser.tokenizer.next):
                        factor2 = Parser.parseFactor()
                        factor = BinUp(value="/", children=[factor, factor2])
                        Parser.tokenizer.selectNext()
                    else:
                        raise SyntaxError("Division Error")
                
                elif isinstance(Parser.tokenizer.next, LogicAndToken):
                    Parser.tokenizer.selectNext()
                    if is_factor_token(Parser.tokenizer.next):
                        factor2 = Parser.parseFactor()
                        factor = BinUp(value="&&", children=[factor, factor2])
                        Parser.tokenizer.selectNext()
                    else:
                        raise SyntaxError("Logical AND operator error")
                    
                elif isinstance(Parser.tokenizer.next, DotToken):
                    Parser.tokenizer.selectNext()
                    if is_factor_token(Parser.tokenizer.next):
                        factor2 = Parser.parseFactor()
                        factor = BinUp(value=".", children=[factor, factor2])
                        Parser.tokenizer.selectNext()
                    else:
                        raise SyntaxError("String concatenation error")
                
                if not isinstance(Parser.tokenizer.next, (MultiplicationToken, DivisionToken, LogicAndToken)):
                    valid_factor = False
                
            return factor
        else:
            raise SyntaxError("Error on parseTerm")



    @staticmethod
    def parseFactor() -> Node:
        if isinstance(Parser.tokenizer.next, NumberToken):
            return IntVal(value=Parser.tokenizer.next.value)
        
        elif isinstance(Parser.tokenizer.next, StringToken):
            return StrVal(value=Parser.tokenizer.next.value)
        
        elif isinstance(Parser.tokenizer.next, PlusToken):
            Parser.tokenizer.selectNext()
            factor = Parser.parseFactor()
            return UnOp(value="+", children=[factor])
        
        elif isinstance(Parser.tokenizer.next, MinusToken):
            Parser.tokenizer.selectNext()
            factor = Parser.parseFactor()
            return UnOp(value="-", children=[factor])
        
        elif isinstance(Parser.tokenizer.next, LeftParenthesisToken):
            rel_expression = Parser.parseRelExpression()
            if isinstance(Parser.tokenizer.next, RightParenthesisToken):
                return rel_expression
            raise SyntaxError("An opened parenthesis must be closed.")

        elif isinstance(Parser.tokenizer.next, IdentifierToken):
            return IdentifierNode(Parser.tokenizer.next._value)

        elif isinstance(Parser.tokenizer.next, DenialToken):
            Parser.tokenizer.selectNext()
            factor = Parser.parseFactor()
            return UnOp(value="!", children=[factor])
        
        elif isinstance(Parser.tokenizer.next, ReadlineToken):
            read_line = ReadlineNode()
            Parser.tokenizer.selectNext()
            if isinstance(Parser.tokenizer.next, LeftParenthesisToken):
                Parser.tokenizer.selectNext()
                if isinstance(Parser.tokenizer.next, RightParenthesisToken):
                    return read_line
                else:
                    raise SyntaxError("You must close an opened parenthesis on a readline function.")
            else:
                raise SyntaxError("After declare a readline function, you must use an open parenthesis.")
        
        else:
            raise SyntaxError("Error on parseFactor!")


    @staticmethod
    def parseStatement() -> Node:
        statement = None
        
        if is_statement_token(Parser.tokenizer.next):
            if isinstance(Parser.tokenizer.next, BreakLineToken):
                return NoOp()
            
            elif isinstance(Parser.tokenizer.next, IdentifierToken):
                identifier_node = IdentifierNode(Parser.tokenizer.next._value)
                
                Parser.tokenizer.selectNext()
                
                if isinstance(Parser.tokenizer.next, EqualsToken):
                    statement = AssignmentNode()
                    rel_expression_node = Parser.parseRelExpression()
                    
                    statement.children.append(identifier_node)
                    statement.children.append(rel_expression_node)
                
                elif isinstance(Parser.tokenizer.next, VariableDeclarationToken):
                    Parser.tokenizer.selectNext()
                    
                    if not isinstance(Parser.tokenizer.next, (IntegerTypeToken, StringTypeToken)):
                        raise SyntaxError(f"After declare a variable, you must use a type. Token found: {Parser.tokenizer.next._value}")
                    
                    statement = VariableDeclarationNode(Parser.tokenizer.next._value)
                    statement.children.append(identifier_node)
                    Parser.tokenizer.selectNext()
                    
                    # Declaração de variável com atribuição
                    if isinstance(Parser.tokenizer.next, EqualsToken):
                        rel_expression_node = Parser.parseRelExpression()
                        statement.children.append(rel_expression_node)
                else:
                    raise SyntaxError(f"Invalid token after identifier: {Parser.tokenizer.next._value}")
            
            elif isinstance(Parser.tokenizer.next, PrintlnToken):
                statement = PrintlnNode()

                Parser.tokenizer.selectNext()

                if isinstance(Parser.tokenizer.next, LeftParenthesisToken):
                    rel_expression_node = Parser.parseRelExpression()
                    if isinstance(Parser.tokenizer.next, RightParenthesisToken):
                        statement.children.append(rel_expression_node)
                        Parser.tokenizer.selectNext()
                    else:
                        raise SyntaxError("You must close an opened parenthesis on the println invocation.")
                else:
                    raise SyntaxError("An opening parenthesis is missing on println call.")
                
            elif isinstance(Parser.tokenizer.next, WhileToken):
                statement = WhileNode()
                
                rel_expression_node = Parser.parseRelExpression()
                statement.children.append(rel_expression_node)

                if isinstance(Parser.tokenizer.next, BreakLineToken):
                    Parser.tokenizer.selectNext()
                    block = BlockNode()

                    while is_statement_token(Parser.tokenizer.next):
                        statement_loop = Parser.parseStatement()
                        block.children.append(statement_loop)
                        Parser.tokenizer.selectNext()
                    
                    if isinstance(Parser.tokenizer.next, EndIfToken):
                        Parser.tokenizer.selectNext()
                        statement.children.append(block)
                    else:
                        raise SyntaxError(f"You must finish a while looping with 'end'. Received: {Parser.tokenizer.next._value}")
                else:
                    raise SyntaxError(f"After while conditional you must use a break line token. Received: {Parser.tokenizer.next._value}", )


            elif isinstance(Parser.tokenizer.next, IfToken):
                statement = ConditionalNode("if")

                rel_expression_node = Parser.parseRelExpression()
                statement.children.append(rel_expression_node)

                if isinstance(Parser.tokenizer.next, BreakLineToken):
                    Parser.tokenizer.selectNext()
                    block = BlockNode()

                    while is_statement_token(Parser.tokenizer.next):
                        statement_loop = Parser.parseStatement()
                        block.children.append(statement_loop)
                        Parser.tokenizer.selectNext()

                    statement.children.append(block)
                    
                    # Após statement, pode vir ou não um 'else', seguindo do 'end'.
                    if isinstance(Parser.tokenizer.next, ElseToken):
                        else_statement = ConditionalNode("else")

                        Parser.tokenizer.selectNext()

                        if isinstance(Parser.tokenizer.next, BreakLineToken):
                            Parser.tokenizer.selectNext()

                            while is_statement_token(Parser.tokenizer.next):
                                else_statement_loop = Parser.parseStatement()
                                else_statement.children.append(else_statement_loop)
                                Parser.tokenizer.selectNext()

                            statement.children.append(else_statement)
                        else:
                            raise SyntaxError(f"After 'else' conditional you must use a break line token. Received: {Parser.tokenizer.next._value}")
                    
                    # Após ou não o 'else', vem o 'end'
                    if isinstance(Parser.tokenizer.next, EndIfToken):
                        Parser.tokenizer.selectNext()
                    else:
                        raise SyntaxError(f"You must finish a 'if' looping with 'end'. Received: {Parser.tokenizer.next._value}")
                else:
                    raise SyntaxError(f"You must finish an 'if' conditional with '\\n'. Token found: {Parser.tokenizer.next._value}")
            if isinstance(Parser.tokenizer.next, BreakLineToken):
                return statement
            raise SyntaxError(f"A statement must to finish with '\\n'. Token found: {Parser.tokenizer.next._value}")

        else:
            raise SyntaxError(f"Invalid token in parseStatement: {Parser.tokenizer.next._value}")


    @staticmethod
    def parseBlock() -> Node:
        node_master = BlockNode()
        
        Parser.tokenizer.selectNext()
        token = Parser.tokenizer.next

        if (isinstance(token, (IdentifierToken, PrintlnToken, BreakLineToken))):
            while not (isinstance(token, EndOfFileToken)):
                statement = Parser.parseStatement()
                node_master.children.append(statement)
                Parser.tokenizer.selectNext()
                token = Parser.tokenizer.next
        else:
            raise SyntaxError(f"Invalid first token: {token._value}")
        
        return node_master

        


    @staticmethod
    def run(code) -> int:
        remove_comments = PrePro.filter(text=code)
        code_processed = PrePro.add_eof(text=remove_comments)
        
        Parser.tokenizer = Tokenizer(source=code_processed)

        result = Parser.parseBlock()
        result.evaluate()

        if isinstance(Parser.tokenizer.next, EndOfFileToken):
            return result
        raise SyntaxError("Where is EOF?")