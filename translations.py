from aqt.qt import QLocale
from aqt import mw

# Supported languages / Fallback language
SUPPORTED_LANGUAGES = ["en", "pt_BR"]
FALLBACK_LANGUAGE = "en"

def get_language_code():
    """Gets the current language code from Anki's settings or system locale."""
    try:
        # Try to get language from Anki's settings first
        lang_code = mw.pm.meta.get('defaultLang', None)
        if lang_code:
            if lang_code.startswith("pt"):
                return "pt_BR"
            elif lang_code.startswith("en"):
                return "en"
            # Add other language codes if needed
    except AttributeError: # mw or mw.pm might not be available
        pass

    # Fallback to system locale if Anki's setting is not available or not specific enough
    system_lang = QLocale().name() # e.g., "pt_BR" or "en_US"
    if system_lang.startswith("pt"):
        return "pt_BR"
    elif system_lang.startswith("en"):
        return "en"
    
    return FALLBACK_LANGUAGE

translations = {
    "en": {
        "invalid_colon_warning_title": "Invalid Structure",
        "invalid_colon_warning_message": "The deck \"{line}\" contains an invalid number of colons (either \":\" or \":::\" are not allowed, and \"::\" cannot be at the start or end).\n\nDo you want to edit the structure and correct the format?",
        "decks_created_successfully": "Decks created successfully!",
        "dialog_title_enter_deck_structure": "Enter the Deck Structure",
        "example_deck_structure": "Deck1::Subdeck1\nDeck1::Subdeck2\nDeck2\nDeck2::Subdeck1",
        "button_ok": "OK",
        "button_cancel": "Cancel",
        "menu_action_mass_deck_creation": "Mass Deck Creation"
    },
    "pt_BR": {
        "invalid_colon_warning_title": "Estrutura Inválida",
        "invalid_colon_warning_message": "O baralho \"{line}\" contém um número inválido de dois-pontos (\":\" ou \":::\" não são permitidos, e \"::\" não pode estar no início ou no fim).\n\nDeseja editar a estrutura e corrigir o formato?",
        "decks_created_successfully": "Baralhos criados com sucesso!",
        "dialog_title_enter_deck_structure": "Insira a Estrutura dos Baralhos",
        "example_deck_structure": "Baralho1::Sub-baralho1\nBaralho1::Sub-baralho2\nBaralho2\nBaralho2::Sub-baralho1",
        "button_ok": "OK",
        "button_cancel": "Cancelar",
        "menu_action_mass_deck_creation": "Criação em Massa de Baralhos"
    }
}

current_lang_code = get_language_code()

def tr(key, **kwargs):
    """Translates a key to the current language with optional parameter substitution."""
    # Ensure current_lang_code is one of the supported, otherwise fallback
    lang_to_use = current_lang_code if current_lang_code in SUPPORTED_LANGUAGES else FALLBACK_LANGUAGE
    
    # Get the dictionary for the determined language, or fallback language's dict
    lang_dict = translations.get(lang_to_use, translations[FALLBACK_LANGUAGE])
    
    # Get the specific translation, or the key itself as a fallback
    text_template = lang_dict.get(key, key)
    
    try:
        return text_template.format(**kwargs) if kwargs else text_template
    except KeyError as e:
        # This can happen if a placeholder in the string (e.g., "{line}") 
        # is not provided in kwargs. Return the template with a warning.
        print(f"Translation warning: Missing key {e} for template '{key}' in language '{lang_to_use}'.")
        return text_template # Or return a more specific error message 