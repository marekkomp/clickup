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
        
        # Sprawdzenie, czy kolumna "Przeznaczenie" istnieje
        if "Przeznaczenie" not in df.columns:
            st.error("Kolumna 'Przeznaczenie' nie istnieje w pliku CSV. Sprawdź nazwy kolumn.")
        else:
            # Wyświetlanie oryginalnych danych z większą wysokością
            st.write("### Oryginalny DataFrame")
            st.dataframe(df, height=500)  # Tabela ma wysokość 500 pikseli
            
            # Sekcja filtrowania po "Przeznaczenie"
            st.write("### Filtrowanie po przeznaczeniu")
            
            # Pobranie unikalnych wartości z kolumny "Przeznaczenie"
            unique_destinations = df["Przeznaczenie"].unique().tolist()
            
            # Dodanie opcji "Wszystkie" na początku listy
            unique_destinations.insert(0, "Wszystkie")
            
            # Dropdown do wyboru przeznaczenia
            selected_destination = st.selectbox("Wybierz przeznaczenie", unique_destinations)
            
            # Filtrowanie danych
            if selected_destination == "Wszystkie":
                filtered_df = df  # Pokaż wszystkie dane
            else:
                filtered_df = df[df["Przeznaczenie"] == selected_destination]
            
            # Wyświetlanie przefiltrowanych danych z większą wysokością
            st.write(f"### Dane dla przeznaczenia: {selected_destination}")
            st.dataframe(filtered_df, height=500)  # Tabela ma wysokość 500 pikseli
    
    except pd.errors.ParserError as e:
        st.error(f"Błąd parsowania pliku CSV: {e}")
        st.write("Sprawdź, czy separator jest poprawny.")
    except UnicodeDecodeError as e:
        st.error(f"Błąd kodowania: {e}")
        st.write("Spróbuj zmienić kodowanie pliku na UTF-8.")
    except Exception as e:
        st.error(f"Nieoczekiwany błąd: {e}")
