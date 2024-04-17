import ply.lex as lex
import ply.yacc as yacc
from flask import Flask, render_template, request

app = Flask(__name__)

# Lista de tokens
tokens = (
    'RESERVADA',
    'DOCTYPE',
    'IDENTIFICADOR',
    'MAYOR',
    'MENOR',
    'FIN',
)

# Expresiones regulares para tokens
t_RESERVADA = r'Mi|primer|Web|Hola|mundo|!'
t_DOCTYPE = r'DOCTYPE|html'
t_IDENTIFICADOR= r'HTML|head|title|body|h1'
t_MAYOR = r'\>'
t_MENOR = r'\<'
t_FIN = r'\/'

# Ignorar espacios y tabulaciones
t_ignore = ' \t'


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Error léxico: Carácter inesperado '{t.value[0]}' en la línea {t.lexer.lineno}")
    t.lexer.skip(1)

# Construir el analizador léxico
lexer = lex.lex()

# Regla de producción para el analizador sintáctico
def p_statement_main(p):
    '''statement : MENOR RESERVADA DOCTYPE DOCTYPE MAYOR MENOR IDENTIFICADOR MAYOR MENOR IDENTIFICADOR MAYOR MENOR IDENTIFICADOR MAYOR RESERVADA RESERVADA RESERVADA MENOR FIN IDENTIFICADOR MAYOR MENOR FIN IDENTIFICADOR MAYOR MENOR IDENTIFICADOR MAYOR MENOR IDENTIFICADOR MAYOR RESERVADA RESERVADA RESERVADA MENOR FIN IDENTIFICADOR MAYOR MENOR FIN IDENTIFICADOR MAYOR MENOR FIN IDENTIFICADOR MAYOR'''
    pass  # La estructura es correcta

def p_error(p):
    if p:
        print(f"Error sintáctico: Token inesperado '{p.value}' en la línea {p.lineno}")
    else:
        print("Error sintáctico: Final inesperado del archivo")
    raise SyntaxError('Error sintáctico')

parser = yacc.yacc()

# Ruta para la página principal
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Obtener el código fuente ingresado por el usuario
        source_code = request.form['source_code']

        # Llamar a los analizadores léxico y sintáctico
        lexical_result = []
        parser_result = ""

        # Analizar léxicamente
        lexer.input(source_code)
        for token in lexer:
            lexical_result.append((token.type, token.value))
        
        # Imprimir resultados léxicos en la consola del servidor
        print("Resultados del análisis léxico:")
        for token_type, token_value in lexical_result:
            print(f"Token: {token_type}, Valor: {token_value}")

        # Analizar sintácticamente
        try:
            parser_result = parser.parse(source_code)
            syntax_result = "La sintaxis es correcta."
        except Exception as e:
            syntax_result = f"Error sintáctico: {str(e)}"
            parser_result = None

        # Devolver los resultados al cliente
        return render_template('index.html',
                               lexical_result=lexical_result,
                               syntax_result=syntax_result,
                               parser_result=parser_result)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
