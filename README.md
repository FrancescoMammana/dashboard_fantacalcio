# 🏆 Dashboard Fantacalcio - Wins for Life

Dashboard interattiva Streamlit per la gestione delle rose del fantacalcio con calcolo automatico dei crediti residui e gestione degli svincolati.

## 📋 Funzionalità

### 1. Gestione Rose Squadre
- **Importazione automatica** di tutte le squadre dal file Excel (Scarponi, N.S., Fantateone, Skubys Sonics, Tanaka's Team, OR.PA.S., Villareal, The Hangover, SS Longobarda, Dynamo CM)
- **Calcolo crediti residui** con bonus automatico per giocatori con asterisco (*): `ceil(costo/2)` aggiunto ai crediti base
- **Visualizzazione per ruolo**: Portieri (P), Difensori (D), Centrocampisti (C), Attaccanti (A)

### 2. Colonne Editabili
- **Svincolare?** - Checkbox (default: `True` per giocatori con asterisco)
- **Importo_Pagato** - Input numerico (default: 1)

### 3. Sidebar Informativa
- **Crediti Residui Totali** - Calcolo dinamico basato su crediti base + bonus asterischi
- **Costo Totale Rosa** - Somma degli importi pagati
- **Conta Svincolati per Ruolo** - P/D/C/A separati

### 4. Tab Svincolati
- **Filtro per ruolo** - Dropdown per selezionare P/D/C/A o visualizzare tutti
- **Ordinamento FVM** - Decrescente (migliori giocatori in cima)
- **Dati dal foglio Svincolati** - Nome, Squadra, Ruolo, PGv, MV, FM, FVM
- **Top 10 FVM** - Tabella riepilogativa dei migliori svincolati

### 5. Tema Scuro Professionale
- Design moderno con tema scuro
- Colori professionali e leggibili
- Layout responsive e ottimizzato

## 🚀 Installazione e Avvio

### Prerequisiti
- Python 3.8+
- File Excel: `Rose_wins-for-life_updated.xlsx`

### Installazione Dipendenze

```bash
pip install -r requirements.txt
```

### Avvio Dashboard

**Metodo 1: Script automatico**
```bash
./run_dashboard.sh
```

**Metodo 2: Comando diretto**
```bash
streamlit run dashboard_fantacalcio.py
```

La dashboard sarà disponibile su: **http://localhost:8501**

## 📊 Struttura File Excel

### Foglio "Rose"
- Contiene tutte le squadre con struttura:
  - Nome Squadra (es: "Scarponi")
  - Ruolo | Calciatore | Squadra | Costo
  - Giocatori con asterisco (*) nel nome
  - Crediti Residui: XX

### Foglio "Svincolati"
- Colonne: Nome, Sq., Ruolo, PGv, MV, FM, FVM
- Ordinabile per FVM (Fantamedia)

## 🎯 Caratteristiche Tecniche

### Calcolo Crediti Residui
```python
crediti_residui = crediti_base + Σ(ceil(costo_giocatore_asterisco / 2))
```

### Identificazione Giocatori con Asterisco
- Rilevamento automatico del carattere "*" nel nome
- Bonus calcolato automaticamente: `ceil(costo / 2)`
- Rimozione asterisco dal nome visualizzato

### Session State
- Persistenza dati durante la sessione
- Aggiornamento in tempo reale delle modifiche
- Sincronizzazione tra tab e sidebar

## 📦 File Inclusi

- `dashboard_fantacalcio.py` - Applicazione principale Streamlit
- `requirements.txt` - Dipendenze Python
- `run_dashboard.sh` - Script di avvio automatico
- `README.md` - Questo file

## 🎨 Personalizzazione

Il tema scuro può essere personalizzato modificando il CSS nella sezione `st.markdown()` del file principale.

## 🐛 Risoluzione Problemi

### Errore: File non trovato
Assicurati che il file `Rose_wins-for-life_updated.xlsx` sia nel percorso:
```
/mnt/user-data/uploads/Rose_wins-for-life_updated.xlsx
```

### Porta 8501 già in uso
Modifica la porta nel comando:
```bash
streamlit run dashboard_fantacalcio.py --server.port 8502
```

## 📝 Note

- I dati vengono caricati in cache per prestazioni ottimali
- Le modifiche sono temporanee (non salvate nel file Excel)
- La dashboard supporta tutte le 10 squadre del campionato

## 🏆 Squadre Supportate

1. Scarponi
2. N.S.
3. Fantateone
4. Skubys Sonics
5. Tanaka's Team
6. OR.PA.S.
7. Villareal
8. The Hangover
9. SS Longobarda
10. Dynamo CM

---

**Sviluppato per Wins for Life Fantasy League** ⚽
