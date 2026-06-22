import streamlit as st
import pandas as pd
import sqlite3, ossapi, os
import altair as alt
from dotenv import load_dotenv

load_dotenv()
api = ossapi.Ossapi(os.getenv("CLIENT_ID"), os.getenv("CLIENT_SECRET"))
usuario = os.getenv("USERNAME")

conexion = sqlite3.connect("osu_historial.db")
df = pd.read_sql_query("SELECT * FROM snapshots", conexion)
conexion.close()

st.set_page_config(page_title="Mi progreso osu!", page_icon="🎯", layout="wide")
yo = api.user(usuario)
col_avatar, col_info = st.columns([1, 4])
with col_avatar:
    st.image(yo.avatar_url, width=120)
with col_info:
    st.title("Mi progreso en osu!")
    st.write(f"{yo.username} · {yo.country_code}")

def grafica_metrica(df, campo, titulo, invertir=False):
    escala = alt.Scale(reverse=True) if invertir else alt.Scale()
    chart = alt.Chart(df).mark_line().encode(
        x=alt.X("momento:T", title="Fecha"),
        y=alt.Y(f"{campo}:Q", title=titulo, scale=escala),
        color=alt.Color("modo:N", title="Modo")
    )
    st.subheader(f"{titulo} por modo")
    st.altair_chart(chart, use_container_width=True)

df_osu = df[df["modo"] == "osu"].sort_values("momento")
actual = df_osu.iloc[-1]
previo = df_osu.iloc[-2]

df_mania = df[df["modo"] == "mania"].sort_values("momento")
actual_mania = df_mania.iloc[-1]
previo_mania = df_mania.iloc[-2]

c1, c2, c3 = st.columns(3)
c1.metric("PP (osu)", f"{actual['pp']:.0f}", delta=f"{actual['pp'] - previo['pp']:.0f}")
c2.metric("Ranking México", f"#{actual['country_rank']}",
          delta=int(actual['country_rank'] - previo['country_rank']), delta_color="inverse")
c3.metric("Ranking global", f"#{actual['global_rank']}",
          delta=int(actual['global_rank'] - previo['global_rank']), delta_color="inverse")

c4, c5, c6 = st.columns(3)
c4.metric("PP (mania)", f"{actual_mania['pp']:.0f}", delta=f"{actual_mania['pp'] - previo_mania['pp']:.0f}")
c5.metric("Ranking México", f"#{actual_mania['country_rank']}",
          delta=int(actual_mania['country_rank'] - previo_mania['country_rank']), delta_color="inverse")
c6.metric("Ranking global", f"#{actual_mania['global_rank']}",
          delta=int(actual_mania['global_rank'] - previo_mania['global_rank']), delta_color="inverse")

tab_pp, tab_rankings = st.tabs(["PP", "Rankings"])
with tab_pp:
    grafica_metrica(df, "pp", "Puntos de rendimiento (PP)")
with tab_rankings:
    grafica_metrica(df, "country_rank", "Ranking país", invertir=True)
    grafica_metrica(df, "global_rank", "Ranking global", invertir=True)