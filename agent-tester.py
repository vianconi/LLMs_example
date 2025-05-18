from utils import ChatOpenRouter
import zmq
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from langchain.prompts import ChatPromptTemplate

# Configurar ZMQ
context = zmq.Context()
receiver = context.socket(zmq.PULL)
receiver.connect("tcp://localhost:5555")

sender = context.socket(zmq.PUSH)
sender.bind("tcp://*:5556")

# Configurar LangChain
model = "openai/gpt-4-turbo"

llm = ChatOpenRouter(
    model_name=model
)

print("Se ha iniciado el agent-tester.")

while True:
    # Plantilla de prompt para el tester
    tester_template = """
    Eres un tester de Python. Se te dará un código y debes crear pruebas unitarias (dificiles) para evaluarlo.

    Código:
    {code}

    Crea pruebas unitarias utilizando el módulo unittest de Python para verificar que el código funciona correctamente.
    Proporciona solo el código de las pruebas, sin explicaciones adicionales. No lo encierres en el tag ```python ... ```
    """
    tester_prompt = ChatPromptTemplate.from_template(tester_template)
    # Recibir código del developer
    code = receiver.recv_string()

    print(f"\n-------------------------------------------------\nRecibí del agent-dev:\n {code}\n-------------------------------------------------")

    # Generar pruebas
    messages = tester_prompt.format_messages(code=code)
    response = llm(messages)
    tests = response.content

    print(tests)
    # Enviar pruebas al ejecutor

    new_prompt = f"""{code}\n{tests}"""
    sender.send_string(new_prompt)

    print("Pruebas enviadas al ejecutor.")
    