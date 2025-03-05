import streamlit as st
import pandas as pd

# Funkcja do wczytywania i przetwarzania danych z Excela
def process_excel(file):
    try:
        # Wczytanie pliku Excel
        df = pd.read_excel(file, sheet_name=None)
        
        # Wyświetlamy dostępne arkusze w pliku
        sheet_names = list(df.keys())
        st.write(f"Dostępne arkusze: {sheet_names}")
        
        # Wybieramy pierwszy arkusz (jeśli jest tylko jeden, lub możesz wybrać konkretny)
        sheet_name = sheet_names[0]  # Wybór pierwszego arkusza
        data = df[sheet_name]

        # Sprawdzamy nagłówki, zakładając, że zaczynają się od wiersza 2 (A2)
        data.columns = data.iloc[1]  # Ustawiamy drugi wiersz jako nagłówki
        data = data.drop([0, 1])  # Usuwamy wiersze 0 i 1 (zawierające dane i nagłówki)

        # Sprawdzamy pierwsze wiersze danych
        st.write("Pierwsze dane:", data.head())

        # Przykład grupowania według nazwy modelu i sumowania ilości
        grouped_data = data.groupby('Model').agg({'Cena': 'sum', 'Ilość': 'sum'}).reset_index()

        return grouped_data

    except Exception as e:
        st.error(f"Podczas przetwarzania pliku wystąpił błąd: {e}")
        return None

# Interfejs użytkownika w Streamlit
st.title("Grupowanie danych laptopów")

uploaded_file = st.file_uploader("Wybierz plik Excel", type=["xlsx"])

if uploaded_file is not None:
    # Przetwarzamy dane z pliku
    grouped_data = process_excel(uploaded_file)
    
    if grouped_data is not None:
        # Wyświetlamy grupowane dane
        st.write("Zgrupowane dane:", grouped_data)
