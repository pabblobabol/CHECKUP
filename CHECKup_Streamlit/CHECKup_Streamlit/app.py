import streamlit as st
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="Digital Checkup SEO", page_icon="🔍")
st.title("🔍 Checkup SEO & Web – BIG Digital")

url = st.text_input("Inserisci l'URL della pagina da analizzare", "https://www.bigdigital.it")

if st.button("Avvia Analisi") and url:
    with st.spinner("Analisi in corso..."):
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            res = requests.get(url, headers=headers, timeout=10)
            html = res.text
            soup = BeautifulSoup(html, 'html.parser')

            # Estrazione base SEO
            title = soup.title.string.strip() if soup.title else "❌ Nessun title"
            meta = soup.find("meta", attrs={"name": "description"})
            desc = meta["content"].strip() if meta and "content" in meta.attrs else "❌ Nessuna description"
            h1 = soup.find("h1")
            h1_text = h1.text.strip() if h1 else "❌ Nessun H1"

            imgs = soup.find_all("img")
            imgs_total = len(imgs)
            imgs_no_alt = sum(1 for img in imgs if not img.has_attr("alt") or not img["alt"].strip())

            score = sum([
                1 if "❌" not in title else 0,
                1 if "❌" not in desc else 0,
                1 if "❌" not in h1_text else 0,
                1 if imgs_no_alt == 0 else 0
            ])

            # Risultati
            st.success("Analisi completata!")
            st.markdown(f"**Title:** {title}")
            st.markdown(f"**Meta Description:** {desc}")
            st.markdown(f"**H1:** {h1_text}")
            st.markdown(f"**Immagini totali:** {imgs_total}  |  **Senza ALT:** {imgs_no_alt}")
            st.markdown(f"**SEO Score:** {score} / 4")

        except Exception as e:
            st.error(f"Errore durante l'analisi: {e}")