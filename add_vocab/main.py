import sys
import threading
import time
from itertools import cycle
from add_vocab.gen_vocab import get_vocab
from add_vocab.anki_add import invoke, add_notes

STOP_SPINNER = False

def spinner(message="Processing..."):
    """Display a spinner animation while a task is in progress."""
    spinner_symbols = cycle(['|', '/', '-', '\\'])
    print(message, end=" ", flush=True)
    
    while not STOP_SPINNER:
        sys.stdout.write(next(spinner_symbols))
        sys.stdout.flush()
        sys.stdout.write('\b')
        time.sleep(0.1)
    
    sys.stdout.write(" \b")

def main():
    global STOP_SPINNER

    # Step 1: Fetch and display available decks
    print("Fetching list of decks...")
    decks = invoke('deckNames')
    print("Available decks:", decks)
    
    # Step 2: Select a deck
    deck_name = input("Please select a deck from the above list: ")

    # Step 3: Prompt for headers
    headers = [header.strip() for header in input("Please provide the headers for the vocabulary terms (comma-separated): ").split(',')]

    # Step 4: Get example entries for each header
    target_fields, example_entry = {}, []
    for header in headers:
        target = input(f"For '{header}', what is the corresponding Anki field? ")
        target_fields[target] = header
        entry = input(f"Please provide an example entry for '{header}': ")
        example_entry.append(entry)

    # Step 5: Get HTML content
    print("Please paste the HTML content (press Ctrl+D or Ctrl+Z when finished):")
    html_content = []
    try:
        while True:
            line = input()
            html_content.append(line)
    except EOFError:
        pass
    html_content = "\n".join(html_content)

    # Step 6: Analyze HTML structure and get vocabulary data
    vocab_data = None
    spinner_thread = threading.Thread(target=spinner, args=("Analyzing HTML structure and generating vocabulary data...",))
    spinner_thread.start()
    
    try:
        vocab_data = get_vocab(headers, example_entry, html_content)
        print(vocab_data)
    finally:
        STOP_SPINNER = True  
        spinner_thread.join()  
    
    print("\n")  

    if not vocab_data:
        print("Error: Failed to analyze HTML structure.")
        return
    
    print("Please review the extracted vocabulary data above.\n")
    confirmation = input("Do you want to add these notes to the deck? (y/n): ").strip().lower()
    if confirmation != 'y':
        print("Operation cancelled by user.")
        return
    
    # Step 7: Add notes to the selected deck
    add_notes(deck_name, "Language", target_fields, vocab_data['vocabulary'])

if __name__ == "__main__":
    main()