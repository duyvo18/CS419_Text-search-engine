import streamlit as st

import search_engine

CARDS_PER_ROW = 1

def main():
    st.title("Search Engine")

    query = st.text_input("Query:")

    if query:
        results = search_engine.search(query)
        
        st.write(f"Found {len(results)} results.")
        for idx, result in enumerate(results):
            title = result[0].upper()
            content = result[1]
            
            i = idx % CARDS_PER_ROW
            if i==0:
                st.write("---")
                cols = st.columns(CARDS_PER_ROW, gap="large")
            with cols[idx % CARDS_PER_ROW]:
                st.caption(f'# {title}')
                st.markdown(content)

if __name__ == '__main__':
    main()