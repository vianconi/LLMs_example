from utils import ChatOpenRouter
import zmq
from langchain import PromptTemplate
from langchain.schema import HumanMessage
from langchain.prompts import ChatPromptTemplate
        
# Configurar ZMQ
context = zmq.Context()
socket = context.socket(zmq.PUSH)
socket.bind("tcp://*:5555")

receiver = context.socket(zmq.PULL)
receiver.connect("tcp://localhost:5557")

# Configurar LangChain
model = "openai/gpt-3.5-turbo"

llm = ChatOpenRouter(
    model_name=model
)

# Plantilla de prompt para el desarrollador
developer_template = """
Eres un desarrollador de Python. 

Se te dará un problema y debes proporcionar el código que lo resuelve.

Problema: {problem}

Proporciona solo el código Python, sin explicaciones adicionales. No lo encierres en el tag ```python ... ```.
"""

developer_prompt = ChatPromptTemplate.from_template(developer_template)

# Problema de ejemplo
problem = "Escribe una función que cálcule si un string es un palindrome."

# Generar código
messages = developer_prompt.format_messages(problem=problem)
response = llm(messages)
code = response.content

print(code)
# Enviar código al tester
socket.send_string(code)

while True:
    errors = receiver.recv_string()
    # Plantilla de prompt para el desarrollador
    developer_fix_template = """
    Eres un desarrollador de Python. 

    El código:

    {code}

    A producido los siguientes errores en las pruebas unitarias.

    {errors}

    Genera un nuevo código que pueda pasarlas.

    Proporciona solo el código Python, sin explicaciones adicionales. No lo encierres en el tag ```python ... ```.
    """

    developer_fix_template = ChatPromptTemplate.from_template(developer_fix_template)
    messages = developer_fix_template.format_messages(code=code, errors=errors)
    print(messages)
    response = llm(messages)
    code = response.content

    print("Fix: ", code)
    
    socket.send_string(code)
    print("Código enviado al tester.")
    