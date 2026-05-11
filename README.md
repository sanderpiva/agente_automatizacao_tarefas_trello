# 📌 Agente de Organização de Tarefas com Trello e Python

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue)](https://www.python.org/)
[![Trello API](https://img.shields.io/badge/Trello-API_v1-green)](https://developer.atlassian.com/cloud/trello/)
[![License](https://img.shields.io/badge/license-MIT-lightgrey)](LICENSE)

Este projeto implementa um **Agente de Organização de Tarefas** em Python, integrado ao Trello, que permite adicionar, listar, atualizar status e remover tarefas diretamente de boards e listas do Trello.

---

## 🚀 Funcionalidades

- **Adicionar tarefas** com nome, descrição e data de vencimento  
- **Listar tarefas** filtrando por status (`a fazer`, `em andamento`, `concluido`)  
- **Mudar status** de uma tarefa entre listas  
- **Remover tarefas** do board  
- **Gerar contexto temporal** (data e hora atual)  

---

## 📂 Estrutura do Script

O script principal (`main.py`) contém:

### Funções utilitárias

- `get_temporal_context`
- `adicionar_tarefa`
- `listar_tarefas`
- `mudar_status_tarefa`
- `remover_tarefa`

### Configuração

- Credenciais via `.env`
- Instanciação do `root_agent` usando a biblioteca `google.adk`

---

## 🛠️ Pré-requisitos

- Conta ativa no Trello  
- Python 3.7 ou superior  
- `pip` instalado  
- Navegador web para autorizar o app  

---

## 📦 Instalação

Crie um arquivo `requirements.txt` com:

```txt
google-adk
py-trello
python-dotenv
```

Depois execute:

```bash
pip install -r requirements.txt
```

---

## ⚙️ Criando o ambiente `.lab-dio`

Para manter o projeto isolado e organizado, crie um ambiente virtual chamado `.lab-dio`:

### Criar o ambiente virtual

```bash
python -m venv .lab-dio
```

### Ativar no PowerShell (Windows)

```powershell
.\.lab-dio\Scripts\Activate.ps1
```

### Ativar no Linux/Mac

```bash
source .lab-dio/bin/activate
```

---

## 🔑 Registro e Autorização no Trello

### 1. Criar Power-Up

Acesse o portal oficial:

https://trello.com/power-ups/admin

Crie um novo app e configure:
- Nome
- Workspace
- Informações de contato

---

### 2. Obter API Key

Na página de gerenciamento do app:
- Copie sua **API Key**
- Copie o **API Secret**

---

### 3. Gerar Token

Use a URL abaixo substituindo `SUA_API_KEY`:

```txt
https://trello.com/1/authorize?expiration=never&name=AppDio&scope=read,write&response_type=token&key=SUA_API_KEY
```

Autorize o acesso e copie o token exibido.

---

## ⚙️ Configurar `.env`

Crie um arquivo `.env` na raiz do projeto:

```env
TRELLO_API_KEY=sua_chave_aqui
TRELLO_API_SECRET=seu_secret_aqui
TRELLO_TOKEN=seu_token_aqui
```

---

## 📜 Exemplo de Uso

### Adicionar tarefa

```python
adicionar_tarefa(
    "Estudar Python",
    "Revisar módulo de Trello API",
    "2026-05-12"
)
```

### Listar tarefas

```python
print(listar_tarefas("todas"))
```

### Mudar status

```python
print(mudar_status_tarefa(
    "Estudar Python",
    "em andamento"
))
```

### Remover tarefa

```python
print(remover_tarefa("Estudar Python"))
```

---

## 🖼️ Seção de Fotos

Como exemplo do agente04 em operação, a partir das imagens da pasta `img/`, ilustro parte do seu funcionamento:

![p1](https://github.com/sanderpiva/agente_automatizacao_tarefas_trello/blob/master/agente_automatizacao_tarefas_trello/img/1.PNG)

![p2](https://github.com/sanderpiva/agente_automatizacao_tarefas_trello/blob/master/agente_automatizacao_tarefas_trello/img/2.PNG)

![p3](https://github.com/sanderpiva/agente_automatizacao_tarefas_trello/blob/master/agente_automatizacao_tarefas_trello/img/3.PNG)

![p4](https://github.com/sanderpiva/agente_automatizacao_tarefas_trello/blob/master/agente_automatizacao_tarefas_trello/img/4.PNG)

---

## 📚 Referências

- Documentação Trello API  
  https://developer.atlassian.com/cloud/trello/

- py-trello  
  https://github.com/sarumont/py-trello

---

## 📌 Informações do Projeto

- **Última atualização:** Maio 2026  
- **Versão da API Trello:** v1  
- **Python:** 3.7+  
- **Licença:** MIT  

## IMPORTANTE 

- Assim como relatou o instrutor Henrique nas videoaulas, o Trello sempre subtrai '1' da data do registro da tarefa (Ex: 11 de maio de  2026, passa a ser 10 maio de 2026). Quando descobrir uma solução para esse pequeno problema pontual, farei uma atualização no repositório. Agradeço a compreenção de todos.
---

**Autor** Sander Gustavo Piva
