import streamlit as st
import requests
import json
import re  # For pattern matching
import math
import time  # For time delay

# Read the CSS file content in Adopt.css file
with open("assets/css/Adopt.css", "r", encoding="utf-8") as file:
    css_content = file.read()

# Display CSS in the Streamlit app
st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)

# Define the API endpoint
url = 'https://api.rescuegroups.org/v5/public/animals/search/available/dogs/'

# Set up the headers
headers = {
    'Authorization': 'I9CW09wc',  # Replace with your actual API key
    'Content-Type': 'application/json'  # Specify that you're sending JSON data
}

# Function to fetch data based on zip code and page number
def fetch_data(zip_code, page, limit=10):
    # Prepare the data you want to send, including the zip code
    data = {
        "limit": limit,  # Number of results to return
        "page": page,  # Page number
        "fields": {
            "animals": [
                "name", "ageString", "breedString", "sex",
                "adoptionFeeString", "pictureThumbnailUrl", "rescueId", "url", "sizeCurrent"
            ]  # Fields to return
        },
        "filters": {
            "location": {
                "zip": zip_code
            }
        }
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()

# Validate the rescue ID
def is_valid_rescue_id(rescue_id):
    return bool(rescue_id and re.match(r'^[a-zA-Z0-9-]+$', rescue_id.strip()))

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
        <img src="https://cdn-icons-png.flaticon.com/512/1998/1998627.png" 
            style="position: absolute; right: -150px; top: 50%; transform: translateY(-50%); width: 80px; height: 80px;" />
    </div>
    """,
    unsafe_allow_html=True
)

# Get user input for zip code
zip_code = st.text_input("Enter your zip code (5 digits):", "")

# Validate the zip code (must be exactly 5 digits)
if zip_code and not re.match(r'^\d{5}$', zip_code):
    st.error("Please enter a valid 5-digit zip code.")
else:
    if zip_code:
        page_size = 6
        valid_dogs = []  # List to store valid dog results

        # Display spinner after the zip code is entered and sleep for 5 seconds
        with st.spinner('Fetching data...'):
            time.sleep(5)  # Simulate a 5-second wait before data is fetched
        # Fetch the data after the spinner disappears
        page_number = 1  # Start with the first page
        max_pages = 5  # Set a limit to avoid excessive API calls
        while len(valid_dogs) < 20 and page_number <= max_pages:
            data = fetch_data(zip_code, page_number, limit=100)  # Fetch data for the current page

            # Check if the API returned data
            if 'data' in data and data['data']:
                for animal in data['data']:
                    attributes = animal['attributes']
                    name = attributes.get('name', 'Unknown')
                    age = attributes.get('ageString', 'Unknown')
                    breed = attributes.get('breedString', 'Unknown')
                    gender = attributes.get('sex', 'Not specified')  # Male or Female
                    photo = attributes.get('pictureThumbnailUrl')  # Thumbnail URL
                    adoption_fee = attributes.get('adoptionFeeString', 'Unknown')
                    rescue_id = attributes.get('rescueId', None)  # Rescue ID
                    info_url = attributes.get('url', '#')  # Dog's webpage URL
                    size = attributes.get('sizeCurrent', 'Not specified')  # Dog's current size

                    # Validate rescue ID
                    valid_rescue_id = rescue_id if is_valid_rescue_id(rescue_id) else None

                    # Check if the dog has a valid photo
                    if photo and photo.strip():
                        valid_dogs.append({
                            'name': name,
                            'age': age,
                            'breed': breed,
                            'gender': gender,
                            'photo': photo,
                            'adoption_fee': adoption_fee,
                            'rescue_id': valid_rescue_id,
                            'url': info_url,
                            'size': size  # Add size to the data
                        })
            else:
                # Break if no data is returned for the current page
                break

            page_number += 1  # Move to the next page

        # Pagination control
        num_pages = math.ceil(len(valid_dogs) / page_size)
        page = st.selectbox("Page", range(1, num_pages + 1))

        # Display the current page's dogs
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        current_page_dogs = valid_dogs[start_idx:end_idx]

        # Display the results
        cols = st.columns(3)  # Create three columns
        for i, dog in enumerate(current_page_dogs):
            with cols[i % 3]:  # Use modulo to cycle through columns
                st.subheader(f'[Name: {dog["name"]}]({dog["url"]})')  # Name with link
                if dog['photo']:
                    st.image(dog['photo'], caption=dog['name'], use_container_width=True)  # Display image
                st.write(f'**Age:** {dog["age"] if dog["age"] != "Unknown" else "Not specified"}')
                st.write(f'**Breed:** {dog["breed"] if dog["breed"] != "Unknown" else "Not specified"}')
                st.write(f'**Gender:** {dog["gender"]}')
                st.write(f'**Adoption Fee:** {dog["adoption_fee"]}')
                st.write(
                    f'**Size:** {dog["size"] if dog["size"] != "Not specified" else "Size not available"} lbs' if
                    dog["size"] != "Not specified" else "") # Display size
                if dog['rescue_id']:  # Only display rescue ID if it passes validation
                    st.write(f'**Rescue ID:** {dog["rescue_id"]}')
                st.write(f'**URL:** [View More Info]({dog["url"]})')  # Clickable URL for dog

        if not current_page_dogs:
            st.write("No dogs available for this page.")
