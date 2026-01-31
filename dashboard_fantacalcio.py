import streamlit as st
import pandas as pd
import numpy as np
from math import ceil

# Configurazione pagina con tema scuro
st.set_page_config(
    page_title="Dashboard Fantacalcio - Wins for Life",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizzato per tema scuro professionale
st.markdown("""
<style>
    .main {
        background-color: #0e1117;
    }
    .stApp {
        background-color: #0e1117;
    }
    h1, h2, h3 {
        color: #fafafa;
    }
    .stDataFrame {
        background-color: #1e2130;
    }
    div[data-testid="stMetricValue"] {
        font-size: 24px;
        color: #00d4ff;
    }
    div[data-testid="stMetricLabel"] {
        color: #b0b0b0;
    }
    .css-1d391kg {
        background-color: #262730;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data(file_path):
    """Carica e processa i dati dal file Excel"""
    # Carica il foglio Rose
    df_raw = pd.read_excel(file_path, sheet_name='Rose', header=None)
    
    # Trova le righe che contengono i nomi delle squadre
    team_positions = []
    for idx, row in df_raw.iterrows():
        val = str(row[0]).strip()
        if val not in ['Ruolo', 'P', 'D', 'C', 'A', 'nan'] and not val.startswith('Crediti'):
            if pd.isna(row[1]) or row[1] == 'Calciatore':
                team_positions.append((idx, val))
    
    # Estrai i dati per ogni squadra
    all_teams_data = {}
    
    for i, (start_idx, team_name) in enumerate(team_positions):
        # Determina l'indice di fine (fino alla prossima squadra o fine file)
        if i < len(team_positions) - 1:
            end_idx = team_positions[i + 1][0]
        else:
            end_idx = len(df_raw)
        
        # Estrai i dati della squadra
        team_data = df_raw.iloc[start_idx:end_idx].copy()
        
        # Trova la riga con "Ruolo, Calciatore, Squadra, Costo"
        header_idx = None
        for idx in range(len(team_data)):
            if team_data.iloc[idx, 1] == 'Calciatore':
                header_idx = idx
                break
        
        if header_idx is not None:
            # Usa quella riga come header
            team_df = team_data.iloc[header_idx+1:].copy()
            team_df.columns = ['Ruolo', 'Calciatore', 'Squadra', 'Costo']
            
            # Rimuovi righe vuote e "Crediti Residui"
            team_df = team_df[team_df['Ruolo'].isin(['P', 'D', 'C', 'A'])].copy()
            
            # Converti Costo a numerico
            team_df['Costo'] = pd.to_numeric(team_df['Costo'], errors='coerce')
            
            # Rimuovi righe con NaN
            team_df = team_df.dropna(subset=['Ruolo', 'Calciatore', 'Costo'])
            
            # Trova i crediti residui
            crediti_residui = 0
            for idx in range(len(team_data)):
                val = str(team_data.iloc[idx, 0])
                if val.startswith('Crediti Residui'):
                    try:
                        crediti_residui = int(val.split(':')[1].strip())
                    except:
                        crediti_residui = 0
                    break
            
            # Identifica giocatori con "*" nel nome
            team_df['Ha_Asterisco'] = team_df['Calciatore'].astype(str).str.contains(r'\*', na=False)
            
            # Rimuovi "*" dal nome
            team_df['Calciatore'] = team_df['Calciatore'].astype(str).str.replace('*', '', regex=False)
            
            all_teams_data[team_name] = {
                'data': team_df.reset_index(drop=True),
                'crediti_base': crediti_residui
            }
    
    # Carica il foglio Svincolati
    df_svincolati = pd.read_excel(file_path, sheet_name='Svincolati')
    
    return all_teams_data, df_svincolati

def calculate_crediti_residui(team_df, crediti_base):
    """Calcola i crediti residui considerando i giocatori con asterisco"""
    bonus = 0
    for _, row in team_df.iterrows():
        if row['Ha_Asterisco']:
            bonus += ceil(row['Costo'] / 2)
    return crediti_base + bonus

def main():
    st.title("⚽ Dashboard Fantacalcio - Wins for Life")
    st.markdown("---")
    
    # File upload o path fisso
    file_path = 'rose.xlsx'
    
    try:
        # Carica i dati
        all_teams_data, df_svincolati = load_data(file_path)
        
        # Sidebar: Selezione squadra
        st.sidebar.header("🏆 Selezione Squadra")
        team_names = list(all_teams_data.keys())
        selected_team = st.sidebar.selectbox("Seleziona una squadra:", team_names)
        
        # Recupera i dati della squadra selezionata
        team_info = all_teams_data[selected_team]
        team_df = team_info['data'].copy()
        crediti_base = team_info['crediti_base']
        
        # Inizializza session state per le modifiche
        if 'team_data' not in st.session_state or st.session_state.get('current_team') != selected_team:
            st.session_state.team_data = team_df.copy()
            st.session_state.current_team = selected_team
            # Inizializza colonne editabili
            st.session_state.team_data['Svincolare'] = st.session_state.team_data['Ha_Asterisco']
            st.session_state.team_data['Importo_Pagato'] = 1
        
        team_df = st.session_state.team_data
        
        # Calcola crediti residui totali
        crediti_residui_totali = calculate_crediti_residui(team_df, crediti_base)
        
        # Conta svincolati per ruolo
        svincolati_per_ruolo = team_df[team_df['Svincolare'] == True].groupby('Ruolo').size().to_dict()
        
        # Costo totale basato su Importo_Pagato
        costo_totale = team_df['Importo_Pagato'].sum()
        
        # Sidebar: Metriche
        st.sidebar.markdown("---")
        st.sidebar.header("📊 Statistiche Squadra")
        st.sidebar.metric("💰 Crediti Residui Totali", f"{crediti_residui_totali}")
        st.sidebar.metric("💵 Costo Totale Rosa", f"{costo_totale}")
        
        st.sidebar.markdown("### Svincolati per Ruolo")
        for ruolo in ['P', 'D', 'C', 'A']:
            count = svincolati_per_ruolo.get(ruolo, 0)
            st.sidebar.metric(f"{ruolo}", count)
        
        # Tabs
        tab1, tab2 = st.tabs(["📋 Rosa Squadra", "🔄 Svincolati"])
        
        with tab1:
            st.header(f"Rosa: {selected_team}")
            
            # Mostra crediti base
            st.info(f"💰 **Crediti Base:** {crediti_base} | **Bonus da giocatori con *:** {crediti_residui_totali - crediti_base} | **Totale:** {crediti_residui_totali}")
            
            # Crea editor per la rosa
            st.subheader("Modifica Rosa")
            
            # Raggruppa per ruolo
            for ruolo in ['P', 'D', 'C', 'A']:
                st.markdown(f"### {ruolo} - Portieri" if ruolo == 'P' else f"### {ruolo} - {'Difensori' if ruolo == 'D' else 'Centrocampisti' if ruolo == 'C' else 'Attaccanti'}")
                
                ruolo_df = team_df[team_df['Ruolo'] == ruolo].copy()
                
                if len(ruolo_df) > 0:
                    # Crea colonne per la visualizzazione
                    cols = st.columns([3, 2, 1, 1, 1, 1])
                    cols[0].write("**Calciatore**")
                    cols[1].write("**Squadra**")
                    cols[2].write("**Costo**")
                    cols[3].write("**Ha ***")
                    cols[4].write("**Svincolare?**")
                    cols[5].write("**Importo Pagato**")
                    
                    for idx, row in ruolo_df.iterrows():
                        cols = st.columns([3, 2, 1, 1, 1, 1])
                        cols[0].write(row['Calciatore'])
                        cols[1].write(row['Squadra'])
                        cols[2].write(f"{row['Costo']}")
                        cols[3].write("✅" if row['Ha_Asterisco'] else "")
                        
                        # Checkbox per svincolare
                        svincolare = cols[4].checkbox(
                            "Sì",
                            value=row['Svincolare'],
                            key=f"svinc_{idx}",
                            label_visibility="collapsed"
                        )
                        st.session_state.team_data.loc[idx, 'Svincolare'] = svincolare
                        
                        # Input per importo pagato
                        importo = cols[5].number_input(
                            "Importo",
                            min_value=1,
                            value=int(row['Importo_Pagato']),
                            step=1,
                            key=f"imp_{idx}",
                            label_visibility="collapsed"
                        )
                        st.session_state.team_data.loc[idx, 'Importo_Pagato'] = importo
                    
                    st.markdown("---")
            
            # Riepilogo
            st.subheader("📈 Riepilogo")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Giocatori Totali", len(team_df))
                st.metric("Giocatori con *", team_df['Ha_Asterisco'].sum())
            
            with col2:
                st.metric("Da Svincolare", team_df['Svincolare'].sum())
                st.metric("Costo Totale", f"{team_df['Importo_Pagato'].sum()}")
            
            with col3:
                st.metric("Crediti Residui", crediti_residui_totali)
                # Calcola bonus totale correttamente
                bonus_totale = 0
                for _, row in team_df[team_df['Ha_Asterisco']].iterrows():
                    bonus_totale += ceil(row['Costo'] / 2)
                st.metric("Bonus Totale da *", bonus_totale)
        
        with tab2:
            st.header("🔄 Giocatori Svincolati")
            
            # Filtro per ruolo
            col1, col2 = st.columns([1, 3])
            with col1:
                ruolo_filter = st.selectbox(
                    "Filtra per ruolo:",
                    ["Tutti"] + ['P', 'D', 'C', 'A']
                )
            
            # Filtra i dati
            df_display = df_svincolati.copy()
            if ruolo_filter != "Tutti":
                df_display = df_display[df_display['Ruolo'] == ruolo_filter]
            
            # Ordina per FVM discendente
            df_display = df_display.sort_values('FVM', ascending=False)
            
            # Mostra statistiche
            st.markdown(f"**Totale giocatori svincolati:** {len(df_display)}")
            
            # Mostra la tabella
            st.dataframe(
                df_display,
                use_container_width=True,
                height=600,
                column_config={
                    "Nome": st.column_config.TextColumn("Nome", width="medium"),
                    "Sq.": st.column_config.TextColumn("Squadra", width="small"),
                    "Ruolo": st.column_config.TextColumn("Ruolo", width="small"),
                    "PGv": st.column_config.NumberColumn("PG", width="small"),
                    "MV": st.column_config.NumberColumn("MV", width="small", format="%.2f"),
                    "FM": st.column_config.NumberColumn("FM", width="small", format="%.2f"),
                    "FVM": st.column_config.NumberColumn("FVM", width="small", format="%.1f")
                }
            )
            
            # Top 10 per FVM
            st.subheader("🌟 Top 10 per FVM")
            top10 = df_svincolati.nlargest(10, 'FVM')[['Nome', 'Sq.', 'Ruolo', 'FVM']]
            st.dataframe(top10, use_container_width=True, hide_index=True)
    
    except FileNotFoundError:
        st.error("⚠️ File non trovato! Assicurati che il file Excel sia presente nel percorso corretto.")
    except Exception as e:
        st.error(f"⚠️ Errore durante il caricamento dei dati: {str(e)}")
        st.exception(e)

if __name__ == "__main__":
    main()
