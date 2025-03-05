import streamlit as st
import pandas as pd
from openpyxl import load_workbook

# Funkcja do wczytywania danych z pliku Excel
def process_excel(file):
    try:
        # Załaduj plik przy pomocy openpyxl
        wb = load_workbook(file)
        sheet = wb.active  # Wybierz aktywny arkusz

        # Wczytanie danych do pandas
        data = pd.read_excel(file, sheet_name=sheet.title)

        # Wyświetlamy pierwsze 5 wierszy danych, aby sprawdzić strukturę
        st.write("Pierwsze dane w pliku:")
        st.write(data.head())

        # Sprawdzamy kolumny, aby wiedzieć, jak pogrupować dane
        st.write("Kolumny w pliku:", data.columns)

        # Grupowanie danych według kolumny 'Task Name' (lub innej kolumny)
        grouped_data = data.groupby('Task Name').size().reset_index(name='Ilość laptopów')

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
        st.write("Zgrupowane dane:")
        st.write(grouped_data)
