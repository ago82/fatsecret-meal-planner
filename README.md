# fatsecret-meal-planner

Script Python per compilare automaticamente il diario alimentare settimanale su FatSecret, usando i pasti salvati come template.

## Cosa fa

Ogni volta che lo lanci, compila il diario alimentare della **settimana successiva** (da lunedì a domenica) copiando i pasti salvati nel giorno corretto. Funziona qualsiasi giorno tu lo lanci.

## Struttura del progetto

```
fatsecret-meal-planner/
├── compilaDieta.py        # Script principale
├── fatsecret_token.json   # Token OAuth (NON committato)
├── .gitignore
├── README.md
└── OLD/
    └── getSavedMeals.py   # Script di utility usato per recuperare gli ID dei pasti salvati (NON committato)
```

## Requisiti

```
pip install requests requests-oauthlib
```

## Configurazione

### 1. Credenziali FatSecret Platform

Registrati come developer su [platform.fatsecret.com](https://platform.fatsecret.com) e ottieni:
- **Consumer Key** (OAuth 1.0)
- **Consumer Secret** (OAuth 1.0)

Inseriscili in `compilaDieta.py`:

```python
CONSUMER_KEY = "la_tua_key"
CONSUMER_SECRET = "il_tuo_secret"
```

### 2. Autenticazione (una volta sola)

Lancia `getSavedMeals.py` (nella cartella OLD) per autenticarti e recuperare gli ID dei tuoi pasti salvati. Lo script:
- Apre l'URL di autorizzazione FatSecret nel browser
- Chiede il PIN generato da FatSecret
- Salva il token in `fatsecret_token.json`
- Stampa tutti i pasti salvati con i loro ID

### 3. Configura il menu settimanale

In `compilaDieta.py`, aggiorna il dizionario `MENU` con gli ID dei tuoi pasti salvati:

```python
MENU = {
    0: [("ID_PRANZO", "lunch"), ("ID_CENA", "dinner")],  # Lunedì
    1: [("ID_PRANZO", "lunch"), ("ID_CENA", "dinner")],  # Martedì
    ...
}
```

## Utilizzo

```
python compilaDieta.py
```

Lo script compila pranzo, cena (e snack della domenica) per tutti e 7 i giorni della settimana successiva.

## Note

- Il token OAuth 1.0 di FatSecret non scade — si autentica una volta sola
- `fatsecret_token.json` contiene credenziali sensibili: non committarlo mai
- L'account FatSecret deve essere accessibile con email + password (non solo Google Login) per il flow OAuth 1.0
