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
            
            # Filtr dla "Procesor" (drop down)
            if "Procesor" in df.columns:
                unique_processors = df["Procesor"].unique().tolist()
                selected_processor = st.sidebar.selectbox("Wybierz procesor", ["Wszystkie"] + unique_processors)
            else:
                st.sidebar.warning("Kolumna 'Procesor' nie istnieje w pliku CSV.")
                selected_processor = "Wszystkie"
            
            # Filtr dla "Model Procesora" (short text)
            if "Model Procesora" in df.columns:
                model_processor = st.sidebar.text_input("Wprowadź model procesora", "")
            else:
                st.sidebar.warning("Kolumna 'Model Procesora' nie istnieje w pliku CSV.")
                model_processor = ""
            
            # Filtr dla "Rozdzielczość" (drop down)
            if "Rozdzielczość" in df.columns:
                unique_resolutions = df["Rozdzielczość"].unique().tolist()
                selected_resolution = st.sidebar.selectbox("Wybierz rozdzielczość", ["Wszystkie"] + unique_resolutions)
            else:
                st.sidebar.warning("Kolumna 'Rozdzielczość' nie istnieje w pliku CSV.")
                selected_resolution = "Wszystkie"
            
            # Filtrowanie danych
            filtered_df = df.copy()
            
            # Filtr dla "tags"
            if selected_tag != "Wszystkie":
                filtered_df = filtered_df[filtered_df["tags"] == selected_tag]
            
            # Filtr dla "Procesor"
            if selected_processor != "Wszystkie":
                filtered_df = filtered_df[filtered_df["Procesor"] == selected_processor]
            
            # Filtr dla "Model Procesora" (częściowe dopasowanie)
            if model_processor:
                filtered_df = filtered_df[filtered_df["Model Procesora"].str.contains(model_processor, case=False, na=False)]
            
            # Filtr dla "Rozdzielczość"
            if selected_resolution != "Wszystkie":
                filtered_df = filtered_df[filtered_df["Rozdzielczość"] == selected_resolution]
            
            # Wyświetlanie przefiltrowanych danych
            st.write("### Przefiltrowane dane")
            st.dataframe(filtered_df, height=500)  # Tabela o wysokości 500 pikseli
    
    except pd.errors.ParserError as e:
        st.error(f"Błąd parsowania pliku CSV: {e}")
    except UnicodeDecodeError as e:
        st.error(f"Błąd kodowania: {e}")
    except Exception as e:
        st.error(f"Nieoczekiwany błąd: {e}")
