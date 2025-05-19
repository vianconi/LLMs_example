import os
from dotenv import load_dotenv
from openai import OpenAI  # Para SDK >= 1.0.0

# Cargar el .env
load_dotenv()

# Obtener la API Key
openai_api_key = os.getenv('OPENAI_API_KEY')

# Instanciar el cliente de OpenAI
client = OpenAI(api_key=openai_api_key)

# Mensajes iniciales
messages = [
    {'role': 'user', 'content': 'Eres un asistente útil'}
]

# Entrada del usuario
user_input = input('Tú: ')
messages.append({'role': 'user', 'content': user_input})

# Realizar la solicitud
completion = client.chat.completions.create(
    model='gpt-3.5-turbo',
    messages=messages
)

# Mostrar respuesta
assistant_response = completion.choices[0].message.content
print(f'Asistente: {assistant_response}')
