# coding: utf-8
import ply.yacc as yacc
from lexer import tokens, lexer

def p_programa(p):
    "programa : DEF ID ':' '[' listacmd ']'"
    pass

# TODO : não reconhece pro def e pro ]
def p_programa_error(t):
    """programa : error ID ':' '[' listacmd ']'
    | DEF ID error '[' listacmd ']' 
    | DEF ID ':' error listacmd ']' 
    | DEF ID ':' '[' listacmd error """
    _generateError(t, {1:"def",3:":", 4:"[", 6:']'})
        
def p_empty(p):
    "empty :"
    pass
    
def p_listacmd(p):
    "listacmd : comando listacmd1"
    pass
    
def p_listacmd1(p):
    """listacmd1 : empty 
               | listacmd"""
    pass
    
def p_comando(p):
    """comando : cmdatribui
               | cmdentrada
               | cmdsaida
               | cmdselecao
               | cmdrepeticao"""
    pass

def p_listaidenti(p):
    "listaidenti : ID listaindenti1"
    pass

def p_listaindenti1(p):
    """listaindenti1 : empty
                     | ',' listaidenti"""
    pass
    
def p_listaindenti1_error(t):
    """listaindenti1 : error listaidenti"""
    _generateError(t, {1:","})
    
def p_listaexp(p):
    "listaexp : expressao listaexp1"
    pass

def p_listaexp1(p):
    """listaexp1 : ',' listaexp
                 | empty """
    pass

def p_listaexp1_error(t):
    """listaexp1 : error listaexp"""
    _generateError(t, {1:","})
    
def p_cmdatribui(p):
    "cmdatribui : listaidenti SIM_ATTR expressao ';'"
    pass

def p_cmdatribui_error(t):
    "cmdatribui : listaidenti SIM_ATTR expressao error"
    _generateError(t, {4:";"})


def p_cmdentrada(p):
    "cmdentrada : INPUT '(' listaidenti ')' ';'"
    pass
    
def p_cmdentrada_error(t):
    """cmdentrada : INPUT '(' listaidenti error ';' 
    | INPUT error listaidenti ')' ';' 
    | INPUT '(' listaidenti ')' error """
    _generateError(t, {2:"(",4:")", 5:";"})

def p_cmdsaida(p):
    "cmdsaida : OUTPUT '(' listaexp ')' ';'"
    pass

def p_cmdsaida_error(t):
    """cmdsaida : OUTPUT '(' listaexp error ';' 
    | OUTPUT error listaexp ')' ';' 
    | OUTPUT '(' listaexp ')' error    """
    erros = {2:"(",4:")", 5:";"}
    

def p_cmdselecao(p):
    "cmdselecao : IF expressao ':' '[' listacmd ']' elif else ';'"
    pass
    
def p_elif(p):
    """elif : empty 
            | ELIF expressao ':' '[' listacmd ']' elif"""
    pass

def p_else(p):
    """else : empty
            | ELSE ':' '[' listacmd ']'"""
    pass

def p_cmdrepeticao(p):
    "cmdrepeticao : WHILE expressao ':' '[' listacmd ']' else ';'"
    pass

def p_expressao(p):
    "expressao : valor expressao1"
    pass

def p_expressao1(p):
    """expressao1 : empty
                | OR valor expressao1
                | AND valor expressao1"""
    pass

def p_expressao1_error(t):
    """expressao1 : error valor expressao1"""    
    raise Exception(u"Erro na linha %s - encontrado %s, esperado AND ou OR" % (t.lineno, t.value))

def p_valor(p):
    """valor : relacional
           | TRUE
           | FALSE
           | NOT valor"""
    pass

def p_valor_error(t):
    """valor : error
           | error valor"""
    raise Exception(u"Erro na linha %s - encontrado %s, esperado TRUE, FALSE ou NOT" % (t.lineno, t.value))

def p_relacional(p):
    "relacional : aritmetica relacional1"
    pass

def p_relacional1(p):
    """relacional1 : operador aritmetica
                 | empty"""
    pass

def p_operador(p):
    """operador : SIM_EQ
              | SIM_DIF
              | '<'
              | SIM_LE
              | '>'
              | SIM_GE"""
    pass

def p_operador_error(t):
    """operador : error"""
    raise Exception(u"Erro na linha %s - encontrado %s, esperado operador lógico" % (t.lineno, t.value))

def p_aritmetica(p):
    "aritmetica : termo aritmetica1"
    pass
    
def p_aritmetica1(p):
    """aritmetica1 : empty
                   | '+' termo aritmetica1
                   | '-' termo aritmetica1"""
    pass

def p_termo(p):
    "termo : fator termo1"
    pass

def p_termo1(p):
    """termo1 : empty
              | '*' fator termo1
              | '/' fator termo1
              | '%' fator termo1"""
    pass

def p_fator(p):
    "fator : elemento fator1"
    pass
    
def p_fator1(p):
    """fator1 : empty
              | SIM_POT elemento fator1"""
    pass

def p_elemento(p):
    """elemento : ID
                | INTEIRO
                | REAL
                | LITERAL
                | '(' expressao ')'
                | '+' elemento
                | '-' elemento"""
    pass

def p_elemento_error(t):
  """elemento : error
              | error expressao error
              | error elemento"""
  raise Exception(u"Erro na linha %s - encontrado %s, esperado expressão" % (t.lineno, t.value))

def _getTokenValue(t):
    if not t:
        return "EOF"
    else:
        if type(t) is str:
            return t
        else:
            return t.value
            
def _generateError(t, dictionary):
    for k, v in dictionary.items():
        if _getTokenValue(t[k]) != v:
            raise Exception(u"Erro na linha %s - encontrado %s, esperado %s" % ('1', _getTokenValue(t[k]), v))
  

parser = yacc.yacc()