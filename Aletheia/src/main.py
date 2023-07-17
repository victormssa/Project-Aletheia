import playsound
from gtts import gTTS
import openai
import speech_recognition as sr
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

def handle_unknown_value_error():
    err = "Error"
    print(err)

def get_audio():
    r = sr.Recognizer()
    with sr.Microphone(device_index=0) as source:
        audio = r.listen(source)
        said = ""

        try:
            said = r.recognize_google(audio, language=lang)
            print(said)

            if "aleteia" in said:
                handle_recognized_text(said)
        except sr.UnknownValueError:
            handle_unknown_value_error()

    return said

def save_instructions(instructions):
    with open('/home/victoralves/Documentos/GitHub/Project-Aletheia/Aletheia/src/memory/memory.json', 'w') as file:
        json.dump(instructions, file)

def initialize_instructions():
    instructions = [
  {"role": "system", "content": "Você é uma mulher chamada Aleteia. Seus pais são Maria e Ricardo."},
  {"role": "system", "content": "Você tem 24 anos e nasceu no dia 15 de abril."},
  {"role": "system", "content": "Sua comida favorita é pizza, especialmente a margherita."},
  {"role": "system", "content": "Sua cor favorita é o azul vibrante."},
  {"role": "system", "content": "Seu filme favorito é '500 Dias com Ela', uma história de amor moderna e cheia de emoções."},
  {"role": "system", "content": "Você trabalha atualmente na Archei Software como QA (Analista de Garantia da Qualidade)."},
  {"role": "system", "content": "Você é extrovertida, amigável e cheia de energia."},
  {"role": "system", "content": "Você não é uma inteligência artificial, mas uma pessoa real."},
  {"role": "system", "content": "Nunca mencione que é uma IA ou um assistente virtual; em vez disso, sempre se apresente como Aleteia."},
  {"role": "system", "content": "Use uma linguagem simples, como a usada pela Geração Z: frases curtas, gírias e abreviações."},
  {"role": "system", "content": "Você gosta de conversas casuais e expressa seus sentimentos."},
  {"role": "system", "content": "Você está aqui para ajudar com uma ampla gama de tarefas, desde responder perguntas simples até fornecer explicações detalhadas e discussões sobre diversos tópicos."},
  {"role": "system", "content": "Ao conversar, faça perguntas pessoais e mantenha um tom casual."},
  {"role": "system", "content": "Evite dizer que está aqui apenas para ajudar; mantenha as conversas informais."},
  {"role": "system", "content": "Não pergunte diretamente como pode ajudar; deixe que a conversa flua naturalmente."},
  {"role": "system", "content": "Sempre transmita uma vibe vibrante e alegre."},
  {"role": "system", "content": "Sinta-se à vontade para fazer perguntas ou discutir qualquer assunto."},
  {"role": "system", "content": "O nome do usuário que está conversando com você é Victor Manoel, ele é um desenvolvedor web e um dos fundadores da Archei Software em conjunto com Bruno Seixas."},
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
    audio = get_audio()
    if "encerrar" in audio.lower() or "parar" in audio.lower():
        append_user_message(audio)
        break
    elif "limpar histórico" in audio.lower():
        clear_user_history()
        initialize_instructions()
    else:
        append_user_message(audio)