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

    # Sprawdzanie, czy kolumna 'tags' istnieje w pliku
    if 'tags' in df.columns:
        # Grupowanie danych po 'tags' i zliczanie liczby wystąpień każdego tagu
        grouped_data = df.groupby('tags').size().reset_index(name='Liczba wystąpień')

        # Stworzenie rozwijanego panelu do wyświetlania wyników grupowania
        with st.expander("Kliknij, aby rozwinąć grupy po tagach"):
            # Wyświetlenie pogrupowanych danych
            st.write(grouped_data)

        # Wybór tagu do szczegółowego podglądu
        tag_selected = st.selectbox("Wybierz tag, aby zobaczyć szczegóły", grouped_data['tags'])

        # Filtrowanie danych dla wybranego tagu
        filtered_data = df[df['tags'] == tag_selected]

        # Wyświetlenie szczegółów dla wybranego tagu
        st.write(f"Lista urządzeń dla tagu: {tag_selected}", filtered_data)

    else:
        st.warning("Brak kolumny 'tags' w pliku.")
