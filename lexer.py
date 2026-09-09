class Token:
    def __init__(self, type_, value, line):
        self.type = type_
        self.value = value
        self.line = line

    def __repr__(self):
        return f"Token({self.type}, {self.value!r}, line={self.line})"


KEYWORDS = {
    "let", "fun", "return", "if", "else", "elif", "while", "for", "in",
    "true", "false", "null", "and", "or", "not", "break", "continue",
    "import", "from", "as", "class", "new", "this", "do", "switch", "case", "default",
}

# Hindi-style keyword aliases -> map to the SAME token type as their English
# equivalent, so the parser needs no changes for these to work.
HINDI_ALIASES = {
    "maano": "LET",
    "kaam": "FUN",
    "vapas": "RETURN",
    "agar": "IF",
    "nahito": "ELSE",
    "nahito_agar": "ELIF",
    "jabtak": "WHILE",
    "pratyek": "FOR",
    "mein": "IN",
    "sahi": "TRUE",
    "galat": "FALSE",
    "khaali": "NULL",
    "aur": "AND",
    "ya": "OR",
    "nahi": "NOT",
    "roko": "BREAK",
    "jaari": "CONTINUE",
    "varg": "CLASS",
    "naya": "NEW",
    "yeh": "THIS",
    "karo": "DO",
    "vibhag": "SWITCH",
    "sthiti": "CASE",
    "anyatha": "DEFAULT",
    "aayat": "IMPORT",
    "se": "FROM",
    "ke_roop_mein": "AS",
}

# Multi-character operators must be listed before single-character ones
SYMBOLS = [
    ("==", "EQEQ"), ("!=", "NEQ"), ("<=", "LE"), (">=", "GE"),
    ("->", "ARROW"), ("+=", "PLUSEQ"), ("-=", "MINUSEQ"),
    ("*=", "STAREQ"), ("/=", "SLASHEQ"), ("**=", "STARSTAREQ"), ("**", "STARSTAR"),
    ("+", "PLUS"), ("-", "MINUS"), ("*", "STAR"), ("/", "SLASH"),
    ("%", "PERCENT"), ("=", "EQ"), ("<", "LT"), (">", "GT"),
    ("(", "LPAREN"), (")", "RPAREN"), ("{", "LBRACE"), ("}", "RBRACE"),
    ("[", "LBRACKET"), ("]", "RBRACKET"), (",", "COMMA"), (":", "COLON"),
    (";", "SEMI"), (".", "DOT"),
]


class LexError(Exception):
    def __init__(self, message, line):
        super().__init__(f"[Line {line}] Lexer Error: {message}")
        self.line = line


class Lexer:
    def __init__(self, source):
        self.source = source
        self.pos = 0
        self.line = 1
        self.tokens = []

    def peek(self, offset=0):
        idx = self.pos + offset
        if idx < len(self.source):
            return self.source[idx]
        return ""

    def advance(self):
        ch = self.source[self.pos]
        self.pos += 1
        if ch == "\n":
            self.line += 1
        return ch

    def tokenize(self):
        while self.pos < len(self.source):
            ch = self.peek()

            # Skip whitespace
            if ch in " \t\r\n":
                self.advance()
                continue

            # Skip comments (// line comments)
            if ch == "/" and self.peek(1) == "/":
                while self.pos < len(self.source) and self.peek() != "\n":
                    self.advance()
                continue

            # Skip block comments (/* ... */)
            if ch == "/" and self.peek(1) == "*":
                self.advance(); self.advance()
                while self.pos < len(self.source) and not (self.peek() == "*" and self.peek(1) == "/"):
                    self.advance()
                if self.pos < len(self.source):
                    self.advance(); self.advance()
                continue

            # F-strings (check for f before string)
            if (ch == 'f' or ch == 'F') and (self.peek(1) == '"' or self.peek(1) == "'"):
                self.tokens.append(self.read_fstring(ch))
                continue

            # Strings
            if ch == '"' or ch == "'":
                self.tokens.append(self.read_string(ch))
                continue

            # Numbers
            if ch.isdigit():
                self.tokens.append(self.read_number())
                continue

            # Identifiers / keywords
            if ch.isalpha() or ch == "_":
                self.tokens.append(self.read_identifier())
                continue

            # Symbols / operators
            matched = False
            for sym, name in SYMBOLS:
                if self.source[self.pos:self.pos+len(sym)] == sym:
                    line = self.line
                    for _ in sym:
                        self.advance()
                    self.tokens.append(Token(name, sym, line))
                    matched = True
                    break
            if matched:
                continue

            raise LexError(f"Unexpected character {ch!r}", self.line)

        self.tokens.append(Token("EOF", None, self.line))
        return self.tokens

    def read_string(self, quote):
        line = self.line
        self.advance()  # consume opening quote
        result = []
        while self.pos < len(self.source) and self.peek() != quote:
            ch = self.advance()
            if ch == "\\":
                esc = self.advance()
                escapes = {"n": "\n", "t": "\t", "\\": "\\", '"': '"', "'": "'"}
                result.append(escapes.get(esc, esc))
            else:
                result.append(ch)
        if self.pos >= len(self.source):
            raise LexError("Unterminated string literal", line)
        self.advance()  # consume closing quote
        return Token("STRING", "".join(result), line)

    def read_fstring(self, f_char):
        line = self.line
        self.advance()  # consume 'f' or 'F'
        quote = self.peek()
        self.advance()  # consume opening quote
        result = []
        expressions = []
        in_expr = False
        expr_start = 0
        brace_count = 0
        
        while self.pos < len(self.source) and self.peek() != quote:
            ch = self.advance()
            
            if ch == "\\":
                esc = self.advance()
                escapes = {"n": "\n", "t": "\t", "\\": "\\", '"': '"', "'": "'"}
                result.append(escapes.get(esc, esc))
            elif ch == "{":
                if in_expr:
                    brace_count += 1
                    result.append(ch)
                else:
                    in_expr = True
                    brace_count = 1
                    expr_start = len(result)
            elif ch == "}":
                if in_expr:
                    brace_count -= 1
                    if brace_count == 0:
                        # End of expression
                        expr_text = "".join(result[expr_start:])
                        expressions.append(expr_text)
                        result = result[:expr_start]  # Remove the expression from result
                        result.append("{}")  # Placeholder for later substitution
                        in_expr = False
                    else:
                        result.append(ch)
                else:
                    result.append(ch)
            else:
                result.append(ch)
        
        if self.pos >= len(self.source):
            raise LexError("Unterminated f-string literal", line)
        self.advance()  # consume closing quote
        
        return Token("FSTRING", ("".join(result), expressions), line)

    def read_number(self):
        line = self.line
        start = self.pos
        is_float = False
        while self.pos < len(self.source) and self.peek().isdigit():
            self.advance()
        if self.peek() == "." and self.peek(1).isdigit():
            is_float = True
            self.advance()
            while self.pos < len(self.source) and self.peek().isdigit():
                self.advance()
        text = self.source[start:self.pos]
        value = float(text) if is_float else int(text)
        return Token("FLOAT" if is_float else "INT", value, line)

    def read_identifier(self):
        line = self.line
        start = self.pos
        while self.pos < len(self.source) and (self.peek().isalnum() or self.peek() == "_"):
            self.advance()
        text = self.source[start:self.pos]
        if text in HINDI_ALIASES:
            return Token(HINDI_ALIASES[text], text, line)
        if text in KEYWORDS:
            return Token(text.upper(), text, line)
        return Token("IDENT", text, line)


def tokenize(source):
    return Lexer(source).tokenize()