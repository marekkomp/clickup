import streamlit as st
import pandas as pd

# Wybór pliku (CSV lub Excel)
uploaded_file = st.file_uploader("Wybierz plik CSV lub Excel", type=["csv", "xlsx"])

if uploaded_file is not None:
    # Sprawdzenie, czy plik to CSV czy Excel
    if uploaded_file.name.endswith('.csv'):
        # Wczytanie pliku CSV
        df = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith('.xlsx'):
        # Wczytanie pliku Excel
        df = pd.read_excel(uploaded_file)

    # Wyświetlenie surowych danych
    st.write("Dane z pliku:", df)

    # Grupowanie po kolumnie "tags" i obliczanie sumy w pozostałych kolumnach
    if 'tags' in df.columns:
        grouped_data = df.groupby('tags').sum()
        # Wyświetlenie pogrupowanych danych
        st.write("Dane pogrupowane po modelach (tags):", grouped_data)
    else:
        st.warning("Brak kolumny 'tags' w pliku.")
