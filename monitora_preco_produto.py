import smtplib, requests, sys
from bs4 import BeautifulSoup
from smtplib import SMTPException
import schedule, time

url = 'https://www.amazon.com.br/dp/B07VD3JH2C/ref=s9_acsd_hps_bw_c2_x_1_i?pf_rd_m=A3RN7G7QC5MWSZ&pf_rd_s=merchandised-search-4&pf_rd_r=85KKN1M2HCWPRWZZQS9Z&pf_rd_t=101&pf_rd_p=850aa68f-9fed-44ae-ad94-7f66744b422a&pf_rd_i=16243803011'
cabecalho = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) \
            Gecko/20100101 Firefox/67.0'}
user = 'rico220990@gmail.com'
password = 'zecipeskllmocqwc'

def verifica_preco_produto():
    try:
        print('Tentativa de conexão...')
        pagina = requests.get(url, headers=cabecalho)
        soup = BeautifulSoup(pagina.content, 'html.parser')
        titulo = (soup.find(id='productTitle').get_text()).strip()
        preco_produto = (soup.find(id='priceblock_ourprice').get_text().strip())
        parte_float = float(soup.find(id='priceblock_ourprice').get_text().strip()[2:7])
        print(preco_produto)
        
        if (parte_float > 2.000):
            print('Preço baixou!!!')
            print(' {0} ==> {1} '.format(titulo,preco_produto))
            enviar_email()
           

    except requests.exceptions.HTTPError as  err:
        print(err)
        sys.exit()
    except requests.exceptions.Timeout:
        print('Esgotado tempo de requisição')
    # print(soup.prettify().encode('utf-8')) 
 

def enviar_email():
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()

        server.login(user, password=password)
        subject = 'Corre!!! o preço baixou 😱 '  
        body = 'Acesse 👉 {url} '#.format(url)
        message = f'Subject: {subject}\n\n{body}'

        server.sendmail(
            from_addr = 'rico220990@gmail.com',
            to_addrs = 'ricorjl85@hotmail.com',
            msg=message
        )
        print('Email enviado com sucesso!!!')
    
    except SMTPException as e:
        print('Erro: Não foi possível enviar email: {}'.format(e))
    server.quit()

verifica_preco_produto()
#Executar a cada 2 minuto
# schedule.every(2).minutes.do(verifica_preco_produto).tag('pesquisa-na-amazon')
