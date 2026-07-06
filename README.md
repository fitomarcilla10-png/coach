# 🏀 Buscador de Técnicas de Básquet

App en Streamlit que busca ejercicios, tutoriales y jugadas según:
- **Tipo de técnica**: Individual (dribbling, tiro, defensa 1v1, footwork, etc.)
  o de Equipo (pick and roll, defensa en zona, contraataque, sistemas, etc.)
- **Técnica puntual** elegida de una lista específica de básquet
- **Objetivo** opcional (ej. "mejorar el porcentaje de triples", "romper una zona 2-3")

Busca en:

- 🌐 La web en general
- ▶️ YouTube
- 📷 Instagram
- 📘 Facebook

## ⚠️ Importante sobre Instagram y Facebook

Instagram y Facebook **no ofrecen una API pública de búsqueda por palabra clave** para
usuarios comunes, y scrapear esas webs sin iniciar sesión viola sus Términos de Servicio
(además de que técnicamente lo bloquean). Por eso esta app:

1. Busca contenido público ya **indexado por buscadores** (usando `site:instagram.com` /
   `site:facebook.com`), lo cual es legítimo y no requiere login.
2. Genera un **enlace directo** para que completes la búsqueda manualmente dentro de
   cada red social.

YouTube sí tiene una API oficial y gratuita (con límite diario), que la app usa si le
cargás una API Key. Si no cargás ninguna, usa el mismo método de búsqueda indexada.

## 🚀 Cómo subirlo a GitHub

```bash
cd buscador-ejercicios
git init
git add .
git commit -m "Primera versión del buscador de ejercicios"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/TU_REPO.git
git push -u origin main
```

## ☁️ Cómo desplegarlo en Streamlit Community Cloud

1. Entrá a [share.streamlit.io](https://share.streamlit.io) e iniciá sesión con GitHub.
2. Click en **"New app"**.
3. Elegí tu repositorio, la rama `main` y el archivo `app.py`.
4. (Opcional) Si vas a usar la YouTube API, andá a **Settings → Secrets** de la app
   desplegada y pegá:

   ```toml
   YOUTUBE_API_KEY = "tu_api_key_real"
   ```

5. Click en **Deploy**. En un par de minutos tu app estará online.

## 🔑 Cómo obtener una YouTube API Key (opcional pero recomendado)

1. Entrá a [Google Cloud Console](https://console.cloud.google.com/).
2. Creá un proyecto nuevo (o usá uno existente).
3. Activá la **YouTube Data API v3** desde la biblioteca de APIs.
4. Generá una **credencial de tipo API Key**.
5. Pegala en la barra lateral de la app, o cargala como secret (ver punto anterior).

La API tiene una cuota gratuita diaria (10.000 unidades/día), suficiente para uso normal.

## 🖥️ Cómo correrlo en local

```bash
pip install -r requirements.txt
streamlit run app.py
```

## 📁 Estructura del proyecto

```
buscador-ejercicios/
├── app.py                          # App principal de Streamlit
├── requirements.txt                # Dependencias
├── .gitignore
├── .streamlit/
│   └── secrets.toml.example        # Plantilla de secrets (no subir el real)
└── README.md
```
