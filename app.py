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
        
        # Sprawdzenie, czy kolumna "Przeznaczenie (drop down)" istnieje
        if "Przeznaczenie (drop down)" not in df.columns:
            st.error("Kolumna 'Przeznaczenie (drop down)' nie istnieje w pliku CSV. Sprawdź nazwy kolumn.")
        else:
            # Wyświetlanie oryginalnych danych
            st.write("### Oryginalny DataFrame")
            st.dataframe(df, height=500)  # Wysokość tabeli: 500 pikseli
            
            # Sekcja filtrowania
            st.write("### Filtrowanie po przeznaczeniu")
            
            # Pobranie unikalnych wartości z kolumny "Przeznaczenie (drop down)"
            unique_destinations = df["Przeznaczenie (drop down)"].unique().tolist()
            unique_destinations.insert(0, "Wszystkie")  # Dodanie opcji "Wszystkie"
            
            # Dropdown do wyboru przeznaczenia
            selected_destination = st.selectbox("Wybierz przeznaczenie", unique_destinations)
            
            # Filtrowanie danych
            if selected_destination == "Wszystkie":
                filtered_df = df  # Pokazuje wszystkie dane
            else:
                filtered_df = df[df["Przeznaczenie (drop down)"] == selected_destination]
            
            # Wyświetlanie przefiltrowanych danych
            st.write(f"### Dane dla przeznaczenia: {selected_destination}")
            st.dataframe(filtered_df, height=500)  # Wysokość tabeli: 500 pikseli
    
    except pd.errors.ParserError:
        st.error("Błąd parsowania pliku CSV. Sprawdź, czy separator jest poprawny.")
    except UnicodeDecodeError:
        st.error("Błąd kodowania. Spróbuj zmienić kodowanie pliku na UTF-8.")
    except Exception as e:
        st.error(f"Nieoczekiwany błąd: {e}")
