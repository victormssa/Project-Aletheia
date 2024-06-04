import axios from 'axios';
import readline from 'readline';
import chalk from 'chalk';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

// Substitua 'YOUR_API_KEY' pela sua chave de API
const API_KEY = 'pat_iK5QV0gF2j0OvgMfDNhkgxoB7Xdx1R4DCGechjGLW1CNLZHFYJkhF6CqLAIiZJkY';
const BASE_URL = 'https://api.coze.com/open_api/v2/chat';

// Substitua 'YOUR_BOT_ID' pelo ID do seu bot
const BOT_ID = '7376629605757042694';

// Configuração dos cabeçalhos da requisição
const headers = {
    'Authorization': `Bearer ${API_KEY}`,
    'Content-Type': 'application/json'
};

// Função para enviar mensagem ao bot
async function sendMessage(user, message) {
    const data = {
        bot_id: BOT_ID,
        user: user,
        query: message
    };

    try {
        const response = await axios.post(BASE_URL, data, { headers });
        return response.data;
    } catch (error) {
        console.error(chalk.red(`Erro: ${error.response ? error.response.data : error.message}`));
        return null;
    }
}

// Configuração do readline para interação com o terminal
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
    prompt: chalk.blue('Você: ') // Adiciona cor ao prompt do usuário
});

// Função para salvar o histórico de mensagens
function saveMessageHistory(filename, message) {
    fs.appendFileSync(filename, message + '\n', 'utf8');
}

// Função principal para gerenciar o loop de interação
async function main() {
    const sessionId = new Date().toISOString().replace(/[:.]/g, '-');
    const __filename = fileURLToPath(import.meta.url);
    const __dirname = path.dirname(__filename);
    const historyFile = path.join(__dirname, `chat_history_${sessionId}.txt`);

    console.log(chalk.green("Bem-vindo ao chat com o bot Anima! Digite 'sair' para encerrar."));
    rl.prompt();

    rl.on('line', async (input) => {
        if (input.toLowerCase() === 'sair') {
            console.log(chalk.yellow("Encerrando o chat. Até mais!"));
            rl.close();
            return;
        }

        const user = 'user1'; // Identificador do usuário, pode ser ajustado conforme necessário
        saveMessageHistory(historyFile, `Você: ${input}`);
        const botResponse = await sendMessage(user, input);
        if (botResponse && botResponse.messages) {
            // Filtra e exibe apenas as mensagens de resposta do bot
            const botMessages = botResponse.messages
                .filter(msg => msg.role === 'assistant' && msg.type === 'answer')
                .map(msg => msg.content);

            botMessages.forEach(msg => {
                console.log(chalk.cyan("Bot: ") + msg);
                saveMessageHistory(historyFile, `Bot: ${msg}`);
            });

            // Exibe sugestões de respostas do bot
            const followUpMessages = botResponse.messages
                .filter(msg => msg.role === 'assistant' && msg.type === 'follow_up')
                .map(msg => msg.content);

            if (followUpMessages.length > 0) {
                console.log(chalk.magenta("\nSugestões de respostas:"));
                followUpMessages.forEach(msg => {
                    console.log(chalk.magenta("- ") + msg);
                    saveMessageHistory(historyFile, `Sugestão: ${msg}`);
                });
            }
        } else {
            console.log(chalk.red("Não foi possível obter uma resposta do bot."));
            saveMessageHistory(historyFile, "Não foi possível obter uma resposta do bot.");
        }
        rl.prompt();
    });
}

// Executa a função principal
main();