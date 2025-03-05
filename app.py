import streamlit as st
import pandas as pd

# Tytuł aplikacji
st.title("Grupowanie laptopów")

# Wczytanie pliku Excela
uploaded_file = st.file_uploader("Wybierz plik Excel", type=["xlsx", "xls"])

if uploaded_file is not None:
    # Wczytanie danych z Excela do DataFrame
    df = pd.read_excel(uploaded_file)

    # Wyświetlenie surowych danych (opcjonalne)
    st.subheader("Surowe dane")
    st.dataframe(df)

    # Wybór kolumny do grupowania
    group_by_column = st.selectbox("Wybierz kolumnę do grupowania", df.columns)

    # Grupowanie danych
    grouped_data = df.groupby(group_by_column).size().reset_index(name='Liczba egzemplarzy')

    # Wyświetlenie pogrupowanych danych
    st.subheader(f"Pogrupowane dane według {group_by_column}")
    st.dataframe(grouped_data)

    # Opcjonalnie: możliwość filtrowania po innych kolumnach
    st.subheader("Filtrowanie danych")
    filter_column = st.selectbox("Wybierz kolumnę do filtrowania", df.columns)
    unique_values = df[filter_column].unique()
    selected_value = st.selectbox(f"Wybierz wartość w {filter_column}", unique_values)
    
    filtered_data = df[df[filter_column] == selected_value]
    st.dataframe(filtered_data)
else:
    st.write("Proszę załadować plik Excel, aby kontynuować.")
