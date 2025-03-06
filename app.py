import pandas as pd
import streamlit as st

# Wgranie pliku CSV
uploaded_file = st.file_uploader("Wgrać plik CSV", type=["csv"])

# Wybór separatora
separator = st.selectbox("Wybierz separator", [',', ';', '\t', ' '])

if uploaded_file is not None:
    try:
        # Wczytanie pliku CSV z wybranym separatorem
        df = pd.read_csv(uploaded_file, sep=separator, encoding='utf-8', on_bad_lines='skip')
        st.write("Plik został wczytany poprawnie!")
        
        # Wyświetlanie oryginalnych danych z większą wysokością
        st.write("### Oryginalny DataFrame")
        st.dataframe(df, height=500)  # Tabela ma wysokość 500 pikseli
        
        # Sekcja filtrowania
        st.write("### Filtrowanie danych")
        
        # Filtr 1: Wybór modelu (kolumna "tags")
        unique_tags = df["tags"].unique().tolist()
        selected_tag = st.selectbox("Wybierz model", unique_tags)
        
        # Filtr 2: Wybór przeznaczenia (kolumna "Przeznaczenie") z opcją "Wszystkie"
        unique_destinations = ["Wszystkie"] + df["Przeznaczenie"].unique().tolist()
        selected_destination = st.selectbox("Wybierz przeznaczenie", unique_destinations)
        
        # Checkbox do pokazania/ukrycia egzemplarzy
        show_instances = st.checkbox(f"Pokaż egzemplarze dla modelu: {selected_tag}", value=True)
        
        if show_instances:
            # Filtrowanie po modelu
            filtered_df = df[df["tags"] == selected_tag]
            
            # Dodatkowe filtrowanie po przeznaczeniu, jeśli nie wybrano "Wszystkie"
            if selected_destination != "Wszystkie":
                filtered_df = filtered_df[filtered_df["Przeznaczenie"] == selected_destination]
            
            # Wyświetlanie przefiltrowanych danych z większą wysokością
            st.write(f"Egzemplarze dla modelu: {selected_tag}" + 
                     (f" i przeznaczenia: {selected_destination}" if selected_destination != "Wszystkie" else ""))
            st.dataframe(filtered_df, height=500)  # Tabela ma wysokość 500 pikseli
        else:
            st.write(f"Egzemplarze dla modelu: {selected_tag} są ukryte.")
    
    except pd.errors.ParserError as e:
        st.error(f"Błąd parsowania pliku CSV: {e}")
        st.write("Sprawdź, czy separator jest poprawny.")
    except UnicodeDecodeError as e:
        st.error(f"Błąd kodowania: {e}")
        st.write("Spróbuj zmienić kodowanie pliku na UTF-8.")
    except Exception as e:
        st.error(f"Nieoczekiwany błąd: {e}")
