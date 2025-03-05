import streamlit as st
import pandas as pd
from openpyxl import load_workbook

# Funkcja do wczytywania i przetwarzania danych z pliku Excel
def process_excel(file):
    try:
        # Wczytanie pliku za pomocą openpyxl
        wb = load_workbook(file)
        sheet = wb.active  # Wybór aktywnego arkusza

        # Wczytanie danych do pandas
        data = pd.read_excel(file, sheet_name=sheet.title)

        # Wydobycie nazw modeli laptopów, które znajdują się w co 5-tym wierszu (w przykładzie są to wiersze A4, A9, itd.)
        model_names = []
        for i in range(3, len(data), 6):  # Założenie, że model znajduje się co 6 wierszy (od A4)
            model_names.append(data.iloc[i, 0])

        # Przypisanie modelu do odpowiednich wierszy
        data['Model'] = None
        model_idx = 0
        for i in range(len(data)):
            if i % 6 == 3:  # Każdy 4. wiersz (A4, A9, itd.) to model
                data.loc[i, 'Model'] = model_names[model_idx]
                model_idx += 1
            else:
                data.loc[i, 'Model'] = data.loc[i-1, 'Model']  # Przypisanie poprzedniego modelu dla wierszy Task ID i egzemplarzy

        # Grupowanie danych według modeli
        grouped_data = data.groupby('Model').agg({'Task ID': 'count'}).reset_index()

        return data, grouped_data

    except Exception as e:
        st.error(f"Podczas przetwarzania pliku wystąpił błąd: {e}")
        return None, None

# Interfejs użytkownika w Streamlit
st.title("Grupowanie i ukrywanie egzemplarzy według modelu")

uploaded_file = st.file_uploader("Wybierz plik Excel", type=["xlsx"])

if uploaded_file is not None:
    # Przetwarzamy dane z pliku
    data, grouped_data = process_excel(uploaded_file)

    if data is not None and grouped_data is not None:
        # Wyświetlamy grupowane dane
        st.write("Liczba egzemplarzy według modeli:")
        st.write(grouped_data)

        # Interaktywne rozwijanie/grupowanie dla każdego modelu
        for model in grouped_data['Model']:
            with st.expander(f"{model}"):
                model_data = data[data['Model'] == model]
                st.write(model_data)
