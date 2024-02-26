import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from postprocesser import PostProcesser
from resources import clean_terminal, URL, LOGIN, PASSWORD, CLASSE
import os
import pandas as pd
import warnings

warnings.filterwarnings("ignore")

logging.basicConfig(level=logging.WARNING)


class Bot():
    def __init__(
            self, qnt_prec: int,
            user_page: int = 1,
            continuation: bool = False,
            URL: str = URL,
            key: str = 'Precatório'):

        self.username = LOGIN
        self.senha = PASSWORD
        self.driver = webdriver.Chrome()
        self.url = URL
        self.qnt_prec = qnt_prec
        self.classe = CLASSE
        self.pagination = 1
        self.user_page = user_page
        self.first_load = True
        self.continuation = continuation
        self.keyword = key

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
        clean_terminal()
        print('-=RECUPERAÇÃO=-')
        self.driver.switch_to.window(self.driver.window_handles[0])
        process = pd.DataFrame(columns=[
            'Numero', 'Nome', 'Polo Passivo', 'Link', 'Precatório', 'Página'
        ])

        sleep(12) if self.first_load else None
        self.first_load = False

        fall_pagination = 0
        while self.pagination < self.user_page:
            try:
                next_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//td[normalize-space()='»']"))
                )
                next_button.click()
                self.pagination += 1
                sleep(3.5)
            except:
                fall_pagination += 1
                clean_terminal()
                print("-=RECUPERAÇÃO=-")
                print('Erro na paginação! Tentando novamente...')
                sleep(3.5)
                if fall_pagination > 150:
                    break


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
                elif e == 7:
                    polo_passivo = coluna.text

            line.append({
                'Numero': numero, 'Nome': nome, "Polo Passivo": polo_passivo,
            })

        page = pd.DataFrame(line)
        process = pd.concat([process, page], ignore_index=True)
        process['Link'] = process_links
        return process

    def check_prec(self):
        result = pd.DataFrame(columns=[
            'Numero', 'Nome', 'Página'
        ])

        while result.shape[0] < self.qnt_prec:
            process = self.process_recover()
            self.user_page += 1
            windows = []
            print('Precatórios encontrados:', result.shape[0])

            for row in process.iterrows():
                link = row[1]['Link']
                link.click()
                alert = WebDriverWait(self.driver, 10).until(
                    EC.alert_is_present())
                alert.accept()
                sleep(2)
                WebDriverWait(self.driver, 10).until(EC.new_window_is_opened)
                windows.append(self.driver.window_handles[-1])

                print('Página:', self.pagination,
                      'Processo:', row[1]['Numero'])
            print('Avaliando Processos...')

            WebDriverWait(self.driver, 10).until(
                EC.number_of_windows_to_be(process.shape[0] + 1)
            )

            for e, window in enumerate(windows):
                self.driver.switch_to.window(window)
                self.driver.fullscreen_window()

                search_box = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(
                        (By.ID, 'divTimeLine:txtPesquisa')
                    )
                )
                search_box.send_keys(self.keyword)

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
                process.iloc[
                    e, process.columns.get_loc('Página')
                ] = self.pagination

                self.driver.close()

            process.to_excel('buffer.xlsx', index=False)
            buffer = PostProcesser(process).run()
            result = pd.concat([result, buffer], ignore_index=True)
            result = result.drop_duplicates(subset='Numero')

            if self.continuation and os.path.exists('precatorios.xlsx'):
                buffer = pd.read_excel('precatorios.xlsx')
                result = pd.concat([result, buffer], ignore_index=True)
                result = result.drop_duplicates(subset='Numero')

            result.to_excel('precatorios.xlsx', index=False)

        return result

    def close(self):
        self.driver.quit()

    def run(self):
        self.login()
        self.search()
        process = self.check_prec()
        return process

if __name__ == '__main__':
    bot = Bot(2, user_page=4)
    bot.run()
