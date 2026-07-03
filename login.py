import streamlit as st
import pandas as pd


def login():

    st.markdown("""
    <h1 style='text-align:center;color:#1565C0;'>
    🔐 Login
    </h1>
    """, unsafe_allow_html=True)

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    login_btn = st.button("Login")

    if login_btn:

        users = pd.read_csv("users.csv")

        user = users[
            (users["username"] == username) &
            (users["password"] == password)
        ]

        if len(user) > 0:

            st.session_state["login"] = True

            st.success("Login Successful")

            st.rerun()

        else:

            st.error("Invalid Username or Password")