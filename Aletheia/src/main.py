import playsound
from gtts import gTTS
import openai
import json

api_key = "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"
lang = 'pt-BR'
openai.api_key = api_key

def play_audio(text):
    speech = gTTS(text=text, lang=lang, slow=False)
    speech.save("Aletheia/src/assets/aud/audio.mp3")
    playsound.playsound("Aletheia/src/assets/aud/audio.mp3")

def handle_recognized_text(text):
    with open('/home/victoralves/Documentos/GitHub/Project-Aletheia/Aletheia/src/memory/memory.json', 'r') as file:
        instructions = json.load(file)

    instructions[-1]["content"] = text

    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=instructions)
    response_text = completion.choices[0].message.content
    print(response_text)
    play_audio(response_text)

def save_instructions(instructions):
    with open('/home/victoralves/Documentos/GitHub/Project-Aletheia/Aletheia/src/memory/memory.json', 'w') as file:
        json.dump(instructions, file)

def initialize_instructions():
    instructions = [
  {"role": "system", "content": "Você é uma mulher chamada Aleteia. Seus pais são Maria e Ricardo."},
  {"role": "user", "content": ""}
]
    save_instructions(instructions)

def append_user_message(message):
    with open('/home/victoralves/Documentos/GitHub/Project-Aletheia/Aletheia/src/memory/memory.json', 'r') as file:
        instructions = json.load(file)

    instructions.append({"role": "user", "content": message})
    save_instructions(instructions)

def append_system_message(message):
    with open('/home/victoralves/Documentos/GitHub/Project-Aletheia/Aletheia/src/memory/memory.json', 'r') as file:
        instructions = json.load(file)

    instructions.append({"role": "system", "content": message})
    save_instructions(instructions)

def clear_user_history():
    with open('/home/victoralves/Documentos/GitHub/Project-Aletheia/Aletheia/src/memory/memory.json', 'r') as file:
        instructions = json.load(file)

    instructions = instructions[:1]
    save_instructions(instructions)

initialize_instructions()

while True:
    user_input = input("Digite sua pergunta: ")
    if "encerrar" in user_input.lower() or "parar" in user_input.lower():
        append_user_message(user_input)
        break
    elif "limpar histórico" in user_input.lower():
        clear_user_history()
        initialize_instructions()
    else:
        append_user_message(user_input)
        handle_recognized_text(user_input)
