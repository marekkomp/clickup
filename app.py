import pandas as pd
import streamlit as st

# Umożliwienie wgrania pliku CSV
uploaded_file = st.file_uploader("Wgrać plik CSV", type=["csv"])

# Opcje dla separatora
separator = st.selectbox("Wybierz separator", [',', ';', '\t', ' '])

if uploaded_file is not None:
    try:
        # Wczytaj plik CSV z wybranym separatorem
        df = pd.read_csv(uploaded_file, sep=separator, encoding='utf-8', on_bad_lines='skip')
        st.write("Plik został wczytany poprawnie!")
        st.dataframe(df)
        
        # Przycisk do grupowania po "tags"
        if st.button("Grupuj po tags"):
            # Znajdź kolumny numeryczne, pomijając "Task ID"
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
    except pd.errors.ParserError as e:
        st.error(f"Błąd parsowania pliku CSV: {e}")
        st.write("Sprawdź, czy separator jest poprawny i czy plik nie zawiera błędów strukturalnych.")
    except UnicodeDecodeError as e:
        st.error(f"Błąd kodowania: {e}")
        st.write("Spróbuj zmienić kodowanie pliku na UTF-8 lub określ inne kodowanie.")
    except Exception as e:
        st.error(f"Nieoczekiwany błąd: {e}")
