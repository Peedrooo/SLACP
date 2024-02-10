from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
from time import sleep
from processer import Processer
import os
import pandas as pd

load_dotenv('src/.env')


class Bot:
    def __init__(self, qnt_prec):
        self.username = os.environ.get('LOGIN')
        self.senha = os.environ.get('PASSWORD')
        self.url = os.environ.get('URL')
        self.qnt_prec = qnt_prec
        self.driver = webdriver.Chrome()
        self.classe = os.environ.get('CLASSE')

    def login(self):
        self.driver.get(self.url)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'iframe'))
        )
        iframe = self.driver.find_element(By.TAG_NAME, 'iframe')

        self.driver.switch_to.frame(iframe)

        login_input = self.driver.find_element(By.ID, 'username')
        login_input.send_keys(self.username)

        password_input = self.driver.find_element(By.ID, 'password')
        password_input.send_keys(self.senha)

        login_button = self.driver.find_element(By.ID, 'kc-login')
        login_button.click()

        self.driver.switch_to.default_content()

    def search(self):
        try:

            # click modal button
            modal_button = WebDriverWait(self.driver, 2).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'botao-menu'))
            )
            modal_button.click()
            # print('click modal button')
            sleep(0.1)

            # click process button
            process_button = WebDriverWait(self.driver, 2).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '/html[1]/body[1]/div[6]/div[1]/nav[1]/div[2]/ul[1]/li[2]/a[1]'))
            )
            process_button.click()
            # print('click process button')
            sleep(0.1)

            # click search button
            search_button = WebDriverWait(self.driver, 2).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//a[contains(text(),'Pesquisar')]"))
            )
            search_button.click()
            # print('click search button')
            sleep(0.1)

            # click process button
            process_button = WebDriverWait(self.driver, 2).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//a[@href='/pje/Processo/ConsultaProcesso/listView.seam']"))
            )
            process_button.click()
            # print('click process button')
            sleep(0.1)

            # seach process
            process_input = WebDriverWait(self.driver, 2).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//input[@id='fPP:j_id252:classeJudicial']"))
            )
            process_input.send_keys(self.classe)
            # print('search process')

            # click search button
            search_button = WebDriverWait(self.driver, 2).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//input[@id='fPP:searchProcessos']"))
            )
            search_button.click()
            # print('click search button')

        except:
            self.login()
            self.search()

    def process_recover(self):
        # print('recover process')
        sleep(10)

        process = pd.DataFrame(columns=[
            'Numero', 'Nome', 'CPF', 'Link', 'Precatório'
        ])

        tabela = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "fPP:processosTable:tb"))
        )

        lines = tabela.find_elements(By.TAG_NAME, "tr")
        links = tabela.find_elements(By.TAG_NAME, "a")

        process_links = []
        process_links_number = [
            link for link in range(len(links)) if link % 2 == 1
        ]

        for link in process_links_number:
            process_links.append(links[link])

        line = []
        for e, linha in enumerate(lines):
            colunas = linha.find_elements(By.TAG_NAME, "td")
            for e, coluna in enumerate(colunas):
                if e == 1:
                    numero = coluna.text
                elif e == 6:
                    nome = coluna.text

            line.append({
                'Numero': numero, 'Nome': nome
            })

        page = pd.DataFrame(line)
        process = pd.concat([process, page], ignore_index=True)
        process['Link'] = process_links

        return process

    def process_extration(self, process):
        for row in process.iterrows():
            link = row[1]['Link']
            link.click()
            alert = WebDriverWait(self.driver, 10).until(EC.alert_is_present())
            alert.accept()

        WebDriverWait(self.driver, 10).until(
            EC.number_of_windows_to_be(process.shape[0] + 1)
        )

        for e, window in enumerate(self.driver.window_handles[1:]):
            self.driver.switch_to.window(window)

            try:
                begin_button = WebDriverWait(self.driver, 1).until(
                    EC.element_to_be_clickable(
                        (By.ID, 'detalheDocumento:primeiroDocumento'))
                )
                begin_button.click()

                sleep(1)
                pagina = WebDriverWait(self.driver, 2).until(
                    EC.presence_of_element_located(
                        (By.CLASS_NAME, 'contador-paginas'))
                )

                page_qnt = int(pagina.text.split()[-1])

                for _ in range(page_qnt-1):
                    sleep(0.5)

                    dowload_button = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable(
                            (By.XPATH, "//a[@id='detalheDocumento:download']"))
                    )
                    dowload_button.click()

                    alert = WebDriverWait(self.driver, 10).until(
                        EC.alert_is_present())
                    alert.accept()

                    next_button = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable(
                            (By.ID, 'detalheDocumento:proximoDocumento'))
                    )

                    next_button.click()

                sleep(5)
                process.iloc[
                    e, process.columns.get_loc('Precatório')
                    ] = Processer(page_qnt).run()

            except Exception as e:
                print(e)
                process.iloc[
                    e, process.columns.get_loc('Precatório')
                    ] = 'Documento não encontrado'
                pass

        return process

    def run(self):
        print('LOGIN')
        self.login()
        print('NAVEGAÇÃO')
        self.search()
        print('RECUPERAÇÃO')
        process = self.process_recover()
        print('EXTRAÇÃO')
        process = self.process_extration(process)
        print(process)
        return process


if __name__ == '__main__':
    bot = Bot(2)
    bot.run()
