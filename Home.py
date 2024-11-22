import pathlib

import requests

# Importing a custom font
import streamlit as st

css_path = pathlib.Path("assets/css/style.css")
with open(css_path, "r") as f:
    css_content = f.read()

html_path = pathlib.Path("index.html")
with open(html_path, "r") as f:
    html_content = f.read()

# TODO: Clean this up somehow
st.html(f"<style>{css_content}</style>")
st.html(html_content)


# Fetch a random dog fact from a public API
def fetch_dog_fact():
    try:
        response = requests.get("https://dog-api.kinduff.com/api/facts")
        if response.status_code == 200:
            data = response.json()
            return data["facts"][0]  # The fact is inside a list
        else:
            return "Couldn't fetch a dog fact at the moment. Please try again later!"
    except Exception as e:
        return f"Error: {str(e)}"


# add the new textbox for the dog fact
dog_fact = fetch_dog_fact()
st.markdown(
    f"""
    <div class="howtoadopt-info">
        <div class="howtoadopt-header">Did You Know?</div>
        <div class="howtoadopt-body">{dog_fact}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

footer_container = st.container()
with footer_container:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Contact Us")
        # Email with icon
        st.markdown(
            """
            <p style='font-size:16px;'>
            📧 <a href='mailto:MichaelSMills@jourrapide.com' style='text-decoration:none;'>MichaelSMills@jourrapide.com</a>
            </p>
            """,
            unsafe_allow_html=True
        )

        # Phone number with icon
        st.markdown(
            """
            <p style='font-size:16px;'>
            📞 +1 (201)-271-5719
            </p>
            """,
            unsafe_allow_html=True
        )

        # Address with icon
        st.markdown(
            """
            <p style='font-size:16px;'>
            🏠 3268 West Side Avenue, Union City, NJ 07087
            </p>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.header("Resources")
        st.markdown("<a>Report Animal Cruelty<a>", unsafe_allow_html=True)
        st.markdown("<a>Pet Loss & Grieving Services<a>", unsafe_allow_html=True)
        st.markdown("<a>Pet Safety<a>", unsafe_allow_html=True)

    with col3:
        st.header("Social Media")
        st.markdown(
            """
            <a href="https://www.instagram.com/Moted1971/" target="_blank" style="text-align: center;">
                <img src="https://cdn-icons-png.flaticon.com/512/4922/4922972.png" alt="Instagram" style="width:20px; height:20px; color: #5C6BC0; text-decoration: none;">
            </a>
            <span style="margin-left: 5px;">Moted1971</span>
            """,
            unsafe_allow_html=True
        )

st.sidebar.success("Select a page above.")
