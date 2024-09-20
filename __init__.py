from aqt import mw
from aqt.utils import showInfo, showWarning, askUser
from aqt.qt import QAction, QDialog, QVBoxLayout, QTextEdit, QPushButton, QHBoxLayout

# Função para validar a estrutura inserida pelo usuário
def validar_estrutura(estrutura):
    lines = estrutura.strip().split("\n")
    for line in lines:
        # Verifica se há uso incorreto do "::" (por exemplo, "::Deck" ou "Deck::")
        if "::" in line:
            if line.startswith("::") or line.endswith("::"):
                return False
        # Verifica se o nome do deck está vazio
        if len(line.strip()) == 0:
            return False
        # Verifica se há um ou mais de dois ":"
        num_colons = line.count(":")
        if num_colons == 1 or num_colons > 2:
            # Pergunta ao usuário se deseja continuar mesmo assim
            if not askUser(f'The deck "{line}" contains {num_colons} colon(s). '
                           f'The standard is "::". Do you want to continue with this format?'):
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
def pedir_estrutura():
    # Criar um diálogo personalizado
    dialog = QDialog(mw)
    dialog.setWindowTitle("Enter the Deck Structure")
    
    # Layout do diálogo
    layout = QVBoxLayout()
    
    # Texto de exemplo
    exemplo_estrutura = (
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
            showWarning("The structure is invalid. Please follow the correct format.")

# Função para adicionar o item ao menu
def add_menu_item():
    action = QAction("Mass Deck Creation", mw)
    action.triggered.connect(pedir_estrutura)
    mw.form.menuTools.addAction(action)

# Adiciona o item ao menu ao iniciar o Anki
add_menu_item()
