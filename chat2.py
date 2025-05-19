import os
import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI
import google.generativeai as genai

# Cargar claves del archivo .env
load_dotenv()
openai_key = os.getenv('OPENAI_API_KEY')
gemini_key = os.getenv('GEMINI_API_KEY')

# Inicializar clientes
client = OpenAI(api_key=openai_key)
genai.configure(api_key=gemini_key)

# Función para obtener respuestas de OpenAI o Gemini
def get_response(
    prompt,
    provider_model=('openai', 'gpt-3.5-turbo'),
    temperature=0,
):
    provider, model = provider_model

    if provider == 'openai':
        response = client.chat.completions.create(
            model=model,
            messages=[
                {'role': 'system', 'content': 'Eres un asistente amable'},
                {'role': 'user', 'content': prompt},
            ],
            temperature=temperature
        )
        return response.choices[0].message.content

    elif provider == 'gemini':
        model = genai.GenerativeModel(model_name=model)
        response = model.generate_content(
            prompt,
            generation_config={"temperature": temperature},
            request_options={"timeout": 600}
        )
        return response.candidates[0].content.parts[0].text

    else:
        raise ValueError('Provider not supported')
    
# print(get_response("¿Cuál es la capital de Paraguay?",
#                    provider_model=("openai", "gpt-3.5-turbo")))
print(get_response("¿Cuál es la capital de Paraguay?",
                   provider_model=("gemini", "models/gemini-1.5-flash")))

my_prompts = [
    'Dame 5 ideas de proyectos para hacer con LLMs',
]

# Elegís aquí el proveedor y modelo
provider_model = ('gemini', 'models/gemini-1.5-flash')
# provider_model = ('openai', 'gpt-3.5-turbo')

resultados = []

for prompt in my_prompts:
    respuesta = get_response(prompt, provider_model=provider_model)
    fila = {'prompt': prompt, 'respuesta': respuesta}
    resultados.append(fila)

df = pd.DataFrame(resultados)
print(df)
df.to_csv("respuestas_llm.csv", index=False)
