class PostProcesser:
    def __init__(self, data):
        self.data = data

    def process(self):
        try:
            df = self.data
            df = df[df['Precatório']][['Numero', 'Nome','Polo Passivo','Página']]
            return df
        except:
            return None

    def run(self):
        return self.process()
