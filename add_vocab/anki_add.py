import json
import urllib.request
from add_vocab.gen_vocab import get_vocab

def request(action, **params):
    return {'action': action, 'params': params, 'version': 6}

def invoke(action, **params):
    requestJson = json.dumps(request(action, **params)).encode('utf-8')
    response = json.load(urllib.request.urlopen(urllib.request.Request('http://127.0.0.1:8765', requestJson)))
    if len(response) != 2:
        raise Exception('response has an unexpected number of fields')
    if 'error' not in response:
        raise Exception('response is missing required error field')
    if 'result' not in response:
        raise Exception('response is missing required result field')
    if response['error'] is not None:
        raise Exception(response['error'])
    return response['result']

def add_notes(deck_name, model_name, vocabulary):
    """
    Adds multiple notes to Anki
    """
    notes = []
    for entry in vocabulary:
        fields = {
            "Target Language": entry["script"],  # Farsi script
            "Own Language": entry["english"],  # English translation
            "Phonetic": entry["persian"]  # Transliteration
        }
        
        # Create note object
        note = {
            'deckName': deck_name,
            'modelName': model_name,
            'fields': fields,
            'options': {
                'allowDuplicate': False
            },
            'tags': ['imported_from_ai']
        }
        notes.append(note)
    
    # Invoke addNotes to add all notes at once
    result = invoke('addNotes', notes=notes)
    if result:
        for term in vocabulary:
            print(f"Added term: {term}")
        print("Success: All terms added to the deck.")
    else:
        print("ANKI Error: Failed to add notes.")
