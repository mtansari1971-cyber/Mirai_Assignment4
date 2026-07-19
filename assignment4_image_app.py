import streamlit as st
import requests
import random
from urllib.parse import quote


# Page Configuration

st.set_page_config(page_title="AI Image Studio", page_icon="🎨")

st.title("🎨 AI Image Studio")
st.write("Generate AI images using Pollinations AI")


# Sidebar

st.sidebar.header("⚙️ Image Settings")

width = st.sidebar.slider("Width", 256, 1024, 512, step=64)
height = st.sidebar.slider("Height", 256, 1024, 512, step=64)

art_style = st.sidebar.selectbox(
    "Art Style",
    [
        "Realistic",
        "Anime",
        "Cyberpunk",
        "Fantasy",
        "Watercolor",
        "Oil Painting",
        "Pixel Art"
    ]
)

magic_enhance = st.sidebar.checkbox("✨ Enable Magic Enhance")


# User Prompt

user_prompt = st.text_input(
    "Enter your prompt",
    placeholder="Example: A tiger riding a bicycle"
)


# Surprise Prompts

surprise_prompts = [
    "An astronaut riding a horse on Mars",
    "A cyberpunk street food vendor in Tokyo",
    "A dragon drinking coffee in a library",
    "A giant whale flying over New York City",
    "A panda working as a software engineer"
]



# Function to Generate Image

def generate_image(prompt):

    full_prompt = f"{prompt}, {art_style} style"

    if magic_enhance:
        full_prompt += ", masterpiece, 8k resolution, highly detailed, trending on artstation, unreal engine 5 render"

    encoded_prompt = quote(full_prompt)

    # Task 1
    url = (
        f"https://image.pollinations.ai/prompt/{encoded_prompt}"
        f"?width={width}&height={height}"
    )

    response = requests.get(url)

    if response.status_code == 200:

        st.image(
            response.content,
            caption="Generated Image",
            use_container_width=True
        )

        # Task 2
        st.download_button(
            "⬇ Download Image",
            response.content,
            file_name=f"{art_style}_image.png",
            mime="image/png"
        )

    else:
        st.error("Failed to generate image.")



# Buttons

col1, col2 = st.columns(2)

with col1:
    generate = st.button("🎨 Generate Image")

with col2:
    surprise = st.button("🎲 Surprise Me!")


# Generate Button Logic

if generate:

    if user_prompt.strip() == "":
        st.warning("Please enter a prompt.")
    else:
        generate_image(user_prompt)



# Surprise Button Logic

if surprise:

    random_prompt = random.choice(surprise_prompts)

    st.success(f"Surprise Prompt: {random_prompt}")

    generate_image(random_prompt)