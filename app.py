import streamlit as st
import pandas as pd

# Funkcja do wczytywania i przetwarzania danych z Excela
def process_excel(file):
    # Wczytaj dane z pliku Excel
    df = pd.read_excel(file, sheet_name=None)
    
    # Zakładamy, że dane zaczynają się od A2, więc musimy odpowiednio ustawić nagłówki
    sheet_name = list(df.keys())[0]  # Zakłada, że dane są w pierwszym arkuszu
    data = df[sheet_name]
    
    # Wybieramy tylko dane od wiersza 2 (pomiń nagłówki)
    data.columns = data.iloc[1]  # Ustawiamy drugi wiersz jako nagłówki
    data = data.drop([0, 1])  # Usuwamy wiersze 0 i 1 (zawierające dane i nagłówki)
    
    # Przykład grupowania według nazwy modelu i sumowania ilości
    grouped_data = data.groupby('Model').agg({'Cena': 'sum', 'Ilość': 'sum'}).reset_index()

    return grouped_data

# Interfejs użytkownika w Streamlit
st.title("Grupowanie danych laptopów")

uploaded_file = st.file_uploader("Wybierz plik Excel", type=["xlsx"])

if uploaded_file is not None:
    # Przetwarzamy dane z pliku
    grouped_data = process_excel(uploaded_file)
    
    # Wyświetlamy grupowane dane
    st.write(grouped_data)

