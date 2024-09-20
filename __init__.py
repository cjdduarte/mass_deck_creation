from aqt import mw
from aqt.utils import showInfo, showWarning, askUser
from aqt.qt import QAction, QDialog, QVBoxLayout, QTextEdit, QPushButton, QHBoxLayout

# Função para validar a estrutura inserida pelo usuário
def validar_estrutura(estrutura):
    lines = estrutura.strip().split("\n")
    for line in lines:
        # Verifica se o nome do deck está vazio
        if len(line.strip()) == 0:
            return False
        
        # Verifica se há um uso inválido de ":" (somente um ":" ou mais de dois ":::" ou "::" no início/fim)
        if line.startswith("::") or line.endswith("::") or line.endswith(":") or ":::" in line or ":" in line and "::" not in line:
            # Pergunta ao usuário se deseja continuar com o formato incorreto
            if not askUser(f'The deck "{line}" contains an invalid number of colons (either ":" or ":::" are not allowed, '
                           'and "::" cannot be at the start or end).\n\n'
                           'Do you want to edit the structure and correct the format?'):
                return False
    return True

# Função para criar os decks a partir da estrutura inserida
def criar_decks(estrutura):
    # Separar a estrutura em linhas
    decks = estrutura.strip().split("\n")

    # Iterar pela lista de decks e criar cada um
    for nome_deck in decks:
        nome_deck = nome_deck.strip()
        if nome_deck and not mw.col.decks.id(nome_deck):
            # Cria o deck se ele ainda não existir
            mw.col.decks.id(nome_deck)

    # Atualiza a interface do Anki para mostrar os novos decks
    mw.reset()
    showInfo("Decks created successfully!")

# Função para exibir o diálogo de entrada de múltiplas linhas
# Agora passa o texto anterior para reutilizar caso o usuário queira voltar para edição
def pedir_estrutura(texto_anterior=None):
    # Criar um diálogo personalizado
    dialog = QDialog(mw)
    dialog.setWindowTitle("Enter the Deck Structure")
    
    # Layout do diálogo
    layout = QVBoxLayout()
    
    # Usa o texto anterior se for fornecido, senão usa o exemplo padrão
    exemplo_estrutura = texto_anterior if texto_anterior else (
        "Deck1::Subdeck1\n"
        "Deck1::Subdeck2\n"
        "Deck2\n"
        "Deck2::Subdeck1"
    )
    
    # Caixa de texto multilinha
    text_edit = QTextEdit()
    text_edit.setPlainText(exemplo_estrutura)
    layout.addWidget(text_edit)
    
    # Criar layout horizontal para os botões
    button_layout = QHBoxLayout()

    # Botão OK
    btn_ok = QPushButton("OK")
    button_layout.addWidget(btn_ok)

    # Botão Cancelar
    btn_cancel = QPushButton("Cancel")
    button_layout.addWidget(btn_cancel)

    # Adicionar o layout de botões ao layout principal
    layout.addLayout(button_layout)

    # Conectar o clique dos botões OK e Cancelar
    btn_ok.clicked.connect(dialog.accept)
    btn_cancel.clicked.connect(dialog.reject)

    # Definir o layout no diálogo
    dialog.setLayout(layout)
    
    # Mostrar o diálogo e processar o resultado
    if dialog.exec() == 1:  # Verifica se o botão OK foi pressionado (1 é QDialog.Accepted)
        # Obter o texto da caixa de texto
        estrutura = text_edit.toPlainText().strip()
        
        # Verificar se a estrutura é válida
        if validar_estrutura(estrutura):
            criar_decks(estrutura)
        else:
            # Reabre o diálogo de edição com o texto inserido pelo usuário
            pedir_estrutura(estrutura)

# Função para adicionar o item ao menu
def add_menu_item():
    action = QAction("Mass Deck Creation", mw)
    action.triggered.connect(pedir_estrutura)
    mw.form.menuTools.addAction(action)

# Adiciona o item ao menu ao iniciar o Anki
add_menu_item()
