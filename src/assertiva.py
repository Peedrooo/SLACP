import requests
from time import sleep
from pandas import read_excel
from resources import password, username


class AssertivaApi:
    def __init__(self):
        self.url_token = 'https://api.assertivasolucoes.com.br/oauth2/v3/token'
        self.body_token = {
            'grant_type': 'client_credentials'
        }
        self.url_cpf_by_name = 'https://api.assertivasolucoes.com.br/localize/v3/nome-endereco?buscarPor=ambas&nomeOuRazaoSocial=name&idFinalidade=1'
        self.url_telefone_by_cpf = 'https://api.assertivasolucoes.com.br/localize/v3/cpf?cpf=cpf&idFinalidade=1'
        print('Gerando token para a API da Assertiva...')
        try:
            self.token = self.get_token()['access_token']
            self.headers = {
                'Authorization': f'Bearer {self.token}'
            }
            print('Token gerado com sucesso!')
            self.error = False

        except:
            self.error = True
            print(
                'Erro ao gerar token! - Fora de horário comercial ou erro de credenciais!')

    def get_token(self):
        response = requests.post(
            self.url_token,
            data=self.body_token,
            auth=(username, password)
        )
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def get_cpf_by_name(self, name):
        url = self.url_cpf_by_name.replace('name', name)
        response = requests.get(
            url,
            headers=self.headers
        )

        response = response.json()
        print(response)
        if response['resposta'] == 'Não localizamos nenhuma pessoa ou empresa a partir dos dados informados.':
            return 'Não encontrado'

        people = response['resposta']['pessoaFisica']
        for person in people:
            if person['nome'].lower() == name.lower():
                return person['cpf']

        return 'Não encontrado'

    def get_number_by_cpf(self, cpf):
        if cpf == 'Não encontrado':
            return 'Não encontrado'

        url = self.url_telefone_by_cpf.replace('=cpf', f'={cpf}')
        response = requests.get(
            url,
            headers=self.headers
        )

        response = response.json()
        print(response)
        if response['resposta'] == 'Não localizamos nenhuma pessoa ou empresa a partir dos dados informados.':
            return 'Não encontrado'

        else:
            telefones = []
            telefone_fixo = response['resposta']['telefones']['fixos']
            telefone_movel = response['resposta']['telefones']['moveis']
            for telefone in telefone_fixo:
                telefones.append(telefone['numero'])
            for telefone in telefone_movel:
                telefones.append(telefone['numero'])

            return telefones

    def post_number_by_name(self):
        try:
            print('Lendo arquivo de precatorios...')
            sleep(2)
            df = read_excel('./precatorios.xlsx')
            print(df)
            sleep(2)
        except FileNotFoundError:
            print('precatorios.xlsx não encontrado!')
            sleep(2)
            return
        df['Nome Processado'] = df['Nome'].apply(lambda x: x.split(' e ')[0])
        df['Numero Contato'] = df['Nome Processado'].apply(
            lambda x: self.get_number_by_cpf(self.get_cpf_by_name(x)))
        df.to_excel('./precatorios.xlsx', index=False)


