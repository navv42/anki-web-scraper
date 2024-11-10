# Web Vocabulary Scraper to Anki Deck 

## Overview

Allows user to dynamically import new **Language** entries into an existing ANKI deck from any data source online, utilizing gen AI. 

Say you see a nice vocabulary list on your favorite website for studying a new language and want to quickly import all terms into your current ANKI deck, look no further than this repo!

## Features
- Automatically extracts vocabulary terms from HTML content.
- Allows user-defined headers and example entries for flexible extraction and improved accuracy.
- Adds extracted terms directly to an Anki deck via AnkiConnect.
- Interactive command-line interface with error handling.

## Setup

### Prerequisites
- **Python 3.7+**
- **Anki** with **AnkiConnect** (must be installed and running).
- **Dependencies**: Install with:
  ```
  pip install -r requirements.txt
  ```

## Usage
Run the main script with:
```
bash run.sh
```

Follow the prompts to:
- Select an Anki Deck
- Define vocabulary headers that corresponse to **Target Langauge**, **Own Language**, and **Phonetic** fields in Anki
- Add an example value for these headers (perhaps the first vocab term on your list)
- Input HTML content for extraction 

## Example Run

![Demo of Script Usage](assets/example_run.gif)

## Project Structure

anki-web-scraper/
├── add_vocab/
│   ├── __init__.py
│   ├── anki_add.py       # Manages Anki deck interactions
│   ├── gen_vocab.py      # Handles vocabulary extraction from HTML
│   └── main.py           # Orchestrates user interaction and main workflow
│   └── scrape.py         # Dev script to scrape website content, but non-functional atm
├── run.sh                # Entry point to run the application
├── requirements.txt      # List of dependencies
└── README.md             # Project overview and instructions

## Reasoning 

Tried to just scrape the website data, but many websites require login to fully see static HTML, so decided to implement solution where user copies static HTML over. 

## TODO

