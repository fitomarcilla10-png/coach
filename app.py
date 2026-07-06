"""
Buscador de Ejercicios
-----------------------
App de Streamlit que, a partir de un objetivo y una categoría muscular,
busca ejercicios/rutinas en:
  - La web en general
  - YouTube (API oficial si hay API key, si no, búsqueda alternativa)
  - Instagram (resultados públicos indexados + enlace de hashtag)
  - Facebook (resultados públicos indexados + enlace de búsqueda)

Nota importante sobre Instagram y Facebook:
Ambas plataformas NO ofrecen una API pública de búsqueda por palabra clave
para usuarios comunes (requieren cuentas Business verificadas y permisos
especiales, o directamente no lo permiten). Además, scrapear esas webs sin
iniciar sesión viola sus Términos de Servicio y suele estar bloqueado.
Por eso esta app busca contenido público ya indexado por buscadores
(usando "site:instagram.com" / "site:facebook.com") y además genera un
enlace directo para que el usuario busque manualmente dentro de cada red.
"""

import streamlit as st
from ddgs import DDGS
import requests

st.set_page_config(page_title="Buscador de Ejercicios", page_icon="💪", layout="wide")

CATEGORIAS = [
    "Piernas", "Brazos", "Espalda", "Pecho", "Abdomen", "Glúteos",
    "Cardio", "Movilidad y flexibilidad", "Cuerpo completo", "Hombros",
]

NIVELES = ["", "Principiante", "Intermedio", "Avanzado"]


def obtener_youtube_api_key(input_manual: str) -> str:
    """Prioriza la key ingresada a mano; si no hay, busca en st.secrets."""
    if input_manual:
        return input_manual
    try:
        return st.secrets.get("YOUTUBE_API_KEY", "")
    except Exception:
        return ""


def buscar_web(query: str, max_resultados: int = 5):
    resultados = []
    try:
        with DDGS() as ddgs:
            for r in ddgs.text(query, region="es-es", max_results=max_resultados):
                resultados.append(r)
    except Exception as e:
        st.warning(f"No se pudo completar la búsqueda: {e}")
    return resultados


def buscar_youtube_api(query: str, api_key: str, max_resultados: int = 5):
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "maxResults": max_resultados,
        "key": api_key,
        "relevanceLanguage": "es",
    }
    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        videos = []
        for item in data.get("items", []):
            video_id = item["id"]["videoId"]
            videos.append({
                "titulo": item["snippet"]["title"],
                "canal": item["snippet"]["channelTitle"],
                "url": f"https://www.youtube.com/watch?v={video_id}",
                "thumbnail": item["snippet"]["thumbnails"]["medium"]["url"],
            })
        return videos
    except Exception as e:
        st.warning(f"Error al buscar en YouTube (API): {e}")
        return []


def mostrar_lista_resultados(resultados):
    if not resultados:
        st.info("No se encontraron resultados.")
        return
    for r in resultados:
        titulo = r.get("title", "Sin título")
        link = r.get("href", "#")
        cuerpo = r.get("body", "")
        st.markdown(f"**[{titulo}]({link})**")
        if cuerpo:
            st.caption(cuerpo)
        st.divider()


def main():
    st.title("💪 Buscador de Ejercicios")
    st.caption(
        "Ingresá tu objetivo y la categoría muscular, y la app busca "
        "ejercicios y rutinas en distintas fuentes."
    )

    with st.sidebar:
        st.header("Parámetros de búsqueda")
        objetivo = st.text_input(
            "Objetivo",
            placeholder="Ej: perder grasa, ganar masa muscular, tonificar...",
        )
        categoria = st.selectbox("Categoría muscular", CATEGORIAS)
        nivel = st.selectbox("Nivel (opcional)", NIVELES)
        cantidad = st.slider("Resultados por fuente", min_value=3, max_value=10, value=5)

        st.divider()
        st.subheader("YouTube API (opcional)")
        st.caption(
            "Si cargás una API Key de YouTube Data API v3, vas a obtener "
            "resultados directos con miniaturas. Si no, se usa una búsqueda alternativa."
        )
        yt_key_input = st.text_input("YouTube API Key", type="password")

        buscar_btn = st.button("🔍 Buscar ejercicios", use_container_width=True)

    if not buscar_btn:
        st.info("Completá los parámetros en la barra lateral y presioná **Buscar ejercicios**.")
        return

    if not objetivo.strip():
        st.error("Por favor ingresá un objetivo.")
        return

    yt_api_key = obtener_youtube_api_key(yt_key_input)

    query_base = f"ejercicios de {categoria.lower()} para {objetivo.strip()}"
    if nivel:
        query_base += f" nivel {nivel.lower()}"

    st.subheader(f"Resultados para: _{query_base}_")

    tab_web, tab_yt, tab_ig, tab_fb = st.tabs(
        ["🌐 Web", "▶️ YouTube", "📷 Instagram", "📘 Facebook"]
    )

    with tab_web:
        with st.spinner("Buscando en la web..."):
            resultados = buscar_web(query_base, cantidad)
        mostrar_lista_resultados(resultados)

    with tab_yt:
        with st.spinner("Buscando en YouTube..."):
            if yt_api_key:
                videos = buscar_youtube_api(query_base, yt_api_key, cantidad)
                if videos:
                    cols = st.columns(2)
                    for i, v in enumerate(videos):
                        with cols[i % 2]:
                            st.image(v["thumbnail"])
                            st.markdown(f"**[{v['titulo']}]({v['url']})**")
                            st.caption(v["canal"])
                else:
                    st.info("No se encontraron videos.")
            else:
                st.info(
                    "No cargaste una YouTube API Key. Mostrando resultados "
                    "generales de YouTube encontrados en la web:"
                )
                resultados_yt = buscar_web(f"{query_base} site:youtube.com", cantidad)
                mostrar_lista_resultados(resultados_yt)

    with tab_ig:
        st.caption(
            "Instagram no permite búsquedas automatizadas sin iniciar sesión. "
            "Estos son resultados públicos indexados por buscadores:"
        )
        with st.spinner("Buscando en Instagram..."):
            resultados_ig = buscar_web(f"{query_base} site:instagram.com", cantidad)
        mostrar_lista_resultados(resultados_ig)
        hashtag = categoria.lower().replace(" ", "")
        st.markdown(
            f"🔗 [Ver publicaciones con #{hashtag} directamente en Instagram]"
            f"(https://www.instagram.com/explore/tags/{hashtag}/)"
        )

    with tab_fb:
        st.caption(
            "Facebook también restringe el acceso sin sesión. Estos son "
            "resultados públicos indexados por buscadores:"
        )
        with st.spinner("Buscando en Facebook..."):
            resultados_fb = buscar_web(f"{query_base} site:facebook.com", cantidad)
        mostrar_lista_resultados(resultados_fb)
        query_fb = query_base.replace(" ", "%20")
        st.markdown(
            f"🔗 [Buscar directamente en Facebook]"
            f"(https://www.facebook.com/search/top?q={query_fb})"
        )


if __name__ == "__main__":
    main()
