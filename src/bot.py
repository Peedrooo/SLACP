from variavel import username, senha
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from dotenv import load_dotenv
from time import sleep

load_dotenv('src/.env')


class Bot:
    def __init__(self, qnt_prec):
        self.username = os.environ.get('USERNAME')
        self.senha = os.environ.get('SENHA')
        self.url = os.environ.get('URL')
        print(self.url)
        self.qnt_prec = qnt_prec
        self.driver = webdriver.Chrome()

    def login(self):
        self.driver.get(self.url)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'iframe'))
        )
        iframe = self.driver.find_element(By.TAG_NAME, 'iframe')

        self.driver.switch_to.frame(iframe)

        login_input = self.driver.find_element(By.ID, 'username')
        login_input.send_keys(username)

        password_input = self.driver.find_element(By.ID, 'password')
        password_input.send_keys(senha)

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
            print('click modal button')
            sleep(0.1)

            # click process button
            process_button = WebDriverWait(self.driver, 2).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '/html[1]/body[1]/div[6]/div[1]/nav[1]/div[2]/ul[1]/li[2]/a[1]'))
            )
            process_button.click()
            print('click process button')
            sleep(0.1)

            # click search button
            search_button = WebDriverWait(self.driver, 2).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//a[contains(text(),'Pesquisar')]"))
            )
            search_button.click()
            print('click search button')
            sleep(0.1)

            # click process button
            process_button = WebDriverWait(self.driver, 2).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//a[@href='/pje/Processo/ConsultaProcesso/listView.seam']"))
            )
            process_button.click()
            print('click process button')
            sleep(0.1)

            # seach process
            process_input = WebDriverWait(self.driver, 2).until(
                EC.presence_of_element_located((By.XPATH, "//input[@id='fPP:j_id252:classeJudicial']"))
            )
            process_input.send_keys('CUMPRIMENTO DE SENTENÇA CONTRA A FAZENDA PÚBLICA')
            print('search process')

            # click search button
            search_button = WebDriverWait(self.driver, 2).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//input[@id='fPP:searchProcessos']"))
            )
            search_button.click()
            print('click search button')

            sleep(100)
        except:
            self.login()
            self.search()

    def run(self):
        self.login()
        self.search()


if __name__ == '__main__':
    bot = Bot(2)
    bot.run()
