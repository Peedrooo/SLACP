import requests
from resources import username, password
from time import sleep


class AssertivaApi:
    def __init__(self):
        self.url_token = 'https://api.assertivasolucoes.com.br/oauth2/v3/token'
        self.body_token = {
            'grant_type': 'client_credentials'
        }
        self.url_number_by_name = 'https://api.assertivasolucoes.com.br/localize/v3/nome'

        print('Gerando token para a API da Assertiva...')
        self.token = self.get_token()['access_token']
        print('Token gerado com sucesso!')

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

    def get_number_by_name(self, name):
        url = self.url_number_by_name.replace('nome', name)
        headers = {
            'Authorization': f'Bearer {self.token}'
        }
        response = requests.get(
            url,
            headers=headers
        )
        return response.json()
    

    def post_number_by_name(self, df):
        df['Nome Processado'] = df['Nome'].apply(lambda x: x.split('e')[0])
        df['Numero Contato'] = df['Nome Processado'].apply(lambda x: self.get_number_by_name(x))


if __name__ == '__main__':
    api = AssertivaApi()
    print(api.token)
    print(api.get_number_by_name('Pedro Vitor Augusto de Jesus'))
