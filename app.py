import pandas as pd
import streamlit as st

# Wgranie pliku CSV
uploaded_file = st.file_uploader("Wgrać plik CSV", type=["csv"])

# Wybór separatora
separator = st.selectbox("Wybierz separator", [',', ';', '\t', ' '])

if uploaded_file is not None:
    try:
        # Wczytanie pliku CSV z wybranym separatorem
        df = pd.read_csv(uploaded_file, sep=separator, encoding='utf-8', on_bad_lines='skip')
        st.write("Plik został wczytany poprawnie!")
        
        # Sprawdzenie, czy kolumna "tags" istnieje
        if "tags" not in df.columns:
            st.error("Brak kolumny 'tags' w pliku CSV. Sprawdź plik.")
        else:
            # Filtry po lewej stronie
            st.sidebar.header("Filtry")
            
            # Filtr dla "tags"
            unique_tags = df["tags"].unique().tolist()
            selected_tag = st.sidebar.selectbox("Wybierz tag", ["Wszystkie"] + unique_tags)
            
            # Filtrowanie danych
            filtered_df = df.copy()
            if selected_tag != "Wszystkie":
                filtered_df = filtered_df[filtered_df["tags"] == selected_tag]
            
            # Wyświetlanie przefiltrowanych danych
            st.write("### Przefiltrowane dane")
            st.dataframe(filtered_df, height=500)  # Tabela o wysokości 500 pikseli
    
    except pd.errors.ParserError as e:
        st.error(f"Błąd parsowania pliku CSV: {e}")
    except UnicodeDecodeError as e:
        st.error(f"Błąd kodowania: {e}")
    except Exception as e:
        st.error(f"Nieoczekiwany błąd: {e}")
