from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
from time import sleep
from postprocesser import PostProcesser
import os
import pandas as pd
import warnings

warnings.filterwarnings("ignore")
import logging

logging.basicConfig(level=logging.WARNING)


load_dotenv('src/.env')


class Bot:
    def __init__(self, qnt_prec: int , user_page:int = 1 ):
        self.username = os.environ.get('LOGIN')
        self.senha = os.environ.get('PASSWORD')
        self.url = os.environ.get('URL')
        self.qnt_prec = qnt_prec
        self.driver = webdriver.Chrome()
        self.classe = os.environ.get('CLASSE')
        self.pagination = 1
        self.user_page = user_page
        self.first_load = True

    def login(self):
        print('LOGIN')
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
        print('NAVEGAÇÃO')

        try:

            modal_button = WebDriverWait(self.driver, 2).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'botao-menu'))
            )
            modal_button.click()
            sleep(0.1)

            process_button = WebDriverWait(self.driver, 2).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '/html[1]/body[1]/div[6]/div[1]/nav[1]/div[2]/ul[1]/li[2]/a[1]'))
            )
            process_button.click()
            sleep(0.1)

            search_button = WebDriverWait(self.driver, 2).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//a[contains(text(),'Pesquisar')]"))
            )
            search_button.click()
            sleep(0.1)

            process_button = WebDriverWait(self.driver, 2).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//a[@href='/pje/Processo/ConsultaProcesso/listView.seam']"))
            )
            process_button.click()
            sleep(0.1)

            process_input = WebDriverWait(self.driver, 2).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//input[@id='fPP:j_id252:classeJudicial']"))
            )
            process_input.send_keys(self.classe)

            search_button = WebDriverWait(self.driver, 2).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//input[@id='fPP:searchProcessos']"))
            )
            search_button.click()

        except:
            self.login()
            self.search()

    def process_recover(self):
        print('RECUPERAÇÃO')
        self.driver.switch_to.window(self.driver.window_handles[0])
        process = pd.DataFrame(columns=[
            'Numero', 'Nome', 'CPF', 'Link', 'Precatório'
        ])

        sleep(11) if self.first_load else None
        self.first_load = False

        while self.pagination < self.user_page:
            next_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//td[normalize-space()='»']"))
            )
            next_button.click()
            self.pagination += 1
            sleep(3)

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

    def check_prec(self):
        result = pd.DataFrame(columns=[
            'Numero', 'Nome', 'CPF', 'Link', 'Precatório'
        ])

        while result.shape[0] < self.qnt_prec:
            process = self.process_recover()
            self.user_page += 1
            for row in process.iterrows():
                link = row[1]['Link']
                print(link)
                link.click()
                alert = WebDriverWait(self.driver, 10).until(
                    EC.alert_is_present())
                alert.accept()

            WebDriverWait(self.driver, 10).until(
                EC.number_of_windows_to_be(process.shape[0] + 1)
            )

            for e, window in enumerate(self.driver.window_handles[1:]):
                self.driver.switch_to.window(window)
                self.driver.fullscreen_window()

                search_box = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(
                        (By.ID, 'divTimeLine:txtPesquisa')
                    )
                )
                search_box.send_keys('precatório')

                WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//i[@class='fa fa-search text-muted']")
                    )
                ).click()
                sleep(1)

                try:
                    WebDriverWait(self.driver, 2).until(
                        EC.presence_of_element_located(
                            (By.XPATH,
                            "//span[@class='text-muted data-interna']")
                        )
                    )
                    process.iloc[
                        e, process.columns.get_loc('Precatório')
                    ] = True
                except:
                    process.iloc[
                        e, process.columns.get_loc('Precatório')
                    ] = False
                    continue
                finally:
                    self.driver.close()
            buffer = PostProcesser(process).run()
            result = pd.concat([result, buffer], ignore_index=True)
            print('Precatórios até o momento encontrados:', result.shape[0])
            result.to_excel('precatorios.xlsx', index=False)
        return result

    def run(self):
        self.login()
        self.search()
        print('VERIFICAÇÃO')
        process = self.check_prec()
        return process


if __name__ == '__main__':
    bot = Bot(5)
    bot.run()
