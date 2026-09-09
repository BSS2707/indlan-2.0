"""
IndLan Parser
A recursive-descent parser that converts tokens into an AST.
"""

from ast_nodes import *


class ParseError(Exception):
    def __init__(self, message, line):
        super().__init__(f"[Line {line}] Parse Error: {message}")
        self.line = line


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    # ---------- helpers ----------

    def peek(self, offset=0):
        idx = self.pos + offset
        if idx < len(self.tokens):
            return self.tokens[idx]
        return self.tokens[-1]  # EOF

    def advance(self):
        tok = self.tokens[self.pos]
        if self.pos < len(self.tokens) - 1:
            self.pos += 1
        return tok

    def check(self, type_):
        return self.peek().type == type_

    def match(self, *types):
        if self.peek().type in types:
            return self.advance()
        return None

    def expect(self, type_, msg=None):
        if self.check(type_):
            return self.advance()
        tok = self.peek()
        raise ParseError(msg or f"Expected {type_} but got {tok.type} ({tok.value!r})", tok.line)

    def skip_semis(self):
        while self.match("SEMI"):
            pass

    # ---------- entry point ----------

    def parse_program(self):
        statements = []
        self.skip_semis()
        while not self.check("EOF"):
            statements.append(self.statement())
            self.skip_semis()
        return Program(statements)

    # ---------- statements ----------

    def statement(self):
        if self.check("IMPORT"):
            return self.import_stmt()
        if self.check("FROM"):
            return self.from_import_stmt()
        if self.check("LET"):
            return self.let_stmt()
        if self.check("FUN"):
            return self.fun_decl()
        if self.check("IF"):
            return self.if_stmt()
        if self.check("WHILE"):
            return self.while_stmt()
        if self.check("DO"):
            return self.do_while_stmt()
        if self.check("SWITCH"):
            return self.switch_stmt()
        if self.check("FOR"):
            return self.for_stmt()
        if self.check("RETURN"):
            return self.return_stmt()
        if self.check("BREAK"):
            line = self.advance().line
            return BreakStmt(line)
        if self.check("CONTINUE"):
            line = self.advance().line
            return ContinueStmt(line)
        if self.check("CLASS"):
            return self.class_decl()
        if self.check("LBRACE"):
            return self.block()
        return self.expr_stmt()

    def import_stmt(self):
        line = self.advance().line  # 'import' or 'aayat'
        path_parts = [self.expect("IDENT").value]
        while self.match("DOT"):
            path_parts.append(self.expect("IDENT").value)
        module_path = ".".join(path_parts)
        alias = None
        if self.match("AS"):
            alias = self.expect("IDENT").value
        self.skip_semis()
        return ImportStmt(module_path, alias, line)

    def from_import_stmt(self):
        line = self.advance().line  # 'from' or 'se'
        path_parts = [self.expect("IDENT").value]
        while self.match("DOT"):
            path_parts.append(self.expect("IDENT").value)
        module_path = ".".join(path_parts)
        self.expect("IMPORT", "Expected 'import' or 'aayat' after module path in from-import")
        items = []
        item_name = self.expect("IDENT").value
        item_alias = None
        if self.match("AS"):
            item_alias = self.expect("IDENT").value
        items.append((item_name, item_alias))
        while self.match("COMMA"):
            item_name = self.expect("IDENT").value
            item_alias = None
            if self.match("AS"):
                item_alias = self.expect("IDENT").value
            items.append((item_name, item_alias))
        self.skip_semis()
        return FromImportStmt(module_path, items, line)

    def let_stmt(self):
        line = self.advance().line  # 'let'
        names = [self.expect("IDENT").value]
        while self.match("COMMA"):
            names.append(self.expect("IDENT").value)
        self.expect("EQ", "Expected '=' after variable name in let statement")
        value = self.expression()
        self.skip_semis()
        return LetStmt(names, value, line)

    def fun_decl(self):
        line = self.advance().line  # 'fun'
        name = self.expect("IDENT").value
        self.expect("LPAREN")
        params = []
        if not self.check("RPAREN"):
            params.append(self.expect("IDENT").value)
            while self.match("COMMA"):
                params.append(self.expect("IDENT").value)
        self.expect("RPAREN")
        body = self.block()
        return FunDecl(name, params, body, line)

    def class_decl(self):
        line = self.advance().line  # 'class'
        name = self.expect("IDENT").value
        self.expect("LBRACE")
        methods = []
        while not self.check("RBRACE") and not self.check("EOF"):
            self.skip_semis()
            if self.check("RBRACE"):
                break
            methods.append(self.fun_decl())
            self.skip_semis()
        self.expect("RBRACE")
        return ClassDecl(name, methods, line)

    def if_stmt(self):
        line = self.advance().line  # 'if'
        branches = []
        cond = self.expression()
        body = self.block()
        branches.append((cond, body))
        else_block = None
        while self.check("ELIF"):
            self.advance()
            cond2 = self.expression()
            body2 = self.block()
            branches.append((cond2, body2))
        if self.check("ELSE"):
            self.advance()
            else_block = self.block()
        return IfStmt(branches, else_block, line)

    def while_stmt(self):
        line = self.advance().line  # 'while'
        cond = self.expression()
        body = self.block()
        return WhileStmt(cond, body, line)

    def do_while_stmt(self):
        line = self.advance().line  # 'do'
        body = self.block()
        self.expect("WHILE", "Expected 'while' after 'do' block")
        cond = self.expression()
        self.skip_semis()
        return DoWhileStmt(body, cond, line)

    def switch_stmt(self):
        line = self.advance().line  # 'switch'
        subject = self.expression()
        self.expect("LBRACE")
        cases = []
        default_block = None
        self.skip_semis()
        while self.check("CASE"):
            self.advance()
            value = self.expression()
            body = self.block()
            cases.append((value, body))
            self.skip_semis()
        if self.check("DEFAULT"):
            self.advance()
            default_block = self.block()
            self.skip_semis()
        self.expect("RBRACE", "Expected '}' to close switch")
        return SwitchStmt(subject, cases, default_block, line)

    def for_stmt(self):
        line = self.advance().line  # 'for'
        var_name = self.expect("IDENT").value
        self.expect("IN")
        iterable = self.expression()
        body = self.block()
        return ForStmt(var_name, iterable, body, line)

    def return_stmt(self):
        line = self.advance().line  # 'return'
        value = None
        if not self.check("SEMI") and not self.check("RBRACE") and not self.check("EOF"):
            value = self.expression()
        self.skip_semis()
        return ReturnStmt(value, line)

    def block(self):
        line = self.expect("LBRACE").line
        statements = []
        self.skip_semis()
        while not self.check("RBRACE") and not self.check("EOF"):
            statements.append(self.statement())
            self.skip_semis()
        self.expect("RBRACE", "Expected '}' to close block")
        return Block(statements, line)

    def expr_stmt(self):
        line = self.peek().line
        expr = self.logic_or()
        if self.match("COMMA"):
            targets = [expr]
            targets.append(self.logic_or())
            while self.match("COMMA"):
                targets.append(self.logic_or())
            if self.peek().type in ("EQ", "PLUSEQ", "MINUSEQ", "STAREQ", "SLASHEQ", "STARSTAREQ"):
                op_tok = self.advance()
                value = self.expression()
                for t in targets:
                    if not isinstance(t, (Identifier, Index, GetAttr)):
                        raise ParseError("Invalid assignment target in multi-target assignment", op_tok.line)
                self.skip_semis()
                return ExprStmt(Assign(targets, value, op_tok.line, "="), line)
            raise ParseError("Expected assignment operator after target list", line)
        if self.peek().type in ("EQ", "PLUSEQ", "MINUSEQ", "STAREQ", "SLASHEQ", "STARSTAREQ"):
            op_tok = self.advance()
            value = self.expression()
            if not isinstance(expr, (Identifier, Index, GetAttr)):
                raise ParseError("Invalid assignment target", op_tok.line)
            op_map = {"EQ": "=", "PLUSEQ": "+=", "MINUSEQ": "-=", "STAREQ": "*=", "SLASHEQ": "/=", "STARSTAREQ": "**="}
            self.skip_semis()
            return ExprStmt(Assign(expr, value, op_tok.line, op_map[op_tok.type]), line)
        self.skip_semis()
        return ExprStmt(expr, line)

    # ---------- expressions (precedence climbing) ----------

    def expression(self):
        return self.assignment()

    def assignment(self):
        expr = self.logic_or()
        if self.peek().type in ("EQ", "PLUSEQ", "MINUSEQ", "STAREQ", "SLASHEQ", "STARSTAREQ"):
            op_tok = self.advance()
            value = self.assignment()
            if not isinstance(expr, (Identifier, Index, GetAttr)):
                raise ParseError("Invalid assignment target", op_tok.line)
            op_map = {"EQ": "=", "PLUSEQ": "+=", "MINUSEQ": "-=", "STAREQ": "*=", "SLASHEQ": "/=", "STARSTAREQ": "**="}
            return Assign(expr, value, op_tok.line, op_map[op_tok.type])
        return expr

    def logic_or(self):
        expr = self.logic_and()
        while self.check("OR"):
            line = self.advance().line
            right = self.logic_and()
            expr = LogicalOp("or", expr, right, line)
        return expr

    def logic_and(self):
        expr = self.equality()
        while self.check("AND"):
            line = self.advance().line
            right = self.equality()
            expr = LogicalOp("and", expr, right, line)
        return expr

    def equality(self):
        expr = self.comparison()
        while self.peek().type in ("EQEQ", "NEQ"):
            op = self.advance()
            right = self.comparison()
            expr = BinOp(op.value, expr, right, op.line)
        return expr

    def comparison(self):
        expr = self.term()
        while self.peek().type in ("LT", "GT", "LE", "GE"):
            op = self.advance()
            right = self.term()
            expr = BinOp(op.value, expr, right, op.line)
        return expr

    def term(self):
        expr = self.factor()
        while self.peek().type in ("PLUS", "MINUS"):
            op = self.advance()
            right = self.factor()
            expr = BinOp(op.value, expr, right, op.line)
        return expr

    def factor(self):
        expr = self.exponentiation()
        while self.peek().type in ("STAR", "SLASH", "PERCENT"):
            op = self.advance()
            right = self.exponentiation()
            expr = BinOp(op.value, expr, right, op.line)
        return expr

    def exponentiation(self):
        expr = self.unary()
        if self.check("STARSTAR"):
            op = self.advance()
            right = self.exponentiation()  # Right-associative
            expr = BinOp(op.value, expr, right, op.line)
        return expr

    def unary(self):
        if self.peek().type in ("MINUS", "NOT"):
            op = self.advance()
            operand = self.unary()
            return UnaryOp(op.value, operand, op.line)
        return self.call_or_postfix()

    def parse_call_arg(self):
        line = self.peek().line
        if self.check("IDENT") and self.peek(1).type == "EQ":
            name = self.advance().value
            self.advance()  # consume '='
            val = self.expression()
            return KeywordArg(name, val, line)
        return self.expression()

    def call_or_postfix(self):
        expr = self.primary()
        while True:
            if self.check("LPAREN"):
                line = self.advance().line
                args = []
                if not self.check("RPAREN"):
                    args.append(self.parse_call_arg())
                    while self.match("COMMA"):
                        if self.check("RPAREN"):
                            break
                        args.append(self.parse_call_arg())
                self.expect("RPAREN")
                expr = Call(expr, args, line)
            elif self.check("LBRACKET"):
                line = self.advance().line
                idx = self.expression()
                self.expect("RBRACKET")
                expr = Index(expr, idx, line)
            elif self.check("DOT"):
                line = self.advance().line
                name = self.expect("IDENT").value
                expr = GetAttr(expr, name, line)
            else:
                break
        return expr

    def primary(self):
        tok = self.peek()

        if tok.type == "INT" or tok.type == "FLOAT":
            self.advance()
            return NumberLit(tok.value, tok.line)

        if tok.type == "STRING":
            self.advance()
            return StringLit(tok.value, tok.line)

        if tok.type == "TRUE":
            self.advance()
            return BoolLit(True, tok.line)

        if tok.type == "FALSE":
            self.advance()
            return BoolLit(False, tok.line)

        if tok.type == "NULL":
            self.advance()
            return NullLit(tok.line)

        if tok.type == "THIS":
            self.advance()
            return Identifier("this", tok.line)

        if tok.type == "IDENT":
            self.advance()
            return Identifier(tok.value, tok.line)

        if tok.type == "LPAREN":
            self.advance()
            expr = self.expression()
            self.expect("RPAREN")
            return expr

        if tok.type == "LBRACKET":
            self.advance()
            elements = []
            if not self.check("RBRACKET"):
                elements.append(self.expression())
                while self.match("COMMA"):
                    elements.append(self.expression())
            self.expect("RBRACKET")
            return ListLit(elements, tok.line)

        if tok.type == "LBRACE":
            # dict literal: { key: value, ... }
            self.advance()
            pairs = []
            if not self.check("RBRACE"):
                k = self.expression()
                self.expect("COLON")
                v = self.expression()
                pairs.append((k, v))
                while self.match("COMMA"):
                    k2 = self.expression()
                    self.expect("COLON")
                    v2 = self.expression()
                    pairs.append((k2, v2))
            self.expect("RBRACE")
            return DictLit(pairs, tok.line)

        if tok.type == "NEW":
            self.advance()
            class_name = self.expect("IDENT").value
            self.expect("LPAREN")
            args = []
            if not self.check("RPAREN"):
                args.append(self.parse_call_arg())
                while self.match("COMMA"):
                    if self.check("RPAREN"):
                        break
                    args.append(self.parse_call_arg())
            self.expect("RPAREN")
            return Call(Identifier(class_name, tok.line), args, tok.line)

        raise ParseError(f"Unexpected token {tok.type} ({tok.value!r})", tok.line)


def parse(tokens):
    return Parser(tokens).parse_program()