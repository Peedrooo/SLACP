import sys
from bot import Bot
import pandas as pd
from resources import tribunais, clean_terminal
from time import sleep
from assertiva import AssertivaApi    
import os

class Menu():

    select = 0

    def line(self):
        print('-=' * 33)

    def small_line(self):
        print('-=' * 16)

    def initial(self):
        clean_terminal()
        self.line()
        print('Seja Bem Vindo ao SLACP - Sistema L4 Ativos Coletor de Precatórios')
        self.line()

    def wrong_option(self):
        self.small_line()
        print('Opção inválida, tente novamente.')
        self.small_line()

    def activate_format(self, service):
        clean_terminal()
        self.small_line()
        print(service)
        self.small_line()
        print()

    def verify_file(self):
        try:
            df = pd.read_excel('buffer.xlsx')
            try:
                last_page = max(df['Página'])
            except Exception:
                return 1
            return last_page + 1
        except FileNotFoundError:
            return False
    
    def clean_buffer(self):
        try:
            os.remove('buffer.xlsx')
        except FileNotFoundError:
            pass

    def init(
        self, qnt_prec=0, user_page='0',
        continuation=False, URL=tribunais[1],
    ):
        self.qnt_prec = qnt_prec
        self.select = 0
        self.user_page = user_page
        self.tribunal = 0
        self.file = self.verify_file()
        self.URL = URL
        self.continuation = continuation

        while True:
            try:
                try:
                    self.initial()
                    print('Para forçar o encerramento do sistema, pressione Ctrl + C')
                    print('1 - Coletar Precatórios')
                    print('2 - Preencher Contatos')
                    print('3 - Atualizar Credenciais')
                    print('4 - Limpar Buffer')
                    print('0 - Encerrar')
                    if len(sys.argv) > 1:
                        select = int(sys.argv[1])
                        print('Opção desejada:', select)
                    else:
                        select = int(input('Opção desejada: '))

                    if select == 1:
                        self.activate_format('Iniciando coleta de Precatórios')
                        
                        key = input('Por qual palavra chave deseja buscar os Precatórios? ')

                        while self.qnt_prec == 0:
                            try:
                                self.qnt_prec = int(
                                    input('Digite a quantidade de Precatórios que deseja coletar: '))
                            except ValueError:
                                print('Digite um número natual válido.')

                        continuation = False

                        if self.file:
                            continuation = input(
                                'Observei que o programa estava em execução Anteriormente \nGostaria de continuar de onde parou? (1 - Sim, 2 - Não): ')
                            self.user_page = self.file if continuation == '1' else '0'

                        while self.user_page == '0':
                            try:
                                self.user_page = int(
                                    input('Digite a página que deseja iniciar a coleta: '))
                                if self.user_page == 0:
                                    self.user_page = 1

                            except ValueError:
                                print('Digite um número natual válido.')

                        continuation = True if continuation == '1' else False
                        bot = Bot(
                            self.qnt_prec, self.user_page,
                            continuation, URL = self.URL,
                            key = key
                            )

                        self.activate_format('Ativando Bot')

                        while True:
                            
                            try:
                                bot.run()
                                break
                            except Exception as error:
                                self.activate_format('Erro Detectado - Reiniciando Bot')
                                bot.close()
                                
                                if self.verify_file() < int(self.user_page):
                                    self.file = int(self.user_page)
                                else:
                                    self.file = self.verify_file()
                                
                                bot = Bot(
                                    self.qnt_prec, self.file,
                                    True, self.URL,
                                    key = key
                                )
                                pass

                        self.activate_format('Encerrando sistema')
                        return

                    elif select == 2:
                        self.activate_format('Preenchendo Contatos')
                        sleep(1)
                        assertiva = AssertivaApi()
                        if not assertiva.error:
                            assertiva.post_number_by_name()
                        else:
                            print('Erro ao conectar com a API da Assertiva')
                            sleep(2)
                        continue

                    elif select == 3:
                        self.activate_format('Atualizando Credenciais')

                        cpf = input('Digite o novo CPF: ')
                        password = input('Digite a nova senha: ')

                        salvar = input('Deseja salvar as novas credenciais? (1 - Sim, 2 - Não): ')
                        if salvar == '1':
                            with open('src/resources.py', 'r') as file:
                                lines = file.readlines()

                            for i in range(len(lines)):
                                if lines[i].startswith('LOGIN='):
                                    lines[i] = f'LOGIN={cpf}\n'
                                elif lines[i].startswith('PASSWORD='):
                                    lines[i] = f'PASSWORD={password}\n'

                            with open('src/resources.py', 'w') as file:
                                file.writelines(lines)

                            print('Credenciais atualizadas com sucesso!')
                        else:
                            print('Credenciais não atualizadas.')

                        sleep(2)
                        continue

                    elif select == 4:
                        self.activate_format('Limpando Buffer')
                        self.clean_buffer()
                        sleep(2)
                        continue

                    elif select == 0:
                        self.activate_format('Encerrando sistema')
                        return

                    else:
                        self.wrong_option()
                        sleep(2)
                        continue

                except ValueError:
                    self.wrong_option()
                    sleep(2)
                    continue

            except Exception as error:
                print('\nErro Detectado:')
                print('Reiniciando o sistema com as configurações anteriores...\n')
                print(error)


if __name__ == '__main__':
    menu = Menu()
    while True:
        try:
            menu.init()
            break
        except Exception as error:
            print('ERRO INESPERADO - contate o desenvolvedor')
            print('ERRO: ',error, '\n')

            fall = input(
                'Gostaria de reiniciar o sistema? (1 - Sim, 2 - Não): '
                )
            
            if fall == '2':
                break
            else:
                continue
