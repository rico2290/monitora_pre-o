import smtplib, requests, sys, ssl
from bs4 import BeautifulSoup
from smtplib import SMTPException
import schedule, time
from dotenv import load_dotenv
import os 

load_dotenv()

url = 'https://www.amazon.com.br/dp/B07TXV19N9/ref=s9_acsd_hps_bw_r2_topselle_7_i?pf_rd_m=A3RN7G7QC5MWSZ&pf_rd_s=merchandised-search-11&pf_rd_r=D9MDN0CTRP8HMMSETJZC&pf_rd_t=101&pf_rd_p=f8f47fee-2033-4e88-97dd-477a0f30fc61&pf_rd_i=16364755011'
cabecalho = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) \
            Gecko/20100101 Firefox/67.0'}
sender = os.getenv('USR')
password = os.getenv('PWD')
receiver = os.getenv('RCV')

def verifica_preco_produto():
    try:
        print('Obtendo informacoes do produto...')
        pagina = requests.get(url, headers=cabecalho)
        soup = BeautifulSoup(pagina.content, 'html.parser')
        titulo = (soup.find(id='productTitle').get_text()).strip()
        #print(titulo)
        preco_produto = (soup.find(id='priceblock_ourprice').get_text().strip())
        #parte_float = float(soup.find(id='priceblock_ourprice').get_text().strip()[2:7])
        #print(preco_produto)
        
        #if (parte_float > 2.000):
        #print('Preço baixou!!!')
        print(' {0} ==> {1} '.format(titulo,preco_produto))
        print('Enviando email pra cliente...\n')
        enviar_email(sender,receiver,titulo)
           

    except requests.exceptions.HTTPError as  err:
        print(err)
        sys.exit()
    except requests.exceptions.Timeout:
        print('Esgotado tempo de requisição')
    # print(soup.prettify().encode('utf-8')) 
 

def enviar_email(sender, receiver, product_name):
    smtp_server = 'smtp.gmail.com'
    context = ssl.create_default_context()
    try:
        server = smtplib.SMTP(smtp_server, 587)
    
        #with smtplib.SMTP('smtp.gmail.com', 587, context=context) as server:      
        server.ehlo()
        server.starttls(context=context)
        server.ehlo() 
        server.login(sender, password=password)         

      
        subject = 'Corre 🏃🏃‍♀️ o preço baixou 😱' # 
        body = 'O preço do  {}  baixoooouuuu\n\n acesse 👉 {} '.format(product_name,url) #
        message = '''Subject: {}\n\n{} '''.format(subject, body).encode(encoding='utf-8')

        server.sendmail(
            from_addr = sender,
            to_addrs = receiver,
            msg=message
        )
        print('Email enviado com sucesso!!!')
    
    except SMTPException as e:
        print('Erro: Nao foi possível enviar email: {}'.format(e))
    server.quit()

verifica_preco_produto()

#Executar a cada 2 minuto
# schedule.every(2).minutes.do(verifica_preco_produto).tag('pesquisa-na-amazon')
