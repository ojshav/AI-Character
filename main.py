import streamlit as st
import random
from datetime import datetime
from groq import Groq
import time
from dotenv import load_dotenv
import os
from diffusers import StableDiffusionPipeline
import torch
from PIL import Image
import io
from huggingface_hub import InferenceClient

# Define the AI character's profile
class AICharacter:
    def __init__(self, name, age, location, profession, hobbies, personality_traits):
        self.name = name
        self.age = age
        self.location = location
        self.profession = profession
        self.hobbies = hobbies
        self.personality_traits = personality_traits
        self.daily_routine = self.generate_daily_routine()

    def generate_daily_routine(self):
        return [
            ("Morning", random.choice(["Go for a jog", "Make coffee", "Read a book"])),
            ("Afternoon", random.choice(["Work on projects", "Have lunch", "Study"])),
            ("Evening", random.choice(["Watch a movie", "Go for a walk", "Cook dinner"])),
        ]

# Generate dynamic social media posts
class PostGenerator:
    def __init__(self, character):
        self.character = character
        try:
            # Load environment variables
            load_dotenv()
            self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
            
            # Initialize HuggingFace client
            self.hf_client = InferenceClient(
                "seawolf2357/ntower",
                token=os.getenv("HF_TOKEN")
            )
        except Exception as e:
            st.error(f"Error initializing AI clients: {e}")
            self.client = None
            self.hf_client = None

    def generate_text_post(self):
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": f"Imagine a {self.character.age}-year-old named {self.character.name} from {self.character.location}, "
                        f"who is {self.character.profession} and enjoys {', '.join(self.character.hobbies)}. "
                        f"Write a social media post reflecting their personality: {', '.join(self.character.personality_traits)}."
                    }
                ],
                model="mixtral-8x7b-32768",
                temperature=0.7,
                max_tokens=1000,
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            print(f"Error generating text post: {e}")
            return "Unable to generate text post at this time."

    def generate_image_from_text(self, text_post):
        try:
            # Generate a suitable image prompt from the text post
            image_prompt = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": f"Based on this social media post: '{text_post}', "
                        f"create a short, descriptive prompt for generating an image that would accompany this post. "
                        f"Make it visual and specific, but keep it under 50 words."
                    }
                ],
                model="mixtral-8x7b-32768",
                temperature=0.7,
                max_tokens=50,
            ).choices[0].message.content

            # Generate the image using FLUX
            image = self.hf_client.text_to_image(image_prompt)
            
            # Convert PIL image to bytes for Streamlit
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()
            
            return {
                "prompt": image_prompt,
                "image": img_byte_arr
            }
        except Exception as e:
            st.error(f"Error generating image: {e}")
            return None

    def generate_daily_posts(self):
        posts = []
        for _ in range(3):  # Always generate 3 posts
            # Generate text post
            text_content = self.generate_text_post()
            # Generate matching image
            image_content = self.generate_image_from_text(text_content)
            
            posts.append({
                "text": text_content,
                "image": image_content
            })
            
            # Add a small delay between posts to avoid rate limiting
            time.sleep(2)
            
        return posts

# Simulate daily activity
class AISimulation:
    def __init__(self, character):
        self.character = character
        self.post_generator = PostGenerator(character)

    def simulate_day(self):
        today = datetime.now()
        posts = self.post_generator.generate_daily_posts()
        print(f"{today.strftime('%Y-%m-%d')}: {self.character.name}'s Posts")
        for i, post in enumerate(posts, 1):
            print(f"Post {i}: {post}\n")

class StreamlitApp:
    def __init__(self):
        st.set_page_config(page_title="AI Character Social Feed", layout="wide")
        st.title("AI Character Social Feed Generator")

    def create_character_form(self):
        with st.form("character_creation"):
            st.subheader("Create Your AI Character")
            name = st.text_input("Name", value="Aria")
            age = st.number_input("Age", min_value=1, max_value=100, value=25)
            location = st.text_input("Location", value="San Francisco")
            profession = st.text_input("Profession", value="Graphic Designer")
            hobbies = st.text_input("Hobbies (comma-separated)", value="painting, hiking, playing guitar")
            personality_traits = st.text_input("Personality Traits (comma-separated)", 
                                             value="creative, curious, adventurous")

            submitted = st.form_submit_button("Generate Posts")
            if submitted:
                return AICharacter(
                    name=name,
                    age=age,
                    location=location,
                    profession=profession,
                    hobbies=[hobby.strip() for hobby in hobbies.split(",")],
                    personality_traits=[trait.strip() for trait in personality_traits.split(",")]
                )
        return None

    def display_character_info(self, character):
        st.sidebar.subheader("Character Profile")
        st.sidebar.write(f"**Name:** {character.name}")
        st.sidebar.write(f"**Age:** {character.age}")
        st.sidebar.write(f"**Location:** {character.location}")
        st.sidebar.write(f"**Profession:** {character.profession}")
        st.sidebar.write("**Hobbies:**")
        for hobby in character.hobbies:
            st.sidebar.write(f"- {hobby}")
        st.sidebar.write("**Personality Traits:**")
        for trait in character.personality_traits:
            st.sidebar.write(f"- {trait}")

    def display_daily_routine(self, character):
        st.subheader("Daily Routine")
        cols = st.columns(3)
        for (time_of_day, activity), col in zip(character.daily_routine, cols):
            with col:
                st.write(f"**{time_of_day}:**")
                st.write(activity)

    def run(self):
        character = self.create_character_form()
        
        if character:
            self.display_character_info(character)
            self.display_daily_routine(character)
            
            post_generator = PostGenerator(character)
            
            st.subheader("Generated Social Media Posts")
            with st.spinner("Generating posts and images..."):
                posts = post_generator.generate_daily_posts()
                
                for i, post in enumerate(posts, 1):
                    with st.container():
                        st.markdown("---")
                        st.write(f"**Post {i}** - {datetime.now().strftime('%I:%M %p')}")
                        
                        # Display the text post
                        st.write(post["text"])
                        
                        # Display the generated image if available
                        if post["image"]:
                            with st.expander("View generated image"):
                                st.write(f"*Image prompt: {post['image']['prompt']}*")
                                st.image(post['image']['image'], caption="Generated Image")

if __name__ == "__main__":
    app = StreamlitApp()
    app.run()


