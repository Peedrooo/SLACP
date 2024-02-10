class PostProcesser:
    def __init__(self, data):
        self.data = data

    def process(self):
        df = self.data
        df[df['Precatório']][['Numero', 'Nome', 'CPF', 'Precatório']]
        return df
    
    def run(self):
        return self.process()