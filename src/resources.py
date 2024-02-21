import os

tribunais = {
    1: 'https://pje1g.trf1.jus.br/pje/login.seam',
    3: 'https://pje1g.trf3.jus.br/pje/login.seam',
    5: 'https://pje1g.trf5.jus.br/pje/login.seam',
    6: 'https://pje1g.trf6.jus.br/pje/login.seam',
    7: 'https://pje.tjdft.jus.br/pje/login.seam'
}

def clean_terminal():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
