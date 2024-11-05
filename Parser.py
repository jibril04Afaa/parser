import ASTNodeDefs as AST


class Lexer:
    def __init__(self, code):
        self.code = code
        self.position = 0
        self.current_char = self.code[self.position]
        self.tokens = []

    # Move to the next position in the code.
    def advance(self):
        # TODO: Students need to complete the logic to advance the position.
        self.position += 1
        if self.position < len(self.code):
            self.current_char = self.code[self.position]
        else:
            self.current_char = None

    # Skip whitespaces.
    def skip_whitespace(self):
        # TODO: Complete logic to skip whitespaces.
        while self.current_char is not None:
            if self.current_char.isspace():
                self.advance()
            else:
                break

    # Tokenize an identifier.
    def identifier(self):
        result = ''
        # TODO: Complete logic for handling identifiers.
        while self.current_char is not None and self.current_char.isalnum():
            result += self.current_char
            self.advance()
        return ('IDENTIFIER', result)

    # Tokenize a number.
    def number(self):
        result = ''
        # TODO: Implement logic to tokenize numbers.
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return ('NUMBER', int(result))

    def token(self):
        # skip whitespace
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            if self.current_char.isalpha():
                ident = self.identifier()
                if ident[1] == 'if':
                    return ('IF', 'if')
                elif ident[1] == 'else':
                    return ('ELSE', 'else')
                elif ident[1] == 'while':
                    return ('WHILE', 'while')
                return ident
            if self.current_char.isdigit():
                return self.number()

            # TODO: Add logic for operators and punctuation tokens.
            # equals to
            if self.current_char == '=':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return ('EQUALS', '==')
                return ('ASSIGN', '=')

            # not equals to
            if self.current_char == '!':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return ('NEQ', '!=')
                raise ValueError("Expected '=' after '!' ")

            # plus
            if self.current_char == '+':
                self.advance()
                return ('PLUS', '+')

            # minus
            if self.current_char == '-':
                self.advance()
                return ('MINUS', '-')

            # multiply
            if self.current_char == '*':
                self.advance()
                return ('MULTIPLY', '*')

            # divide
            if self.current_char == '/':
                self.advance()
                return ('DIVIDE', '/')

            # left parantheses
            if self.current_char == '(':
                self.advance()
                return ('LPAREN', '(')

            # right parantheses
            if self.current_char == ')':
                self.advance()
                return ('RPAREN', ')')

            # less than
            if self.current_char == '<':
                self.advance()
                return ('LESS', '<')

            # greater than
            if self.current_char == '>':
                self.advance()
                return ('GREATER', '>')

            raise ValueError(f"Illegal character at position {self.position}: {self.current_char}")

        return ('EOF', None)

    # Collect all tokens into a list.
    def tokenize(self):
        # TODO: Implement the logic to collect tokens.
        self.tokens = []

        while True:
            a_token = self.token()

            if a_token[0] == 'EOF':
                self.tokens.append(a_token)
                break

            self.tokens.append(a_token)
        return self.tokens


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = tokens.pop(0)  # Start with the first token

    def advance(self):
        # Move to the next token in the list.
        # TODO: Ensure the parser doesn't run out of tokens.
        if self.tokens:
            self.current_token = self.tokens.pop(0)
            return True
        else:
            self.current_token = ('EOF', None)

    def parse(self):
        """
        Entry point for the parser. It will process the entire program.
        TODO: Implement logic to parse multiple statements and return the AST for the entire program.
        """
        return self.program()

    def program(self):
        """
        Program consists of multiple statements.
        TODO: Loop through and collect statements until EOF is reached.
        """
        statements = []
        while self.current_token[0] != 'EOF':
            #TODO: Parse each statement and append it to the list.
            statements.append(self.statement())

        # TODO: Return an AST node that represents the program.
        return self.statement()

    def statement(self):
        """
        Determines which type of statement to parse.
        - If it's an identifier, it could be an assignment or function call.
        - If it's 'if', it parses an if-statement.
        - If it's 'while', it parses a while-statement.

        TODO: Dispatch to the correct parsing function based on the current token.
        """
        if self.current_token[0] == 'EOF':
            return None
        if self.current_token[0] == 'IDENTIFIER':
            if self.peek() == 'EQUALS':  # Assignment
                return self.assign_stmt()  #AST of assign_stmt
            elif self.peek() == 'LPAREN':  # Function call
                return self.function_call()  #AST of function call
            else:
                raise ValueError(f"Unexpected token after identifier: {self.current_token}")
        elif self.current_token[0] == 'IF':
            return self.if_stmt()  #AST of if stmt
        elif self.current_token[0] == 'WHILE':
            return self.while_stmt()  #AST of while stmt
        else:
            # TODO: Handle additional statements if necessary.
            raise ValueError(f"Unexpected token: {self.current_token}")

    def assign_stmt(self):
        """
        Parses assignment statements.
        Example:
        x = 5 + 3
        TODO: Implement parsing for assignments, where an identifier is followed by '=' and an expression.
        """
        identifier = self.current_token()
        self.advance()
        self.expect('EQUALS')

        expression = self.expression()

        return AST.Assignment(identifier, expression)

    def if_stmt(self):
        """
        Parses an if-statement, with an optional else block.
        Example:
        if condition:
            # statements
        else:
            # statements
        TODO: Implement the logic to parse the if condition and blocks of code.
        """
        # expects an 'if' keyword
        self.expect('IF')
        condition = self.boolean_expression()

        # expects a colon after 'if'
        self.expect('COLON')

        # parse true block
        true_block = self.block()
        false_block = None

        # parse else block
        if self.current_token[0] == 'ELSE':
            self.advance()
            self.expect('COLON')
            false_block = self.block()

        return AST.IfStatement(condition, true_block, false_block)

    def while_stmt(self):
        """
        Parses a while-statement.
        Example:
        while condition:
            # statements
        TODO: Implement the logic to parse while loops with a condition and a block of statements.
        """
        # expects a 'while' keyword
        self.expect('WHILE')
        condition = self.boolean_expression()
        # expects a colon after 'while'
        self.expect('COLON')
        # parse block
        block = self.block()
        return AST.WhileStatement(condition, block)

    def block(self):
        """
        Parses a block of statements. A block is a collection of statements grouped by indentation.
        Example:
        if condition:
            # This is a block
            x = 5
            y = 10
        TODO: Implement logic to capture multiple statements as part of a block.
        """
        statements = []
        # write your code here
        while self.current_token[0] not in ['EOF', 'ELSE']:
            statements.append(self.statement())
        return AST.Block(statements)

    def expression(self):
        """
        Parses an expression. Handles operators like +, -, etc.
        Example:
        x + y - 5
        TODO: Implement logic to parse binary operations (e.g., addition, subtraction) with correct precedence.
        """
        left = self.term()  # Parse the first term
        while self.current_token[0] in ['PLUS', 'MINUS']:  # Handle + and -
            op = self.current_token  # Capture the operator
            self.advance()  # Skip the operator
            right = self.term()  # Parse the next term
            left = AST.BinaryOperation(left, op, right)

        return left

    def boolean_expression(self):
        """
        Parses a boolean expression. These are comparisons like ==, !=, <, >.
        Example:
        x == 5
        TODO: Implement parsing for boolean expressions.
        """
        # write your code here, for reference check expression function
        left = self.expression()
        if self.current_token[0] in ['EQUALS', 'NEQ', 'LESS', 'GREATER']:
            operator = self.current_token
            self.advance()

            right = self.expression()
            return AST.BooleanExpression(left, operator, right)
        else:
            return left

    def term(self):
        """
        Parses a term. A term consists of factors combined by * or /.
        Example:
        x * y / z
        TODO: Implement the parsing for multiplication and division.
        """
        # write your code here, for reference check expression function
        left = self.factor()
        while self.current_token[0] in ['MULTIPLY', 'DIVIDE']:
            op = self.current_token
            self.advance()
            right = self.factor()
            left = AST.BinaryOperation(left, op, right)
        return left

    def factor(self):
        """
        Parses a factor. Factors are the basic building blocks of expressions.
        Example:
        - A number
        - An identifier (variable)
        - A parenthesized expression
        TODO: Handle these cases and create appropriate AST nodes.
        """
        token_type, token_value = self.current_token

        # number
        if self.current_token[0] == 'NUMBER':
            self.advance()
            return AST.ASTNode(token_value)

        # identifier
        elif self.current_token[0] == 'IDENTIFIER':
            self.advance()
            AST.ASTNode(token_value)

        # a paranthesized expression
        elif self.current_token[0] == 'LPAREN':
            self.advance()
            result = self.expression()
            self.expect('RPAREN')
            return result

        # unexpected tokens
        else:
            raise ValueError(f"Unexpected token in factor: {self.current_token}")

    def function_call(self):
        """
        Parses a function call.
        Example:
        myFunction(arg1, arg2)
        TODO: Implement parsing for function calls with arguments.
        """

        self.advance()

        # parse opening parantheses
        self.expect('LPAREN')

        # parse arguments
        args = []
        if self.current_token[0] != 'RPAREN':
            args = self.arg_list()

        # parse closing parantheses
        self.expect('RPAREN')

        return AST.FunctionCall(self.current_token(), args)

    def arg_list(self):
        """
        Parses a list of arguments in a function call.
        Example:
        arg1, arg2, arg3
        TODO: Implement the logic to parse comma-separated arguments.
        """
        args = [self.expression()]

        while self.current_token[0] != 'COMMA':
            self.advance()
            args.append(self.expression())

        return args

    def expect(self, token_type):

        if self.current_token[0] == token_type:
            self.advance()  # Move to the next token
        else:
            raise ValueError(f"Expected {token_type} but got {self.current_token[0]}")

    def peek(self):
        if self.tokens:
            return self.tokens[0][0]
        else:
            return None
