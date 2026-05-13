from google.adk.agents.llm_agent import Agent   
from trello import TrelloClient
from dotenv import load_dotenv
from datetime import datetime
import os

load_dotenv()

API_KEY = os.getenv('TRELLO_API_KEY')
API_SECRET = os.getenv('TRELLO_API_SECRET')
TOKEN = os.getenv('TRELLO_TOKEN')


def get_temporal_context():
    now = datetime.now()
    return now.strftime('%Y-%m-%d %H:%M:%S')


def adicionar_tarefa(nome_da_task: str, descricao_da_task: str, due_date: str):
    client = TrelloClient(
        api_key=API_KEY,
        api_secret=API_SECRET,
        token=TOKEN
    )

    boards = client.list_boards()
    meu_board = [b for b in boards if b.name == 'NOME-SEU-PROJETO-DIO'][0]

    listas = meu_board.list_lists()
    minha_lista = [l for l in listas if l.name.upper() in ['TO DO', 'A FAZER']][0]
    
    minha_lista.add_card(
        name=nome_da_task,
        desc=descricao_da_task,
        due=due_date
    )


def listar_tarefas(status: str = "todas"):
    client = TrelloClient(
        api_key=API_KEY,
        api_secret=API_SECRET,
        token=TOKEN
    )

    boards = client.list_boards()
    meu_board = [b for b in boards if b.name == 'NOME-SEU-PROJETO-DIO'][0]
    listas = meu_board.list_lists()        

    if status.lower() == "todas":
        listas_filtradas = listas
    elif status.lower() == "a fazer":
        listas_filtradas = [l for l in listas if l.name.upper() in ['A FAZER', 'TO DO', 'TODO']]
    elif status.lower() == "em andamento":
        listas_filtradas = [l for l in listas if l.name.upper() in ['EM ANDAMENTO', 'DOING']]
    elif status.lower() == "concluido":
        listas_filtradas = [l for l in listas if l.name.upper() in ['CONCLUÍDO', 'CONCLUIDO', 'DONE']]
    else:
        return "❌ Status inválido. Use: 'todas', 'a fazer', 'em andamento' ou 'concluido'."

    tarefas = []
    for lista in listas_filtradas:
        cards = lista.list_cards()
        for card in cards:
            tarefas.append({
                "nome": card.name,
                "descricao": card.desc,
                "vencimento": card.due,
                "status": lista.name,
                "id": card.id
            })
    
    return tarefas


def mudar_status_tarefa(nome_da_task: str, novo_status: str) -> str:
    try:
        client = TrelloClient(
            api_key=API_KEY,
            api_secret=API_SECRET,
            token=TOKEN
        )

        boards = client.list_boards()
        meu_board = [b for b in boards if b.name == 'NOME-SEU-PROJETO-DIO'][0]
        listas = meu_board.list_lists()
                       
        # CORREÇÃO: expandi status_map para aceitar variações
        status_map = {
            "a fazer": ["A FAZER", "TO DO", "TODO"],
            "em andamento": ["EM ANDAMENTO", "DOING"],
            "concluido": ["CONCLUÍDO", "CONCLUIDO", "DONE"]
        }
        
        nome_lista_destino = status_map.get(novo_status.lower())
        if not nome_lista_destino:
            return f"❌ Status inválido. Use: 'a fazer', 'em andamento' ou 'concluido'"
        
        lista_destino = next(
            (l for l in listas if l.name.upper() in [n.upper() for n in nome_lista_destino]), 
            None
        )

        if not lista_destino:
            return f"❌ Lista '{novo_status}' não encontrada no board"
        
        card_encontrado = None
        lista_origem = None

        for lista in listas:
            cards = lista.list_cards()
            card_encontrado = next(
                (c for c in cards if c.name.lower() == nome_da_task.lower()), 
                None
            )
            if card_encontrado:
                lista_origem = lista
                break
        
        if not card_encontrado:
            return f"❌ Card '{nome_da_task}' não encontrado"
        
        card_encontrado.change_list(lista_destino.id)
        return f"✅ '{nome_da_task}': {lista_origem.name} → {lista_destino.name}"
    except Exception as e:
        return f"❌ Erro: {str(e)}"


def remover_tarefa(nome_da_task: str) -> str:
    client = TrelloClient(api_key=API_KEY, api_secret=API_SECRET, token=TOKEN)
    boards = client.list_boards()
    meu_board = [b for b in boards if b.name == 'NOME-SEU-PROJETO-DIO'][0]
    listas = meu_board.list_lists()
    
    for lista in listas:
        cards = lista.list_cards()
        card_encontrado = next((c for c in cards if c.name.lower() == nome_da_task.lower()), None)
        if card_encontrado:
            card_encontrado.delete()
            return f"✅ Tarefa '{nome_da_task}' removida com sucesso."
    return f"❌ Tarefa '{nome_da_task}' não encontrada."


root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='Agente de Organização de Tarefas',
    instruction="""
        Você é um agente de organização de tarefas.     
        Sua função é receber uma tarefa e criar um card no Trello com o nome e descrição da tarefa.
        Você deve me perguntar as atividades que tenho no dia e criar um card para cada uma delas.
        Você inicia a conversa assim que for ativado, perguntando quais são as tarefas do dia.
        Sempre inicie a conversa perguntando quais são as tarefas do dia informando a data pela tool get_temporal_context, 
        e depois vá perguntando se tem mais alguma tarefa, até que o usuário diga que não tem mais tarefas.
        Suas funções:
         1. Adicionar novas tarefas com nome e descrição
         2. Listar todas as tarefas ou filtrar por status
         3. Marcar tarefas como concluídas
         4. Remover tarefas da lista
         5. Mudar o status da tarefa (ex: de "A Fazer" para "Em Andamento" e de "Em Andamento" para "Concluído")
         6. Gerar contexto temporal (data e hora atual) para organizar as tarefas do dia
""",
    tools=[get_temporal_context, adicionar_tarefa, listar_tarefas, mudar_status_tarefa, remover_tarefa],
)
