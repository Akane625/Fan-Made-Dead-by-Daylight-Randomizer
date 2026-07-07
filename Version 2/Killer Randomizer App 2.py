import streamlit as st
import pandas as pd
import random

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(page_title="Dead by Daylight Randomizer", layout="centered")

# ==========================================
# LOAD DATA
# ==========================================

@st.cache_data
def load_data():
    df = pd.read_csv("Killer Perks Dataset Updated.csv")
    return df

df = load_data()
all_killers = sorted(df["killer"].dropna().unique())

# ==========================================
# SESSION STATE INIT
# ==========================================

if "killer_selected" not in st.session_state:
    st.session_state.killer_selected = {killer: True for killer in all_killers}

if "result_text" not in st.session_state:
    st.session_state.result_text = "Click Generate Build!"

# ==========================================
# FUNCTIONS
# ==========================================

def set_all(value):
    for killer in all_killers:
        st.session_state.killer_selected[killer] = value
        # also update the actual checkbox widget state
        st.session_state[f"chk_{killer}"] = value


def sync_from_checkboxes():
    for killer in all_killers:
        st.session_state.killer_selected[killer] = st.session_state[f"chk_{killer}"]


def generate_build():
    selected_killers = [k for k, v in st.session_state.killer_selected.items() if v]

    if not selected_killers:
        st.session_state.result_text = "Please select at least one killer."
        return

    killer = random.choice(selected_killers)

    perk_pool = df.loc[
        df["killer"].isna() | df["killer"].isin(selected_killers), "perk"
    ].dropna().tolist()

    if len(perk_pool) < 4:
        st.session_state.result_text = "Not enough perks available."
        return

    selected_perks = random.sample(perk_pool, 4)

    output = f"Killer: {killer}\n\n" + "\n".join(
        f"Perk {i}: {perk}" for i, perk in enumerate(selected_perks, 1)
    )
    st.session_state.result_text = output

# ==========================================
# LAYOUT
# ==========================================

st.markdown(
    "<h1 style='text-align:center;'>Dead by Daylight Randomizer</h1>",
    unsafe_allow_html=True,
)

selected_count = sum(st.session_state.killer_selected.values())
st.markdown(
    f"<p style='text-align:center;'>Selected Killers: {selected_count}/{len(all_killers)}</p>",
    unsafe_allow_html=True,
)

# ---- Killer filter (expander instead of popup window) ----
with st.expander("Edit Killer Filter", expanded=False):

    col_a, col_b = st.columns(2)
    with col_a:
        st.button("Select All", use_container_width=True, on_click=set_all, args=(True,))
    with col_b:
        st.button("Deselect All", use_container_width=True, on_click=set_all, args=(False,))

    st.divider()

    # 5-column checkbox grid, same as the tkinter grid layout
    columns = 5
    cols = st.columns(columns)
    for i, killer in enumerate(all_killers):
        with cols[i % columns]:
            st.checkbox(
                killer,
                value=st.session_state.killer_selected[killer],
                key=f"chk_{killer}",
                on_change=sync_from_checkboxes,
            )

st.divider()

# ---- Generate button ----
st.button("Generate Build", use_container_width=True, on_click=generate_build)

# ---- Result display ----
st.subheader("Generated Build")
st.code(st.session_state.result_text, language=None)
