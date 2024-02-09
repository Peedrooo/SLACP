import sys
from bot import Bot

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

    def init(self):
        self.initial()
        self.qnt_prec = 0
        while self.select != 3:
            try:
                print('1 - Coletar Precatórios')
                print('2 - Ativar API')
                print('3 - Encerrar')
                if len(sys.argv) > 1:
                    select = int(sys.argv[1])
                    print('Opção desejada:', select)
                else:
                    select = int(input('Opção desejada: '))

                if select == 1:
                    self.activate_format('Iniciando coleta de Precatórios')

                    while self.qnt_prec <= 0:
                        try:
                            self.qnt_prec = int(input('Digite a quantidade de Precatórios que deseja coletar: '))
                        except ValueError:
                            print('Digite um número natual válido.')

                    bot = Bot(self.qnt_prec)
                    return bot.run()
                
                elif select == 2:
                    self.activate_format('Ativando API')
                    return
                
                elif select == 3:
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
