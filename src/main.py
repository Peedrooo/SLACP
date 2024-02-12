import sys
from bot import Bot
import pandas as pd
import os

class Menu():

    select = 0

    def line(self):
        print('-=' * 33)

    def small_line(self):
        print('-=' * 16)

    def initial(self):
        self.line()
        print('Seja Bem Vindo ao SLACP - Sistema L4 Ativos Coletor de Precatórios')
        self.line()

    def wrong_option(self):
        self.small_line()
        print('Opção inválida, tente novamente.')
        self.small_line()

    def activate_format(self, service):
        self.small_line()
        print(service)
        self.small_line()

    def verify_file(self):
        try:
            df = pd.read_excel('precatorios.xlsx')
            last_page = max(df['Página'])
            return last_page
        except FileNotFoundError:
            return False

    def init(self):
        self.initial()
        self.qnt_prec = 0
        self.user_page = 0
        self.file = self.verify_file()
        while self.select != 9:
            try:
                print('1 - Coletar Precatórios')
                print('2 - Ativar API')
                print('3 - Atualizar Credenciais')
                print('9 - Encerrar')
                if len(sys.argv) > 1:
                    select = int(sys.argv[1])
                    print('Opção desejada:', select)
                else:
                    select = int(input('Opção desejada: '))

                if select == 1:
                    self.activate_format('Iniciando coleta de Precatórios')

                    while self.qnt_prec == 0:
                        try:
                            self.qnt_prec = int(input('Digite a quantidade de Precatórios que deseja coletar: '))
                        except ValueError:
                            print('Digite um número natual válido.')

                    if self.file:
                        continuation = input('Observei que o programa estava em execução Anteriormente \nGostaria de continuar de onde parou? (1 - Sim, 2 - Não): ')
                        self.user_page = self.file if continuation == '1' else '0'

                    while self.user_page == '0':
                        try:
                            self.user_page = int(input('Digite a página que deseja iniciar a coleta: '))
                        except ValueError:
                            print('Digite um número natual válido.')
                    continuation = True if continuation == '1' else False
                    bot = Bot(self.qnt_prec, self.user_page, continuation)

                    self.activate_format('Ativando Bot')

                    print(bot.run())
                    self.activate_format('Encerrando sistema')

                    return 
                
                elif select == 2:
                    self.activate_format('Ativando API')
                    return
                
                elif select == 3:
                    cpf = input('Digite o novo CPF: ')
                    password = input('Digite a nova senha: ')

                    with open('src/.env', 'r') as file:
                        lines = file.readlines()

                    for i in range(len(lines)):
                        if lines[i].startswith('LOGIN='):
                            lines[i] = f'LOGIN={cpf}\n'
                        elif lines[i].startswith('PASSWORD='):
                            lines[i] = f'PASSWORD={password}\n'

                    with open('src/.env', 'w') as file:
                        file.writelines(lines)

                    print('Credenciais atualizadas com sucesso!')
                    return

                elif select == 9:
                    self.activate_format('Encerrando sistema')
                    return
                
                else:
                    self.wrong_option()

            except ValueError:
                self.wrong_option()
            
            except Exception as error:
                print('Erro ao executar ação solicitada. Tente novamente.')
                print('Erro:', error)
                

if __name__ == '__main__':
    menu = Menu()
    menu.init()
