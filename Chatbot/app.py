from flask import Flask, request, jsonify, send_from_directory, render_template
import openai
import datetime
import os
from fuzzywuzzy import process

app = Flask(__name__)

# Set your OpenAI API key
openai.api_key = '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'

# Combined data directly in the code
fish_data = {
    "fish_species": {
        "napoleon_wrasse": {
            "description": "The Napoleon wrasse is a large, colorful reef fish found in the Indian and Pacific Oceans.",
            "habitat": "Coral reefs around Mauritius.",
            "conservation_status": "Vulnerable",
            "notes": "It is protected under Mauritian law due to its declining population."
        },
        "parrotfish": {
            "description": "Parrotfish are known for their bright colors and their beak-like teeth used for scraping algae off coral reefs.",
            "habitat": "Coral reefs and seagrass beds.",
            "conservation_status": "Least Concern",
            "notes": "Important for the health of coral reefs as they help control algae growth."
        },
        "yellowtail_snapper": {
            "description": "A common fish found in tropical waters, recognized by its yellow tail and body.",
            "habitat": "Reef and pelagic zones.",
            "conservation_status": "Least Concern",
            "notes": "Popular in local fisheries and as a food source."
        },
        "tuna": {
            "description": "Tuna are large, fast-swimming fish known for their commercial value and migratory behavior.",
            "habitat": "Pelagic waters, often far from shore.",
            "conservation_status": "Varies by species",
            "notes": "Overfishing concerns exist for some species."
        },
        "lionfish": {
            "description": "Lionfish are known for their venomous spines and striking appearance.",
            "habitat": "Coral reefs and rocky crevices.",
            "conservation_status": "Invasive species",
            "notes": "Their introduction to non-native areas can threaten local ecosystems."
        },
        "surgeonfish": {
            "description": "Surgeonfish are known for their bright colors and sharp spines on their tails.",
            "habitat": "Coral reefs.",
            "conservation_status": "Least Concern",
            "notes": "They play a crucial role in controlling algae growth on reefs."
        },
        "grouper": {
            "description": "Groupers are robust fish that are often found in rocky or coral reef environments.",
            "habitat": "Coral reefs and rocky areas.",
            "conservation_status": "Varies by species",
            "notes": "Some species are popular targets for fishing."
        },
        "rabbitfish": {
            "description": "Rabbitfish have a distinctive rabbit-like face and are known for their herbivorous diet.",
            "habitat": "Coral reefs and seagrass beds.",
            "conservation_status": "Least Concern",
            "notes": "They are often seen in schools and are important for reef health."
        },
        "barracuda": {
            "description": "Barracudas are large, predatory fish known for their speed and sharp teeth.",
            "habitat": "Open waters and near reefs.",
            "conservation_status": "Least Concern",
            "notes": "They are often feared by smaller fish and are a popular game fish."
        },
        "bluespine_unicornfish": {
            "description": "This fish is recognized by its long, horn-like projection on its forehead.",
            "habitat": "Coral reefs.",
            "conservation_status": "Least Concern",
            "notes": "They are often seen in schools and feed primarily on algae."
        },
        "yellowfin_tuna": {
            "description": "Yellowfin tuna are highly valued for their meat and are known for their speed.",
            "habitat": "Pelagic waters.",
            "conservation_status": "Overfished",
            "notes": "Sustainability efforts are important for their populations."
        },
        "octopus": {
            "description": "Octopuses are intelligent mollusks known for their problem-solving abilities.",
            "habitat": "Rocky reefs and coral formations.",
            "conservation_status": "Varies by species",
            "notes": "They are skilled at camouflage and are a popular seafood choice."
        },
        "scad": {
            "description": "Scads are small to medium-sized fish often found in schools.",
            "habitat": "Coastal waters.",
            "conservation_status": "Least Concern",
            "notes": "They are important forage fish for larger predators."
        },
        "moray_eel": {
            "description": "Moray eels have elongated bodies and are often found hiding in crevices.",
            "habitat": "Coral reefs.",
            "conservation_status": "Least Concern",
            "notes": "They are generally shy but can be aggressive if provoked."
        },
    }
}

marine_data = {
    "marine_species": {
        "dugong": {
            "description": "The dugong is a large marine mammal found in warm coastal waters.",
            "habitat": "Shallow coastal waters and seagrass beds.",
            "conservation_status": "Vulnerable",
            "notes": "Dugongs are herbivores and play a key role in seagrass ecosystems."
        },
        "nassau_grouper": {
            "description": "The Nassau grouper is a large fish found in the Caribbean and western Atlantic.",
            "habitat": "Coral reefs and rocky areas.",
            "conservation_status": "Endangered",
            "notes": "Overfishing has severely impacted their populations."
        },
        "mauritian_blacktip_shark": {
            "description": "A medium-sized shark known for its distinctive black-tipped fins.",
            "habitat": "Coral reefs and coastal waters.",
            "conservation_status": "Near Threatened",
            "notes": "Important for marine ecosystems and ecotourism."
        },
        "mauritian_scad": {
            "description": "A fast-swimming fish often found in schools.",
            "habitat": "Coastal waters and reefs.",
            "conservation_status": "Least Concern",
            "notes": "Popular among local fishers and divers."
        },
        "mauritius_goatfish": {
            "description": "Recognized by their two whisker-like barbs on the chin.",
            "habitat": "Sandy bottoms and coral reefs.",
            "conservation_status": "Least Concern",
            "notes": "Important for local fisheries."
        },
        "squirrelfish": {
            "description": "Known for their large eyes and red coloration.",
            "habitat": "Coral reefs and rocky areas.",
            "conservation_status": "Least Concern",
            "notes": "Nocturnal and often hide during the day."
        },
        "lizardfish": {
            "description": "Recognized for their elongated bodies and sharp teeth.",
            "habitat": "Sandy and muddy bottoms near reefs.",
            "conservation_status": "Least Concern",
            "notes": "Ambush predators that rely on camouflage."
        },
        "bottlenose_dolphin": {
            "description": "A highly intelligent and social marine mammal known for its playful behavior.",
            "habitat": "Coastal waters and often seen in pods.",
            "conservation_status": "Least Concern",
            "notes": "Commonly spotted off the coast of Mauritius."
        },
        "sperm_whale": {  
            "description": "The largest of the toothed whales, known for its deep diving abilities.",
            "habitat": "Deep ocean waters.",
            "conservation_status": "Vulnerable",
            "notes": "Migrates through Mauritian waters, primarily for feeding."
        },
        "humpback_whale": {
            "description": "Known for its acrobatic breaches and songs, humpback whales migrate through Mauritian waters.",
            "habitat": "Open ocean, often near coastal areas during migration.",
            "conservation_status": "Humpback whales are recovering from past whaling.",
            "notes": "Typically seen between June and November during their migration."
        }
    },
    "marine_ecosystems": {
        "coral_reefs": {
            "description": "Coral reefs are underwater ecosystems characterized by reef-building corals.",
            "locations": ["Mauritius", "Rodrigues", "Agaléga"],
            "conservation_efforts": "Marine protected areas and reef restoration projects."
        },
        "seagrass_beds": {
            "description": "Seagrass beds are underwater meadows of flowering plants that provide critical habitat for various marine species.",
            "locations": ["Shallow coastal waters of Mauritius"],
            "conservation_efforts": "Protection and restoration initiatives to support marine biodiversity."
        },
        "mangroves": {
            "description": "Mangrove forests are coastal ecosystems that provide important habitats for fish and other wildlife.",
            "locations": ["Mauritius coastlines"],
            "conservation_efforts": "Rehabilitation projects and conservation policies to protect these vital ecosystems."
        }
    }
}

marine_laws = {
    "laws": {
        "fishing_regulations": "Fishing regulations in Mauritius include restrictions on the size and type of fish that can be caught, and certain species are protected.",
        "marine_protected_areas": "Marine protected areas (MPAs) are designated to protect critical habitats and biodiversity. Fishing is restricted or prohibited in these areas.",
        "safety_regulations": "Maritime safety regulations in Mauritius include mandatory safety equipment on vessels and adherence to navigation rules.",
        "conservation_of_marine_biodiversity": "The Wildlife and National Parks Act aims to protect marine biodiversity by prohibiting the capture of certain threatened species and enforcing penalties for illegal fishing activities.",
        "licensing_and_permits": "Fishermen must obtain licenses to fish commercially, and specific permits are required for fishing in protected areas or for targeting certain species.",
        "size_and_catch_limits": "Regulations exist regarding the minimum size for catchable species and established catch limits for certain fish to ensure sustainability.",
        "no_take_zones": "Certain areas are designated as no-take zones where all fishing is prohibited to allow ecosystems to recover and thrive.",
        "environmental_impact_assessments": "Activities such as coastal development or marine resource extraction require environmental impact assessments to evaluate potential effects on marine ecosystems.",
        "waste_management_regulations": "Regulations exist for managing waste disposal from vessels to minimize pollution in marine environments.",
        "community_fishing_rights": "Local fishing communities may have rights to specific fishing areas, promoting sustainable practices and ensuring access to resources.",
        "invasive_species_control": "Measures are in place to manage and prevent the introduction of invasive species that threaten local marine ecosystems."
    }
}

def get_greeting():
    now = datetime.datetime.now()
    hour = now.hour
    if 5 <= hour < 12:
        return "Good Morning!"
    elif 12 <= hour < 18:
        return "Good Afternoon!"
    else:
        return "Good Evening!"

def get_intro():
    return "I’m here to help with any queries you might have. Feel free to ask me anything!"

def get_fish_info(fish_name):
    fish = fish_data.get("fish_species", {}).get(fish_name.lower(), None)
    if fish:
        return (f"{fish['description']}\n"
                f"Habitat: {fish['habitat']}\n"
                f"Conservation Status: {fish['conservation_status']}\n"
                f"Notes: {fish['notes']}")
    return "Sorry, I don't have information about that fish species."

def fuzzy_match(query, choices, threshold=80):
    match, score = process.extractOne(query, choices)
    if score >= threshold:
        return match
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '').strip().lower()

    # Define keywords for specific topics dynamically
    fish_keywords = list(fish_data["fish_species"].keys())
    marine_data_keywords = list(marine_data["marine_species"].keys()) + list(marine_data["marine_ecosystems"].keys())
    marine_laws_keywords = list(marine_laws['laws'].keys())
    goodbye_keywords = ["bye", "goodbye", "see you", "take care", "farewell"]

    if any(greeting in user_message for greeting in ["hello", "hi", "hey"]):
        bot_message = f"{get_greeting()} {get_intro()}"
    elif any(fish in user_message for fish in fish_keywords):
        for fish in fish_keywords:
            if fish in user_message:
                bot_message = get_fish_info(fish)
                break
    elif "mangroves" in user_message:
        bot_message = (f"Mangrove forests are coastal ecosystems that provide important habitats for fish and other wildlife. "
                       f"They help stabilize coastlines, protect against erosion, and support biodiversity. "
                       f"Conservation efforts include rehabilitation projects and policies to protect these vital ecosystems.")
    elif "seagrass beds" in user_message:
        bot_message = (f"Seagrass beds are underwater meadows of flowering plants that provide critical habitat for various marine species. "
                       f"They play a vital role in maintaining healthy coastal ecosystems and are important for biodiversity. "
                       f"Conservation efforts include protection and restoration initiatives.")
    elif "marine ecosystems" in user_message:
        bot_message = "Marine ecosystems include various environments such as coral reefs, seagrass beds, and mangroves. They are crucial for biodiversity and ocean health."
    elif "coral reefs" in user_message:
        bot_message = "Coral reefs are underwater ecosystems characterized by reef-building corals. They are found in warm, shallow waters and are vital for marine life."
    elif any(keyword in user_message for keyword in marine_laws_keywords):
        bot_message = "\n".join([f"{law}: {detail}" for law, detail in marine_laws['laws'].items()])
    elif any(keyword in user_message for keyword in marine_data_keywords):
        bot_message = "I can provide information about marine ecosystems, conservation efforts, and fishing regulations. Please specify what you're interested in!"
    elif any(goodbye in user_message for goodbye in goodbye_keywords):
        bot_message = "Goodbye! If you have more questions in the future, feel free to ask. Take care!"
    else:
        # Attempt to use GPT for broader queries
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": user_message}],
                max_tokens=150,
                temperature=0.9
            )
            bot_message = response.choices[0].message['content'].strip()
        except Exception as e:
            bot_message = "I can't access external information at the moment. Please ask about specific fish or local marine data."

    return jsonify({'response': bot_message})

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static'), 'favicon.ico')

if __name__ == '__main__':
    app.run(debug=True)
