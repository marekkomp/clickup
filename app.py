import streamlit as st
import pandas as pd

# Umożliwienie wgrania pliku CSV
uploaded_file = st.file_uploader("Wgrać plik CSV", type=["csv"])

# Jeśli plik został wgrany, wykonaj poniższe kroki
if uploaded_file is not None:
    # Wczytaj plik CSV do DataFrame
    df = pd.read_csv(uploaded_file)
    
    # Wyświetl oryginalną tabelę danych
    st.write("Oryginalny DataFrame")
    st.dataframe(df)
    
    # Przycisk do grupowania po "tags"
    if st.button("Grupuj po tags"):
        # Znajdź kolumny numeryczne, pomijając "Task ID", bo jego suma nie ma sensu
        numerical_columns = df.select_dtypes(include=['number']).columns.tolist()
        if "Task ID" in numerical_columns:
            numerical_columns.remove("Task ID")
        
        # Grupuj dane po "tags" i oblicz liczbę zadań oraz sumy kolumn numerycznych
        grouped_df = df.groupby("tags").apply(lambda x: pd.Series({
            "liczba_zadań": x["Task ID"].count(),  # Liczba wierszy (zadań) dla każdego modelu
            **{col: x[col].sum() for col in numerical_columns}  # Sumy dla kolumn numerycznych
        })).reset_index()
        
        # Wyświetl zgrupowane dane
        st.write("Zgrupowany DataFrame")
        st.dataframe(grouped_df)
