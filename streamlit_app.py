import streamlit as st

st.set_page_config(layout="wide")

# --- PAGE SETUP ---
home_page = st.Page(
    "pages/home.py",
    title="Home Page",
    icon=":material/menu_book:",
    default=True,
)
#description, account_circle, article, assignment, summarize, book
parties_sel_page = st.Page(
    "pages/parties_selection.py",
    title="Parties Selection",
    icon=":material/account_balance:",
)
eda_page = st.Page(
    "pages/eda.py",
    title="Data Exploration",
    icon=":material/bar_chart:",
)
#monitoring, trending_up, query_stats, analytics
#:material/database:, table_rows, :material/timer:, hourglass_top, tune, :material/business_center:, work, card_travel
pred_mod_page = st.Page(
    "pages/prediction_models.py",
    title="Prediction Models",
    icon=":material/pattern:",
) #shape_line, activity_zone, circles_ext, hub, network_intelligence,blur_on


# --- NAVIGATION SETUP [WITHOUT SECTIONS] ---
# pg = st.navigation(pages=[home_page, parties_sel_page, eda_page, pred_mod_page])

# --- NAVIGATION SETUP [WITH SECTIONS]---
pg = st.navigation(
    {
        "Introduction": [home_page],
        "Projects": [parties_sel_page, eda_page, pred_mod_page],
    }
)


# --- SHARED ON ALL PAGES ---
#st.logo("assets/codingisfun_logo.png")
st.sidebar.markdown("Made by [Adrià Julià Parada](https://github.com/AdriaJP02)")


# --- RUN NAVIGATION ---
pg.run()