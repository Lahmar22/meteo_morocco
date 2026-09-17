import streamlit as st


from analysis import app


st.set_page_config(
    page_title="Météo Maroc",
    page_icon="🌤️",
    layout="wide"
)


st.sidebar.title("Filtres")

st.sidebar.subheader("📍 Localisation")

city = st.sidebar.selectbox(
    "Choisir une ville",
    [
        "Casablanca",
        "Rabat",
        "Marrakech",
        "Fès",
        "Tanger",
        "Agadir",
        "Meknès",
        "Salé"
    ]
)

st.sidebar.subheader("📅 Période")

period = st.sidebar.selectbox(
    "Choisir une période",
    [
        "Aujourd'hui",
        "7 prochains jours"
    ]
)

st.sidebar.divider()

st.sidebar.info(
    "Utilisez les filtres pour explorer les données météo."
)


st.title("🌤️ Météo Maroc")

st.markdown(
    """
    ### Prévisions et analyse météorologique

    Cette application permet de consulter et d'analyser les données
    météorologiques des principales villes du Maroc.

    Vous pouvez sélectionner une ville et une période depuis la barre
    latérale afin d'explorer les températures, les précipitations et
    les conditions de vent.
    """
)

st.divider()

# Informations sélectionnées
st.subheader("📍 ")

st.metric("Nombre de villes", app.getCity())

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Ville",
        city
    )

with col2:
    st.metric(
        "Période",
        period
    )

