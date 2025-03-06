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

    # Sprawdzanie, czy kolumna 'tags' istnieje w pliku
    if 'tags' in df.columns:
        # Dodanie opcji 'Wszystkie modele' w filtrze 'tags'
        tag_selected = st.selectbox("Wybierz model, aby zobaczyć szczegóły", ['Wszystkie modele'] + list(df['tags'].unique()))

        # Jeżeli wybrano 'Wszystkie modele', zliczamy wszystkie tagi razem
        if tag_selected == 'Wszystkie modele':
            filtered_data = df
            grouped_data = filtered_data.groupby('tags').size().reset_index(name='Liczba wystąpień')
            st.write(f"Grupa: Wszystkie modele (razem {grouped_data['Liczba wystąpień'].sum()} sztuk)", grouped_data)
        else:
            # Filtrowanie danych po wybranym modelu
            filtered_data = df[df['tags'] == tag_selected]
        
        # Opcjonalne filtry: Lists i Przeznaczenie
        # Filtracja po "Lists" z nazwą "Wybierz dostawę"
        if 'Lists' in df.columns:
            list_selected = st.selectbox("Wybierz dostawę (opcjonalnie)", ['Wszystkie'] + list(filtered_data['Lists'].unique()))
            if list_selected != 'Wszystkie':
                filtered_data = filtered_data[filtered_data['Lists'] == list_selected]

        # Filtracja po "Przeznaczenie" z nazwą "Przeznaczenie"
        if 'Przeznaczenie' in df.columns:
            przeznaczenie_selected = st.selectbox("Przeznaczenie", ['Wszystkie'] + list(filtered_data['Przeznaczenie'].unique()))
            if przeznaczenie_selected != 'Wszystkie':
                filtered_data = filtered_data[filtered_data['Przeznaczenie'] == przeznaczenie_selected]

        # Wyświetlenie przefiltrowanych danych
        st.write("Dane po zastosowaniu filtrów:", filtered_data)

    else:
        st.warning("Brak kolumny 'tags' w pliku.")
