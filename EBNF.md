# Brah EBNF Grammar Specification


```ebnf

module: declaration*

declaration: importdecl
    | constantdecl
    | enumerationdecl
    | exceptiondecl
    | signaturedecl
    | functiondecl
    | structuredecl
    | classdecl
    | interfacedecl
    | singletondecl

importdecl: 'importe' [ ( NAME | multinames ) 'de' ] ( FILEPATH | qualifiedname ) ';'
multinames: '{' NAME ( ',' NAME )* '}'
qualifiedname: NAME ( '.' NAME )+

constantdecl: [ 'exporte' ] 'constante' NAME '=' constexpr ';'

enumerationdecl: [ 'exporte' ] 'enumeração' NAME [ ':' TYPENAME ] enumblock
enumblock: '{' NAME [ '=' constexpr ] ( ',' NAME [ '=' constexpr ] )* '}'

expectiondecl: [ 'exporte' ] 'exceção' NAME ':' NAME ';'

signaturedecl: [ 'exporte' ] 'assinatura' NAME paramtypelist ':' TYPENAME ';'
paramtypelist: '(' [ TYPENAME ( ',' TYPENAME )* ] ')'

functiondecl: [ templatedecl ] [ 'exporte' ] função NAME paramlist ':' TYPENAME functionblock
paramlist: '(' [ parameterdecl ( ',' parameterdecl )* ] ')'
parameterdecl: NAME ':' TYPENAME [ '=' constexpr ]

templatedecl: 'modelo' typenames
typenames: '<' typename ( ',' typename )* '>'
typename: 'tipo' ':' NAME
    | TYPENAME ':' NAME

structuredecl: [ templatedecl ] [ 'exporte' ] 'estrutura' NAME declblock

classdecl: [ templatedecl ] [ 'exporte' ] 'classe' [ 'abstrata' ] NAME [ implements ] [ inherits ] declblock
implements: 'implementa' TYPENAME ( ',' TYPENAME )
inherits: 'extende' TYPENAME

interfacedecl: [ 'exporte' ] 'interface' NAME declblock

singletondecl: [ 'exporte' ] 'singular' NAME declblock

functionblock: '{' ( assignment | statement )* '}'

declblock: '{' ( fielddecl | methoddecl | propertydecl | operatordecl )* '}'

fielddecl: identifiers ':' TYPENAME ';'
    | identifier ':' TYPENAME '=' expression ';'

identifiers: identifier [ ',' identifier ]
identifier: ( '*' )* NAME ( '[' [ expression ] ']' )*

methodecl: [ 'estático' ] [ ( 'protegido' | 'privado' ) ] NAME paramlist ':' TYPENAME methodblock

propertydecl: [ 'estático' ] [ ( 'protegido' | 'privado' ) ] NAME ':' TYPENAME propertyblock
propertyblock: '{' [ getstmt ] [ setstmt ] '}'
getstmt: 'leia' ( '{' getterblock '}' | expression ';' )
setstmt: 'escreva' ( '{' setterblock '}' | NAME (',' NAME ) ';' )

operatordecl: 'operador' OPERATOR paramlist ':' TYPENAME methodblock

statement: ifthenstmt
    | ifelsestmt
    | whilestmt
    | dowhilestmt
    | dountilstmt
    | repeatstmt
    | forstmt
    | foreachstmt
    | switchstmt
    | trystmt
    | breakstmt
    | continuestmt
    | returnstmt
    | assignment

block: '{' statement* '}'
test: '(' expression ')'
iteration: '(' [ starters ';' ] stoppers ';' steppers ')'
labeldef: ':' NAME

ifthenstmt: 'se' test block

ifelsestmt: ifthenstmt 'senão' block

whilestmt: 'enquanto' test [ labeldef ] block

dowhilestmt: 'faça' [ labeldef ] block 'enquanto' test

dountilstmt: 'faça' [ labeldef ] block 'até' test

repeatstmt: 'repita' [ target ] [ labeldef ] block

forstmt: 'para' iteration [ labeldef ] block

foreach: 'para '(' 'cada' element 'em' target ')' [ labeldef ] block

switchstmt: 'alterne' '(' target ')' [ labeldef ] '{' ( casestmt )+ [ defaultstmt ] '}' 
casestmt: 'caso' constexpr ':' block
defaultstmt: 'senão' ':' block

trystmt: 'tente' block ( 'exceto' NAME block )* [ 'enfim' block ]

continuestmt: 'continue' [ NAME ] ';'

breakstmt: 'pare' [ NAME ] ';'

returnstmt: 'retorne' [ expression | aggregate ] ';'

assignment: targets "=" ( expression | aggregate ) ';'
    | target ('+=' | '-=' | '*=' | '/=' | '%=' | &= | '|=' | '^=' | '~='| '<<=' | '>>=') expression ';'
    | target [ '++' | '--' ] ';'

targets: target
    | '{' (target | '...' ',' target) ( ',' ( target | '...' ) )* '}'

target: NAME ( subscript | arglist | '.' NAME )*

subscript: ( '[' expression ']' )+
arglist: '(' [ expression ( ',' expression ) ] ')'

expression : ternary
binaryor : binaryand ( 'ou' binaryand )*
ternary : expresson '?' expression ':' expression
binaryand : binarycomp ( 'e' binarycomp )*
binarycomp : binaryadd ( ('<' | '<=' | '==' | '!=' | '>=' | '>') binaryadd )*
binaryadd : binarymul ( ('+' | '-'| '|'| '^') binarymul )*
binarymul : unary ( ('*' | '/' | '%' | '&'| '<<'| '>>') unary )*
unary : ('--' | '++', '-' | '+') operand
operand : literal | target
literal : INT
        | FLOAT



```
