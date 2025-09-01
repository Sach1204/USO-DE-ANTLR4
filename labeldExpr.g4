grammar labeldExpr;

prog:   stat+ ;

stat:   expr NEWLINE                # printExpr
    |   ID '=' expr NEWLINE         # assign
    |   NEWLINE                     # blank
    ;

expr
    : expr '^' expr                 # Pow
    | expr op=('*'|'/') expr        # MulDiv
    | expr op=('+'|'-') expr        # AddSub
    | expr '!'                      # Fact
    | '-' expr                      # UnaryMinus
    | ID '(' (expr)? ')'            # Function
    | INT                           # Int
    | DOUBLE                        # Double
    | ID                            # Id
    | '(' expr ')'                  # Parens
    ;

MUL : '*' ;
DIV : '/' ;
ADD : '+' ;
SUB : '-' ;
POW : '^' ;

ID  : [a-zA-Z]+ ;
INT : [0-9]+ ;
DOUBLE: [0-9]+'.'[0-9]+ ;

NEWLINE:'\r'? '\n' ;
WS  : [ \t]+ -> skip ;

