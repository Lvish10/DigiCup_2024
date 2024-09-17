from flask import Flask, request, jsonify, send_from_directory, render_template
import openai
import json
import datetime
import os

app = Flask(__name__)

# Set your OpenAI API key
openai.api_key = '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'

# Get the base directory of the current script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load data from JSON files using absolute path
def load_json(filename):
    try:
        with open(os.path.join(BASE_DIR, filename), 'r') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error loading {filename}: {e}")
        return {}
    except FileNotFoundError:
        print(f"{filename} not found.")
        return {}

fish_data = load_json('fish.json')
marine_data = load_json('marine_data.json')
marine_laws = load_json('marine_laws.json')

def get_greeting():
    now = datetime.datetime.now()
    hour = now.hour

    if 5 <= hour < 12:
        return "Good Morning! Hope you are fine! How can I assist you today?"
    elif 12 <= hour < 18:
        return "Good Afternoon! Hope you are fine! How can I assist you this afternoon?"
    else:
        return "Good Evening! Hope you are fine! How can I make your evening better?"

def get_intro():
    return "I’m here to help with any queries you might have. Feel free to ask me anything!"

def get_marine_species_info(species_name):
    species = marine_data.get("marine_species", {}).get(species_name.lower(), None)
    if species:
        return f"{species['description']}\nHabitat: {species['habitat']}\nConservation Status: {species['conservation_status']}\nNotes: {species['notes']}"
    else:
        return "Sorry, I don't have information about that species."

def get_marine_ecosystem_info(ecosystem_name):
    ecosystem = marine_data.get("marine_ecosystems", {}).get(ecosystem_name.lower(), None)
    if ecosystem:
        locations = ", ".join(ecosystem["locations"])
        return f"{ecosystem['description']}\nLocations: {locations}\nConservation Efforts: {ecosystem['conservation_efforts']}"
    else:
        return "Sorry, I don't have information about that ecosystem."

def get_marine_law_info(law_topic):
    law_info = marine_laws.get("laws", {}).get(law_topic.lower().replace(" ", "_"), None)
    if law_info:
        return law_info
    else:
        return "Sorry, I don't have specific information about that law topic."

def get_fish_info(fish_name):
    fish = fish_data.get("fish_species", {}).get(fish_name.lower(), None)
    if fish:
        return f"{fish['description']}\nHabitat: {fish['habitat']}\nConservation Status: {fish['conservation_status']}\nNotes: {fish['notes']}"
    else:
        return "Sorry, I don't have information about that fish species."

@app.route('/')
def index():
    return render_template('index.html')  # Serve the HTML file from templates directory

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '').strip().lower()

    # Initial greeting and introduction
    if 'hello' in user_message or 'hi' in user_message or 'hey' in user_message:
        bot_message = get_greeting() + " " + get_intro()
    # Marine life related queries
    elif "marine" in user_message or "sea" in user_message or "ocean" in user_message:
        if any(keyword in user_message for keyword in
               ["dugong", "nassau grouper", "sea turtle", "humpback whale", "giant clam", "sharks", "rays"]):
            if "dugong" in user_message:
                bot_message = get_marine_species_info("dugong")
            elif "nassau grouper" in user_message:
                bot_message = get_marine_species_info("nassau_grouper")
            elif "sea turtle" in user_message:
                bot_message = get_marine_species_info("sea_turtle")
            elif "humpback whale" in user_message:
                bot_message = get_marine_species_info("humpback_whale")
            elif "giant clam" in user_message:
                bot_message = get_marine_species_info("giant_clam")
            elif "sharks" in user_message:
                bot_message = get_marine_species_info("sharks")
            elif "rays" in user_message:
                bot_message = get_marine_species_info("rays")
        elif any(keyword in user_message for keyword in ["coral reef", "seagrass bed", "mangroves"]):
            if "coral reef" in user_message:
                bot_message = get_marine_ecosystem_info("coral_reefs")
            elif "seagrass bed" in user_message:
                bot_message = get_marine_ecosystem_info("seagrass_beds")
            elif "mangroves" in user_message:
                bot_message = get_marine_ecosystem_info("mangroves")
        elif any(keyword in user_message for keyword in
                 ["dugong protection", "nassau grouper regulations", "coral reef protection",
                  "seagrass bed conservation"]):
            if "dugong protection" in user_message:
                bot_message = get_marine_law_info("dugong_protection")
            elif "nassau grouper regulations" in user_message:
                bot_message = get_marine_law_info("nassau_grouper_regulations")
            elif "coral reef protection" in user_message:
                bot_message = get_marine_law_info("coral_reef_protection")
            elif "seagrass bed conservation" in user_message:
                bot_message = get_marine_law_info("seagrass_bed_conservation")
        elif any(keyword in user_message for keyword in
                 ["napoleon wrasse", "parrotfish", "yellowtail snapper", "tuna", "lionfish"]):
            if "napoleon wrasse" in user_message:
                bot_message = get_fish_info("napoleon_wrasse")
            elif "parrotfish" in user_message:
                bot_message = get_fish_info("parrotfish")
            elif "yellowtail snapper" in user_message:
                bot_message = get_fish_info("yellowtail_snapper")
            elif "tuna" in user_message:
                bot_message = get_fish_info("tuna")
            elif "lionfish" in user_message:
                bot_message = get_fish_info("lionfish")
        else:
            bot_message = "I can provide information about marine species, ecosystems, fish species, and related laws. Please ask me specific questions about these topics."
    else:
        # Use GPT-4 to handle other queries
        response = openai.Completion.create(
            model="gpt-4",
            prompt=f"You are a friendly and knowledgeable assistant. Respond to the following user question as naturally and informatively as possible:\n\n{user_message}",
            max_tokens=150,
            temperature=0.9
        )
        bot_message = response.choices[0].text.strip()

    return jsonify({'response': bot_message})

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(BASE_DIR, 'static'), 'favicon.ico')

if __name__ == '__main__':
    app.run(debug=True)
