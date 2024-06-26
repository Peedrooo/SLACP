# SLACP
Sistema L4 Ativos Coletor de Precatórios

## Como Rodar o Projeto - Desenvolvimento

### Pré-requisitos
1. Instale o [Python 3.11](https://www.python.org/downloads/)
2. Instale o [Git](https://git-scm.com/downloads)

### Clonar o Projeto
1. Abra o terminal e navegue até a pasta onde deseja clonar o projeto
2. Clone o projeto com o comando:

```bash
git clone https://github.com/Peedrooo/SLACP.git
```

### Ambiente Virtual
1. Dentro da pasta do projeto, crie e ative o ambiente virtual com o comando:

```bash
python -m venv .venv
.venv/Scripts/activate
```

### Instalar Dependências
1. Instale as dependências do projeto com o comando:

```bash
pip install -r src/requirements.txt
```

### Atualizar .env-example
1. Renomeie o arquivo `.env-example` para `.env`
2. Preencha as variáveis de ambiente com as informações necessárias

### Rodar o Projeto
1. Rode o projeto com o comando:

```bash
python src/main.py
```

