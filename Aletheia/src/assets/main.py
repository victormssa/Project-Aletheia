import requests
import json

# Substitua 'YOUR_API_KEY' pela sua chave de API
API_KEY = 'YOUR_API_KEY'
BASE_URL = 'https://api.coze.com/v1/messages'

# Configuração dos cabeçalhos da requisição
headers = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}

def send_message(message):
    """
    Envia uma mensagem para o bot e retorna a resposta.

    Args:
        message (str): A mensagem a ser enviada para o bot.

    Returns:
        dict: A resposta do bot em formato JSON.
    """
    data = {
        'message': message
    }
    try:
        response = requests.post(BASE_URL, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # Levanta uma exceção para códigos de status HTTP 4xx/5xx
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"Erro HTTP: {http_err}")
    except Exception as err:
        print(f"Erro: {err}")
    return None

def main():
    """
    Função principal que gerencia o loop de interação com o usuário.
    """
    print("Bem-vindo ao chat com o bot Coze! Digite 'sair' para encerrar.")
    while True:
        user_message = input("Você: ")
        if user_message.lower() == 'sair':
            print("Encerrando o chat. Até mais!")
            break
        bot_response = send_message(user_message)
        if bot_response:
            print("Bot:", bot_response.get('response', 'Sem resposta'))
        else:
            print("Não foi possível obter uma resposta do bot.")

if __name__ == "__main__":
    main()