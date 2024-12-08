import streamlit as st

import requests
import json
import re  # For pattern matching
import math
import base64
import time  # For time delay


# Convert image to base64
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()


image_path = "assets/images/puppy place logo.jpg"
# image_path = "assets\images\puppy place logo.jpg"
base64_image = get_base64_image(image_path)

# Embed in HTML
st.markdown(
    f"""
    <div style="display: flex; flex-direction: column; align-items: center;">
        <img src='data:image/png;base64,{base64_image}' width='100'>
    </div>
    """,
    unsafe_allow_html=True,
)


# Read the CSS file content in Adopt.css file
with open("assets/css/Adopt.css", "r", encoding="utf-8") as file:
    css_content = file.read()

# Display CSS in the Streamlit app
st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)

# Define the API endpoint
url = "https://api.rescuegroups.org/v5/public/animals/search/available/dogs/"

# Set up the headers
headers = {
    "Authorization": "I9CW09wc",  # Replace with your actual API key
    "Content-Type": "application/json",  # Specify that you're sending JSON data
}


# Function to fetch data based on zip code and page number
def fetch_data(zip_code, miles=35):
    # Prepare the data you want to send, including the zip code
    data = {"data": {"filterRadius": {"miles": miles, "postalcode": zip_code}}}

    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()


# Validate the rescue ID
def is_valid_rescue_id(rescue_id) -> bool:
    return bool(rescue_id and re.match(r"^[a-zA-Z0-9-]+$", rescue_id.strip()))


# A text box that says "Find Dogs for Adoption Near You"
st.markdown(
    """
    <div style="
        background-color: rgba(255, 255, 255, 0.9);
        padding: 10px 20px; 
        border-radius: 10px; 
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); 
        text-align: center; 
        width: 50%; 
        margin: 0 auto;
        position: relative;">
        <img src="https://cdn-icons-png.flaticon.com/512/1998/1998627.png" 
            style="position: absolute; left: -150px; top: 50%; transform: translateY(-50%); width: 80px; height: 80px;" />
        <h1 style="font-size: 30px; color: black;">
            Find Dogs for Adoption Near You
        </h1>
        <div class="subtitle-text">Find dogs 10-50 miles from your zip code</div>
        <img src="https://cdn-icons-png.flaticon.com/512/1998/1998627.png" 
            style="position: absolute; right: -150px; top: 50%; transform: translateY(-50%); width: 80px; height: 80px;" />
    </div>
    """,
    unsafe_allow_html=True,
)

# Get user input for zip code
zip_code = st.text_input(" ### Enter your zip code (5 digits):", None)

# Validate the zip code (must be exactly 5 digits)
if zip_code and not re.match(r"^\d{5}$", str(zip_code)):
    st.error("Please enter a valid 5-digit zip code.")
else:
    if zip_code:
        # Let the user decide the number of results per page
        page_size = st.selectbox(
            "### How many results do you want to show per page?", options=[3, 6, 12, 20]
        )

        distance: int = st.slider(
            "### Distance",
            value=35,
            step=5,
            min_value=10,
            max_value=50,
        )  # TODO: How tf do I add this to the filter thing below instead of having this here?

        valid_dogs = []  # List to store valid dog results
        all_breeds = set()  # Set to store unique breeds

        # Display spinner after the zip code is entered and simulate a wait time
        # with st.spinner("Fetching data..."):
        # time.sleep(5)  # Simulate a wait time before data is fetched

        # Fetch the data
        page_number = 1  # Start with the first page
        while len(valid_dogs) < 20:
            data = fetch_data(zip_code, distance)  # Fetch data for the current page

            # Check if the API returned data
            if "data" in data and data["data"]:
                for animal in data["data"]:
                    attributes = animal["attributes"]
                    name = attributes.get("name", "Unknown")
                    age = attributes.get("ageString", "Unknown")
                    breed = attributes.get("breedPrimary", "Unknown")
                    gender = attributes.get("sex", "Not specified")  # Male or Female
                    coatLength = attributes.get("coatLength", "Unknown")
                    photo = attributes.get("pictureThumbnailUrl")  # Thumbnail URL
                    adoption_fee = attributes.get("adoptionFeeString", "Unknown")
                    rescue_id = attributes.get("rescueId", None)  # Rescue ID
                    info_url = attributes.get("url", "#")  # Dog's webpage URL

                    # Add breed to the set of all breeds
                    if breed != "Unknown":
                        all_breeds.add(breed)

                    # Fetch and normalize the size value
                    size = attributes.get("sizeCurrent", "Not specified")
                    if isinstance(
                        size, (int, float)
                    ):  # Ensure it's numeric before rounding
                        size = round(size, 1)
                    else:
                        size = (
                            "Not specified"  # Default for non-numeric or missing sizes
                        )

                    # Validate rescue ID
                    valid_rescue_id = (
                        rescue_id if is_valid_rescue_id(rescue_id) else None
                    )

                    # Check if the dog has a valid photo
                    if photo and photo.strip():
                        valid_dogs.append(
                            {
                                "name": name,
                                "age": age,
                                "breed": breed,
                                "gender": gender,
                                "coatLength": coatLength,
                                "photo": photo,
                                "adoption_fee": adoption_fee,
                                "rescue_id": valid_rescue_id,
                                "url": info_url,
                                "size": size,  # Add size to the data
                                "isDogsOk": attributes.get("isDogsOk", False),
                                "isCatsOk": attributes.get("isCatsOk", False),
                                "isHousetrained": attributes.get(
                                    "isHousetrained", False
                                ),
                                "energyLevel": attributes.get("energyLevel", "Unknown"),
                            }
                        )
            else:
                # Break if no data is returned for the current page
                break

            page_number += 1  # Move to the next page

        # Convert breeds to a sorted list for dropdown
        all_breeds = sorted(all_breeds)

        # Define the checkboxes outside the expander to ensure they're always available
        st.write("Other Filters:")
        good_with_dogs = st.checkbox("Good with other Dogs", key="good_with_dogs")
        good_with_cats = st.checkbox("Good with Cats", key="good_with_cats")
        house_trained = st.checkbox("House trained", key="house_trained")
        high_energy = st.checkbox("High energy level", key="high_energy")

        # Add the expander and filters inside it
        with st.expander("### Filters List"):
            st.markdown("### Apply Filters")

            # Other filter options inside the expander
            sex_filter: str = st.selectbox(
                "Sex:", ["Any", "Male", "Female"], key="sex_filter"
            )

            breed_filter: str = st.selectbox(
                "Breed:",
                ["All Breeds"] + all_breeds,  # Dynamically populated list of breeds
                key="breed_filter",
            )

            coat_length_filter: str = st.selectbox(
                "Coat Length:",
                ["Any", "Short", "Medium", "Long"],
                key="coat_length_filter",
            )

        # Now apply the filters to the dogs
        filtered_dogs = valid_dogs if valid_dogs else []

        # Apply the sex filter if not "Any"
        if sex_filter != "Any":
            filtered_dogs = [
                dog for dog in filtered_dogs if dog["gender"] == sex_filter
            ]



        # Filter the dogs by the selected breed if not "All Breeds"
        if breed_filter != "All Breeds":
            filtered_dogs = [
                dog for dog in filtered_dogs if dog["breed"] == breed_filter
            ]

        # Apply the coat length filter if not "Any"
        if coat_length_filter != "Any":
            filtered_dogs = [
                dog for dog in filtered_dogs if dog["coatLength"] == coat_length_filter
            ]

        # Now you can move the filter logic to where the actual filtering happens
        if good_with_dogs:
            filtered_dogs = [dog for dog in filtered_dogs if dog.get("isDogsOk")]
        if good_with_cats:
            filtered_dogs = [dog for dog in filtered_dogs if dog.get("isCatsOk")]
        if house_trained:
            filtered_dogs = [dog for dog in filtered_dogs if dog.get("isHousetrained")]
        if high_energy:
            filtered_dogs = [
                dog for dog in filtered_dogs if dog.get("energyLevel") == "High"
            ]

        if len(filtered_dogs) > 0:
            num_pages = math.ceil(len(filtered_dogs) / page_size)
            page = st.selectbox("### Page", range(1, num_pages + 1), key="pagination")

            start_idx = (page - 1) * page_size
            end_idx = start_idx + page_size
            current_page_dogs = filtered_dogs[start_idx:end_idx]
        else:
            st.write("No dogs available for the selected filters.")
            current_page_dogs = []

        # AAAAAAAAAAAAAAAAAAAAAAAAH
        # HOW THE FUUUCK DO I SET THE BACKGROUND FOR A CONTAINEEEEER
        # IM GOING INSAAAAAAANE
        # THIS SHOULD HAVE SOLVED IIIIIIT
        # GODDAMMMIIIIIIT
        # for experiment purposes, can delete JUST vvv THIS
        with st.container(border=True, key="dawg-container"):
            # Apparently, adding a key  ^^^^^^         here, adds
            # a css class of the same name prefixed with 'st-key-',
            # Havent gotten it to work however
            cols = st.columns(3)  # Create three columns
            for i, dog in enumerate(current_page_dogs):
                with cols[i % 3]:  # Use modulo to cycle through columns
                    st.subheader(
                        f'[Name: {dog["name"]}]({dog["url"]})'
                    )  # Name with link
                    if dog["photo"]:
                        st.image(
                            dog["photo"],
                            caption=dog["name"],
                            use_container_width=True,
                        )  # Display image
                    st.write(
                        f'**Age:** {dog["age"] if dog["age"] != "Unknown" else "Not specified"}'
                    )
                    st.write(
                        f'**Breed:** {dog["breed"] if dog["breed"] != "Unknown" else "Not specified"}'
                    )
                    st.write(f'**Gender:** {dog["gender"]}')
                    st.write(f'**Adoption Fee:** {dog["adoption_fee"]}')
                    st.write(
                        f'**Size:** {dog["size"] if dog["size"] != "Not specified" else "Size not available"} lbs'
                        if dog["size"] != "Not specified"
                        else ""
                    )  # Display size
                    if dog[
                        "rescue_id"
                    ]:  # Only display rescue ID if it passes validation
                        st.write(f'**Rescue ID:** {dog["rescue_id"]}')
                    st.write(
                        f'**URL:** [View More Info]({dog["url"]})'
                    )  # Clickable URL for dog

                # if not current_page_dogs: # If page lacks dogs, it wont show
                # st.write("No dogs available for this page.")
