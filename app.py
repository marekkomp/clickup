import pandas as pd
import streamlit as st

# Umożliwienie wgrania pliku CSV
uploaded_file = st.file_uploader("Wgrać plik CSV", type=["csv"])

# Opcje dla separatora
separator = st.selectbox("Wybierz separator", [',', ';', '\t', ' '])

if uploaded_file is not None:
    try:
        # Wczytaj plik CSV z wybranym separatorem
        df = pd.read_csv(uploaded_file, sep=separator, encoding='utf-8', on_bad_lines='skip')
        st.write("Plik został wczytany poprawnie!")
        
        # Wyświetlanie oryginalnych danych
        st.write("### Oryginalny DataFrame")
        st.dataframe(df)
        
        # Interaktywność: wybór modelu do ukrywania/odsłaniania egzemplarzy
        st.write("### Ukrywanie i odsłanianie egzemplarzy po modelu")
        
        # Lista unikalnych modeli (tags)
        unique_tags = df["tags"].unique().tolist()
        
        # Wybór modelu z listy rozwijanej
        selected_tag = st.selectbox("Wybierz model do zarządzania widocznością", unique_tags)
        
        # Checkbox do przełączania widoczności
        show_instances = st.checkbox(f"Pokaż egzemplarze dla modelu: {selected_tag}", value=True)
        
        # Filtruj dane na podstawie wybranego modelu i checkboxa
        if show_instances:
            filtered_df = df[df["tags"] == selected_tag]
            st.write(f"Egzemplarze dla modelu: {selected_tag}")
            st.dataframe(filtered_df)
        else:
            st.write(f"Egzemplarze dla modelu: {selected_tag} są ukryte.")
    
    except pd.errors.ParserError as e:
        st.error(f"Błąd parsowania pliku CSV: {e}")
        st.write("Sprawdź, czy separator jest poprawny i czy plik nie zawiera błędów strukturalnych.")
    except UnicodeDecodeError as e:
        st.error(f"Błąd kodowania: {e}")
        st.write("Spróbuj zmienić kodowanie pliku na UTF-8 lub określ inne kodowanie.")
    except Exception as e:
        st.error(f"Nieoczekiwany błąd: {e}")
