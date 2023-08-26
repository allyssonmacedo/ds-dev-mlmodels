import telebot #pip install pytelegrambotapi
import time
from datetime import datetime
import inner_infos as info
import predict_regressao_model as regression

bot = telebot.TeleBot(info.CHAVE_API)

hora = datetime.now().strftime('%H')
   
#Adiciona um novo membro 
@bot.message_handler(commands=["lista"])
def lista_automática(mensagem):
    chat_id = mensagem.chat.id
    if str(chat_id) in list(info.chat_ids.values()):
        bot.send_message(mensagem.chat.id, f"""Você já está na lista automática. Caso deseje parar de receber os informes, entre em contato com o setor do Agrodigital""")
    else:
        msg = bot.send_message(mensagem.chat.id, f"""{mensagem.chat.first_name}, Deseja receber mensagens automáticas em horarios definidos? Digite Sim ou Não """)
        bot.register_next_step_handler(msg, novo_membro)
def novo_membro(mensagem):
    info_text = mensagem.text
    if info_text.lower() in ['sim','quero','ok','s','pode ser', 'claro', 'positivo']:
        bot.reply_to(mensagem, f'OK, {mensagem.chat.first_name}. Um administrador irá averiguar seu pedido e confirmá-lo.')
        #Envia mensagem para o Allysson com a info da mensagem para que possa adicionar manualmente no script.
        bot.send_message('801431606', f'{mensagem.chat.first_name} deseja fazer parte da lista automática do AgrodigitalBot! \n {mensagem}')
    else:
        bot.reply_to(mensagem, f'OK, {mensagem.chat.first_name}. Espero que continue utilizando o @AgrodigitalBot quando precisar!')
   
#Envia o dashboard com a colheita de milho
@bot.message_handler(commands=["PreverSuporte"])
def prever_suporte_regressao_logistica():
    
    regression()

    # msg = bot.send_message(mensagem.chat.id, f'{mensagem.chat.first_name}, Responda as perguntas para interagir com o sistema')
    # bot.send_message(mensagem.chat.id, 'Digite o número corresponte: \n 0 - Todas as unidades \n 1 - Cerro Azul \n 2 - Fortaleza \n 3 - Ipê')
    # bot.register_next_step_handler(msg, selecionar_unidade_colheita_milho)
def selecionar_unidade_colheita_milho(mensagem):
    selecionar_unidade(mensagem, 'COLHEITA DE MILHO', info.colheita_milho_geral, info.colheita_milho_caz, info.colheita_milho_ftz, info.colheita_milho_ipe)
    bot.send_message(mensagem.chat.id, 'Caso deseje interagir com o dashboard, acesse: https://bit.ly/colheita-milho')

#Envia o dashboard com a gradagem
@bot.message_handler(commands=["gradagem"])
def gradagem(mensagem):
    msg = bot.send_message(mensagem.chat.id, f'{mensagem.chat.first_name}, Informe a unidade que deseja visualizar')
    bot.send_message(mensagem.chat.id, 'Digite o número corresponte: \n 0 - Todas as unidades \n 1 - Cerro Azul \n 2 - Fortaleza \n 3 - Ipê')
    bot.register_next_step_handler(msg, selecionar_unidade_gradagem)
def selecionar_unidade_gradagem(mensagem):
    selecionar_unidade(mensagem, 'GRADAGEM', info.gradagem_geral, info.gradagem_caz, info.gradagem_ftz, info.gradagem_ipe)
    bot.send_message(mensagem.chat.id, 'Caso deseje interagir com o dashboard, acesse: https://bit.ly/gradagem')
    
#Configurações Gerais
def selecionar_unidade(mensagem, Operação, diretorio_geral, diretorio_caz, diretorio_ftz, diretorio_ipe):
        unid = mensagem.text
        data_hoje = str(datetime.now().strftime('%d/%m/%y'))
        global dh
        dh = data_hoje.replace('/','-')    
        if unid == '0':
            bot.reply_to(mensagem, f'Abrindo dashboard de {Operação} para todas as Unidades')
            bot.send_photo(mensagem.chat.id, 'https://phoenixnap.com/kb/wp-content/uploads/2021/04/install-python-on-windows.png')
            #bot.send_photo(mensagem.chat.id, photo=open(diretorio_geral + dh + '.png', 'rb'))
        elif unid == '1':
            bot.reply_to(mensagem, f'Abrindo dashboard de {Operação} para a CERRO AZUL')
            bot.send_photo(mensagem.chat.id, photo=open(diretorio_caz + dh + '.png', 'rb'))
        elif unid == '2':
            bot.reply_to(mensagem, f'Abrindo dashboard de {Operação} para a FORTALEZA')
            bot.send_photo(mensagem.chat.id, photo=open(diretorio_ftz + dh + '.png', 'rb'))
        elif unid == '3':
            bot.reply_to(mensagem, f'Abrindo dashboard de {Operação} para a IPÊ')
            bot.send_photo(mensagem.chat.id, photo=open(diretorio_ipe + dh + '.png', 'rb'))
        else:
            bot.reply_to(mensagem, f'Unidade não encontrada, tente novamente')

def verificar(mensagem):
    return True

@bot.message_handler(func=verificar)
def responder(mensagem):
    texto_inicial = f"""Olá, {mensagem.chat.first_name}! 
    Este é um bot desenvolvido para você conseguir testar o seu modelo de machine learning de maneira interativa 
    /PreverSuporte Visualizar a probabilidade de seus clientes acionarem o suporte mais de uma vez por semana
    /lista Para receber diariamente o relatório customizado \n
Responder qualquer outra coisa não vai funcionar, clique em uma das opções"""
    bot.reply_to(mensagem, texto_inicial)
    print(f'{datetime.now()} - {mensagem.chat.id} {mensagem.chat.first_name}: {mensagem.text}')  

bot.polling()

