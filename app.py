from flask import Flask, render_template, jsonify, request
import random
from openai import OpenAI
from dotenv import load_dotenv
import os 
app = Flask(__name__)
load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


# Mapping tone options to dynamic prompts
TONE_PROMPTS = {
    "funny": "Generate a witty and humorous icebreaker for asking someone out. It should be playful and lighthearted.",
    "serious": "Create a sincere and thoughtful icebreaker for asking someone on a date. It should be genuine and respectful.",
    "romantic": "Generate a romantic and charming icebreaker to express interest in someone. It should be sweet and heartfelt."
}

def generate_icebreaker(tone):
    """Generate an icebreaker based on the selected tone using OpenAI"""
    prompt = TONE_PROMPTS.get(tone, TONE_PROMPTS["funny"])  # Default to funny if no valid tone

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "system", "content": prompt}]
    )

    icebreaker = response.choices[0].message.content.strip()
    return icebreaker
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/icebreaker', methods=['GET'])
def get_icebreaker():
    """Returns an AI-generated icebreaker based on user-selected tone"""
    tone = request.args.get('tone', 'funny').lower()  # Get tone from query params
    icebreaker = generate_icebreaker(tone)
    return jsonify({'icebreaker': icebreaker})
@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')

    if not user_message:
        return jsonify({'response': "Hmm, I didn't quite get that. Try again! 😊"})

    # Call OpenAI API
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an AI assistant that helps people craft confident and natural date invitations."},
                {"role": "user", "content": user_message}
            ]
        )
        bot_response = response.choices[0].message.content.strip()
    except Exception as e:
        bot_response = "Oops! Something went wrong. Try again later. 😢"

    return jsonify({'response': bot_response})
if __name__ == '__main__':
    app.run(debug=True)
