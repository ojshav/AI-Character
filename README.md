# AI Character Social Feed Generator

This Streamlit application allows users to create AI-based virtual characters and generate dynamic social media posts, complete with text and AI-generated images, reflecting the character's profile, hobbies, and personality traits. 

## Features
- **AI Character Creation**: Customize the character's name, age, location, profession, hobbies, and personality traits.
- **Daily Routine Simulation**: View a generated daily routine for the character.
- **Social Media Post Generation**: Automatically create realistic text posts using AI.
- **Image Generation**: Generate matching images for each text post using AI-based tools like Hugging Face Diffusers.
- **Streamlit Integration**: User-friendly interface for seamless interaction.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/ai-character-social-feed.git
   cd ai-character-social-feed
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
3. Set up environment variables: Create a .env file in the project root and add the following:
   ```env
   GROQ_API_KEY=<your_groq_api_key>
   HF_TOKEN=<your_huggingface_api_token>
4. Run the application:
   ```bash
   streamlit run app.py
## How It Works
- Create an AI Character: Fill out the form to define your character's attributes, such as name, age, and personality traits.
- Generate Posts: The app generates three social media posts with corresponding AI-generated images.
- View Results: Explore the posts and images in an interactive format within the Streamlit app.

## Technologies Used
- Python: The core programming language used.
- Streamlit: For building the user interface.
- Stable Diffusion: For AI-based image generation.
- Hugging Face: For integrating with LLMs and image generation APIs.
- Groq: For text generation and AI-powered social media post creation.
- PIL (Pillow): For image processing.
- dotenv: For managing environment variables.

  

   
