import streamlit as st
import pandas as pd

# Wczytanie pliku CSV
uploaded_file = st.file_uploader("Wybierz plik CSV", type=["csv"])

if uploaded_file is not None:
    # Wczytanie danych do DataFrame
    df = pd.read_csv(uploaded_file)

    # Wyświetlenie surowych danych
    st.write("Dane z pliku CSV:", df)

    # Grupowanie po kolumnie "tags" i obliczanie sumy w pozostałych kolumnach (np. jeśli są numeryczne)
    if 'tags' in df.columns:
        grouped_data = df.groupby('tags').sum()

        # Wyświetlenie pogrupowanych danych
        st.write("Dane pogrupowane po modelach (tags):", grouped_data)

    else:
        st.warning("Brak kolumny 'tags' w pliku CSV.")
