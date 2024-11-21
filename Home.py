import streamlit as st

# Using st.markdown with CSS to hide the default header and footer of the website
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# Custom CSS to change sidebar collapse button color
custom_sidebar_button_css = """
<style>
.st-emotion-cache-1rg1gxd {
  font-weight: 400;
  color: orange;
  cursor: pointer;
  font-size: 16px;
  line-height: 1;
}
<style>
"""
st.markdown(custom_sidebar_button_css, unsafe_allow_html=True)
# Add CSS for background, button area, and image slider styling
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://wallpaperaccess.com/full/3019614.jpg");
    background-size: cover;  
    background-position: center;  
    background-attachment: local; 
}

.slider-frame {
    overflow: hidden;
    height: 800px;
    width: 1200px;
    position: relative;
    left: 50%;
    transform: translateX(-50%);
    margin-top: 160px; /* Adjusted to move the slider up into the previous textbox space */
}

@keyframes slide_animation {
    0% {left:0px;}
    10% {left:0px;}
    20% {left:1200px;}
    30% {left:1200px;}
    40% {left: 2400px;}
    50% {left: 2400px;}
    60% {left: 1200px;}
    70% {left:1200px;}
    80% {left: 0px;}
    90% {left: 0px;}
    100% {left:0px;}
}

.slide-images {
    width: 3600px;
    height: 800px;
    margin: 0 0 0 -2400px;
    position: relative;
    animation-name: slide_animation;
    animation-duration: 33s;
    animation-iteration-count: infinite;
    animation-direction: alternate;
    animation-play-state: running;
}

.img-container {
    height: 800px;
    width: 1200px;
    position: relative;
    float: left;
}

.textbox {
    position: absolute;
    top: 100px; /* Adjust the distance from the top */
    left: 50%;
    transform: translateX(-50%);
    font-size: 40px;
    font-weight: bold;
    color: white;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5); /* Adds shadow for better visibility */
    z-index: 999; /* Ensure it's above other content */
}

/* New styles for the 'Why Choose Adoption?' section */
.adoption-info {
    background-color: rgba(255, 255, 255, 0.8); /* Semi-transparent white background */
    border-radius: 8px; /* Rounded corners */
    padding: 20px; /* Padding inside the box */
    margin: 20px auto; /* Center the box with margin */
    max-width: 800px; /* Restrict the width */
    text-align: center; /* Center align text */
}

.adoption-header {
    font-size: 24px; /* Header font size */
    font-weight: bold; /* Bold header */
    color: #333; /* Dark text color */
    margin-bottom: 10px; /* Space below the header */
}

.adoption-body {
    font-size: 16px; /* Body text size */
    color: #555; /* Medium gray text color */
    line-height: 1.5; /* Improve readability */
}

.howtoadopt-info {
    background-color: rgba(255, 255, 255, 0.8); /* Semi-transparent white background */
    border-radius: 8px; /* Rounded corners */
    padding: 20px; /* Padding inside the box */
    margin: 20px auto; /* Center the box with margin */
    max-width: 800px; /* Restrict the width */
    text-align: center; /* Center align text */
}

.howtoadopt-header {
    font-size: 24px; /* Header font size */
    font-weight: bold; /* Bold header */
    color: #333; /* Dark text color */
    margin-bottom: 10px; /* Space below the header */
}

.howtoadopt-body {
    font-size: 16px; /* Body text size */
    color: #555; /* Medium gray text color */
    line-height: 1.5; /* Improve readability */
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# Add a textbox with "Adopt a Pet" text
st.markdown(
    """
    <div class="textbox">
        Adopt a Pet
    </div>
    """,
    unsafe_allow_html=True
)

# Add the image slider
st.markdown(
    """
    <div class="slider-frame">
        <div class="slide-images">
            <div class="img-container">
                <img src="https://images.pexels.com/photos/2887566/pexels-photo-2887566.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2" width="1200" height="800">
            </div>
            <div class="img-container">
                <img src="https://images.pexels.com/photos/7289/animal-dog-pet-sad.jpg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2" width="1200" height="800">
            </div>
            <div class="img-container">
                <img src="https://images.pexels.com/photos/29359650/pexels-photo-29359650/free-photo-of-black-dog-lying-under-rusty-metal-outdoors.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2" width="1200" height="800">
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# Below, are the textboxes for various info
# In the HTML for the text use the code: <div class="textboxName-body">text</div> ... to add text in a textbox.
# Add the new textbox for "Why Choose Adoption?"
st.markdown(
    """
    <div class="adoption-info">
        <div class="adoption-header">Why Choose Adoption?</div>
        <div class="adoption-body">When people choose to adopt animals in need of homes, they not only save the lives of those animals but also improve their own lives in countless meaningful ways. When you adopt a dog you get a pet and you give a homeless animal a second chance.</div>
        <div class="adoption-body">Adopted dogs are often spayed or neutered and vaccinated and microchipped before they find their new homes.</div>
        <div class="adoption-body">Adopting a dog brings joy, and it creates a rewarding experience. As you provide love and companionship, a deserving animal will benefit from your kindness.</div>
    </div>
    """,
    unsafe_allow_html=True
)

# Add the new textbox for "How to Adopt?"
st.markdown(
    """
    <div class="howtoadopt-info">
        <div class="howtoadopt-header">How Do I Adopt?</div>
        <div class="howtoadopt-body">Explore the dogs that are available for adoption!</div>
        <div class="howtoadopt-body">When you're ready, submit your adoption application!</div>
        <div class="howtoadopt-body">Meet your new furry family member and bring joy to your home!</div>
        <div class="howtoadopt-body">Finally, complete the adoption and make it official!</div>
    """,
    unsafe_allow_html=True
)

st.sidebar.success("Select a page above.")