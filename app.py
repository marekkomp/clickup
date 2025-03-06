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
            
            # Filtr dla "Procesor (drop down)"
            unique_processors = df["Procesor (drop down)"].unique().tolist()
            selected_processor = st.sidebar.selectbox("Wybierz procesor", ["Wszystkie"] + unique_processors)
            
            # Filtr dla "Model Procesora (short text)"
            processor_model = st.sidebar.text_input("Model Procesora (short text)", "")
            
            # Filtr dla "Rozdzielczość (drop down)"
            unique_resolutions = df["Rozdzielczość (drop down)"].unique().tolist()
            selected_resolution = st.sidebar.selectbox("Wybierz rozdzielczość", ["Wszystkie"] + unique_resolutions)
            
            # Filtrowanie danych
            filtered_df = df.copy()
            
            # Filtrowanie po "tags"
            if selected_tag != "Wszystkie":
                filtered_df = filtered_df[filtered_df["tags"] == selected_tag]
                
            # Filtrowanie po "Procesor (drop down)"
            if selected_processor != "Wszystkie":
                filtered_df = filtered_df[filtered_df["Procesor (drop down)"] == selected_processor]
                
            # Filtrowanie po "Model Procesora (short text)" (częściowe dopasowanie)
            if processor_model:
                filtered_df = filtered_df[filtered_df["Model Procesora (short text)"].str.contains(processor_model, case=False, na=False)]
                
            # Filtrowanie po "Rozdzielczość (drop down)"
            if selected_resolution != "Wszystkie":
                filtered_df = filtered_df[filtered_df["Rozdzielczość (drop down)"] == selected_resolution]
            
            # Wyświetlanie przefiltrowanych danych
            st.write("### Przefiltrowane dane")
            st.dataframe(filtered_df, height=500)  # Tabela o wysokości 500 pikseli
    
    except pd.errors.ParserError as e:
        st.error(f"Błąd parsowania pliku CSV: {e}")
    except UnicodeDecodeError as e:
        st.error(f"Błąd kodowania: {e}")
    except KeyError as e:
        st.error(f"Brak wymaganej kolumny w pliku CSV: {e}")
    except Exception as e:
        st.error(f"Nieoczekiwany błąd: {e}")
