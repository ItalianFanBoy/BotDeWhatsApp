import asyncio
import time
from datetime import date, datetime
from playwright.async_api import Playwright, async_playwright, expect
import mysql.connector

#---------------------------------------------------------------------------
import acesso as cx 
import status as st
import mensagens as msg

#------------------------------------------------------------------------------
async def run(playwright: Playwright) -> None:
    browser = await playwright.chromium.launch(headless=False)
    context = await browser.new_context()

    #abrir nova pagina
    page = await context.new_page()

    #abrir site do whatsapp
    await page.goto("https://web.whatsapp.com")

    # letura do HTML
    await page.locator('//*[@id="side"]/div[1]/button/div/span').click
    await page.locator('//*[@id="app"]/div/span[4]/div/ul/div/li[1]/div/div[2]').click

    while page:
        time.sleep(5)
        data_atual = date.today()
        try:
        
            await page.get_by_test_id("icon-unread-count").nth(0).click()
            time.sleep(3)

            nome_real = "~"
            telefone = await page.locator('//*[@id="main"]/header/div/[2]/div/div/span').all_text_contents()
            print(telefone)
            tel = telefone[0].replace(" ", "")
            t = tel.replace("-", "")

            fone = t.replace("+", "")
            print(fone)

            time.sleep(3)

            for i in range(1):
                count =  await page.get_by_test_id("msg-container").count()
                a = await page.get_by_test_id("msg-container").all_text_contents()

            texto =  a[-1]
            ultimamensagem = str(texto[0:-10])
            print(ultimamensagem)

        #--------------------------------------------------------------------------------------

            conectar = mysql.connector.connect(host= cx.h, database=cx.d, user=cx.u, password= cx.p)
            dados = '('+'\''+str(nome_real)+'\''+',\''+str(fone)+'\''+',\''+str(ultimamensagem)+'\''+')'
            comando = "INSERT INTO `atendimento`(`apoio, `Telefone`, `Mensagem`) VALUES"
            sql = comando + dados

            print(sql)
            
            try:
                cursos = conectar.cursor()
                cursos.execute(sql)
                conectar.commit()
                conectar.close()

            except:
                conectar.close


            conectar = mysql.connector.connect(host= cx.h, database=cx.d, user=cx.u, password= cx.p)
            dados = '('+'\''+str(nome_real)+'\''+',\''+str(fone)+'\''+',\''+str(ultimamensagem)+'\''+')'
            comando = "INSERT INTO `processo_atendimento`(`apoio, `Telefone`, `Mensagem`) VALUES"
            sql = comando + dados

            print(sql)
            
            try:
                cursos = conectar.cursor()
                cursos.execute(sql)
                conectar.commit()
                conectar.close()

            except:
                conectar.close

            
            conexao = mysql.connector.connect(host= cx.h, database=cx.d, user=cx.u, password= cx.p)

            cursor =  conexao.cursor()
            select = cursor.execute("SELECT `apoio`, `Telefone`, `ID`, `Status`, `Nome_Completo`,`Data_nascimento`, `CPF`, `email` From `processo_atendimento` ") 
            resultador = cursor.fetchall()
            conexao.close()



            for resultados in resultado:
                resultados[0]
                resultados[1]
                resultados[2]
                resultados[3]
                resultados[4]
                resultados[5]
                resultados[6]
                resultados[7]

            if str(resultados[3]) == 'aguardando':
                mensagem = msg.menu_saudacao
                atualizar1 = st.esperando_opcao
                atualizar2 = ultimamensagem
                atualizar3 = ultimamensagem


                campo1 = 'Status'
                campo2 = 'apoio'
                campo3= 'apoio2'

            elif str(resultados[3]==str(st.esperando_opcao) and str(ultimamensagem)=='1'):
                mensagem = msg.nomecompleto
                mensagem = st.nome_completo
                atualizar2 = ultimamensagem
                atualizar3 = 'EP'
                
                campo1 = 'Status'
                campo2 = 'apoio'
                campo3= 'Produto'

            elif str(resultados[3]==str(st.esperando_opcao) and str(ultimamensagem)=='3'):
                mensagem = msg.nomecompleto
                mensagem = st.nome_completo
                atualizar2 = ultimamensagem
                atualizar3 = "Outros"
                
                campo1 = 'Status'
                campo2 = 'apoio'
                campo3= 'Produto'
            
            elif str(resultados[3]==str(st.esperando_opcao) and str(ultimamensagem)=='1'):
                mensagem = msg.nomecompleto
                mensagem = st.nome_completo
                atualizar2 = ultimamensagem
                
                campo1 = 'Status'
                campo2 = 'apoio'
                campo3= 'Produto'

            
        except:
            time.sleep(1)
            continue 

async def main() -> None:
    async with async_playwright() as playwright:
        await run(playwright)
asyncio.run(main())