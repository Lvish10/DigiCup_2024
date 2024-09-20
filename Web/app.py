from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify, send_from_directory, render_template
import openai
import datetime
import os
from fuzzywuzzy import process

app = Flask(__name__)
Bootstrap(app)
app.secret_key = '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'  # Replace with a strong secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///volunteers.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Dummy user data for example purposes
users = {
    'admin@example.com': generate_password_hash('password')  # Example hash; replace with real hashed passwords
}

# Database model for volunteers
class Volunteer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    message = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Volunteer {self.name}>'

# Home Page
@app.route('/')
def home():
    return render_template('home.html', title='Home', css_file='home.css', js_file='home.js')

# About Page
@app.route('/about')
def about():
    return render_template('about.html', title='About Us', css_file='about.css', js_file='about.js')

# Maps Page
@app.route('/maps')
def maps():
    return render_template('maps.html', title='Maps', css_file='maps.css', js_file='maps.js')

# E-Learning Page
@app.route('/elearning')
def elearning():
    subjects = {
        'maths': 'Maths',
        'english': 'English',
        'french': 'French',
        'history': 'History',
        'geography': 'Geography',
        'science': 'Science',
        'marine_species': 'Marine Species',
        'marine_ecosystems': 'Marine Ecosystems',
        'conservation': 'Conservation',
        'marine_policies': 'Marine Policies',
        'marine_science': 'Marine Science'
    }
    return render_template('elearning.html', title='E-Learning', subjects=subjects, css_file='elearning.css', js_file='elearning.js')

# Dynamic Subject Pages
@app.route('/elearning/<subject_name>')
def subject(subject_name):
    subjects = {
        'maths': 'Maths',
        'english': 'English',
        'french': 'French',
        'history': 'History',
        'geography': 'Geography',
        'science': 'Science',
        'marine_species': 'Marine Species',
        'marine_ecosystems': 'Marine Ecosystems',
        'conservation': 'Conservation',
        'marine_policies': 'Marine Policies',
        'marine_science': 'Marine Science'
    }
    
    if subject_name in subjects:
        if subject_name in ['marine_species', 'marine_ecosystems', 'conservation', 'marine_policies', 'marine_science']:
            base_template = 'base_marine.html'
        else:
            base_template = 'base_general.html'
        
        return render_template(
            f'subjects/{subject_name}/syllabus.html',
            title=subjects[subject_name],
            css_file=f'{subject_name}.css',
            js_file=f'{subject_name}.js',
            base_template=base_template
        )
    else:
        return render_template('404.html', title='404 Not Found'), 404

# Dynamic Topic Pages
@app.route('/elearning/<subject_name>/topics')
def topics(subject_name):
    subjects = {
        'maths': ['Algebra', 'Geometry', 'Calculus'],
        'english': ['Grammar', 'Literature', 'Writing'],
        'french': ['Grammar', 'Literature', 'Conversation'],
        'history': ['Ancient History', 'Modern History'],
        'geography': ['Physical Geography', 'Human Geography'],
        'science': ['Biology', 'Chemistry', 'Physics'],
        'marine_species': ['Fish', 'Corals', 'Mammals'],
        'marine_ecosystems': ['Coral Reefs', 'Mangroves', 'Open Ocean'],
        'conservation': ['Marine Conservation', 'Protected Areas'],
        'marine_policies': ['International Agreements', 'Local Regulations'],
        'marine_science': ['Oceanography', 'Marine Biology']
    }
    
    if subject_name in subjects:
        topics_list = subjects[subject_name]
        base_template = 'base_marine.html' if subject_name in ['marine_species', 'marine_ecosystems', 'conservation', 'marine_policies', 'marine_science'] else 'base_general.html'
        return render_template(
            f'subjects/{subject_name}/topics.html',
            title=f'{subjects[subject_name]} Topics',
            css_file=f'{subject_name}.css',
            js_file=f'{subject_name}.js',
            topics=topics_list,
            base_template=base_template
        )
    else:
        return render_template('404.html', title='404 Not Found'), 404

# Dynamic Topic Details Page
@app.route('/elearning/<subject_name>/topics/<topic_name>')
def topic_details(subject_name, topic_name):
    subjects = {
        'maths': {
            'Algebra': {'intro': 'Introduction to Algebra', 'key_points': ['Equations', 'Functions'], 'resources': [{'name': 'Algebra Resource', 'url': '#'}]},
            'Geometry': {'intro': 'Introduction to Geometry', 'key_points': ['Shapes', 'Angles'], 'resources': [{'name': 'Geometry Resource', 'url': '#'}]},
            'Calculus': {'intro': 'Introduction to Calculus', 'key_points': ['Limits', 'Derivatives'], 'resources': [{'name': 'Calculus Resource', 'url': '#'}]}
        },
        'english': {
            'Grammar': {'intro': 'Introduction to Grammar', 'key_points': ['Parts of Speech', 'Sentence Structure'], 'resources': [{'name': 'Grammar Resource', 'url': '#'}]},
            'Literature': {'intro': 'Introduction to Literature', 'key_points': ['Genres', 'Themes'], 'resources': [{'name': 'Literature Resource', 'url': '#'}]},
            'Writing': {'intro': 'Introduction to Writing', 'key_points': ['Essay Structure', 'Creative Writing'], 'resources': [{'name': 'Writing Resource', 'url': '#'}]}
        },
        'french': {
            'Grammar': {'intro': 'Introduction to French Grammar', 'key_points': ['Nouns', 'Verbs'], 'resources': [{'name': 'French Grammar Resource', 'url': '#'}]},
            'Literature': {'intro': 'Introduction to French Literature', 'key_points': ['Authors', 'Genres'], 'resources': [{'name': 'French Literature Resource', 'url': '#'}]},
            'Conversation': {'intro': 'Introduction to French Conversation', 'key_points': ['Common Phrases', 'Pronunciation'], 'resources': [{'name': 'French Conversation Resource', 'url': '#'}]}
        },
        'history': {
            'Ancient History': {'intro': 'Introduction to Ancient History', 'key_points': ['Civilizations', 'Key Events'], 'resources': [{'name': 'Ancient History Resource', 'url': '#'}]},
            'Modern History': {'intro': 'Introduction to Modern History', 'key_points': ['Revolutions', 'Recent Events'], 'resources': [{'name': 'Modern History Resource', 'url': '#'}]}
        },
        'geography': {
            'Physical Geography': {'intro': 'Introduction to Physical Geography', 'key_points': ['Landforms', 'Climate'], 'resources': [{'name': 'Physical Geography Resource', 'url': '#'}]},
            'Human Geography': {'intro': 'Introduction to Human Geography', 'key_points': ['Population', 'Urbanization'], 'resources': [{'name': 'Human Geography Resource', 'url': '#'}]}
        },
        'science': {
            'Biology': {'intro': 'Introduction to Biology', 'key_points': ['Cells', 'Genetics'], 'resources': [{'name': 'Biology Resource', 'url': '#'}]},
            'Chemistry': {'intro': 'Introduction to Chemistry', 'key_points': ['Elements', 'Reactions'], 'resources': [{'name': 'Chemistry Resource', 'url': '#'}]},
            'Physics': {'intro': 'Introduction to Physics', 'key_points': ['Forces', 'Energy'], 'resources': [{'name': 'Physics Resource', 'url': '#'}]}
        },
        'marine_species': {
            'Fish': {'intro': 'Introduction to Fish', 'key_points': ['Types of Fish', 'Habitat'], 'resources': [{'name': 'Fish Resource', 'url': '#'}]},
            'Corals': {'intro': 'Introduction to Corals', 'key_points': ['Coral Species', 'Ecosystem'], 'resources': [{'name': 'Coral Resource', 'url': '#'}]},
            'Mammals': {'intro': 'Introduction to Marine Mammals', 'key_points': ['Species', 'Conservation'], 'resources': [{'name': 'Mammals Resource', 'url': '#'}]}
        },
        'marine_ecosystems': {
            'Coral Reefs': {'intro': 'Introduction to Coral Reefs', 'key_points': ['Reef Formation', 'Biodiversity'], 'resources': [{'name': 'Coral Reefs Resource', 'url': '#'}]},
            'Mangroves': {'intro': 'Introduction to Mangroves', 'key_points': ['Mangrove Species', 'Ecological Importance'], 'resources': [{'name': 'Mangroves Resource', 'url': '#'}]},
            'Open Ocean': {'intro': 'Introduction to Open Ocean', 'key_points': ['Ocean Zones', 'Marine Life'], 'resources': [{'name': 'Open Ocean Resource', 'url': '#'}]}
        },
        'conservation': {
            'Marine Conservation': {'intro': 'Introduction to Marine Conservation', 'key_points': ['Conservation Strategies', 'Protected Areas'], 'resources': [{'name': 'Marine Conservation Resource', 'url': '#'}]},
            'Protected Areas': {'intro': 'Introduction to Protected Areas', 'key_points': ['Marine Reserves', 'Management'], 'resources': [{'name': 'Protected Areas Resource', 'url': '#'}]}
        },
        'marine_policies': {
            'International Agreements': {'intro': 'Introduction to International Agreements', 'key_points': ['Key Agreements', 'Signatories'], 'resources': [{'name': 'International Agreements Resource', 'url': '#'}]},
            'Local Regulations': {'intro': 'Introduction to Local Regulations', 'key_points': ['Regulations Overview', 'Enforcement'], 'resources': [{'name': 'Local Regulations Resource', 'url': '#'}]}
        },
        'marine_science': {
            'Oceanography': {'intro': 'Introduction to Oceanography', 'key_points': ['Ocean Circulation', 'Marine Chemistry'], 'resources': [{'name': 'Oceanography Resource', 'url': '#'}]},
            'Marine Biology': {'intro': 'Introduction to Marine Biology', 'key_points': ['Marine Ecosystems', 'Species Diversity'], 'resources': [{'name': 'Marine Biology Resource', 'url': '#'}]}
        }
    }
    
    if subject_name in subjects and topic_name in subjects[subject_name]:
        topic = subjects[subject_name][topic_name]
        base_template = 'base_marine.html' if subject_name in ['marine_species', 'marine_ecosystems', 'conservation', 'marine_policies', 'marine_science'] else 'base_general.html'
        return render_template(
            f'subjects/{subject_name}/topic_details.html',
            title=f'{topic_name} - Details',
            css_file=f'{subject_name}.css',
            js_file=f'{subject_name}.js',
            topic=topic,
            base_template=base_template
        )
    else:
        return render_template('404.html', title='404 Not Found'), 404

# Marine Education Pages
@app.route('/marine_education')
def marine_education():
    return render_template('base_marine.html', title='Marine Education', css_file='marine.css', js_file='marine.js')

# General Education Pages
@app.route('/general_education')
def general_education():
    return render_template('base_general.html', title='General Education', css_file='general.css', js_file='general.js')

# Volunteer Page
@app.route('/volunteer', methods=['GET', 'POST'])
def volunteer():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        new_volunteer = Volunteer(name=name, email=email, message=message)
        db.session.add(new_volunteer)
        db.session.commit()
        flash('Thank you for signing up to volunteer!', 'success')
        return redirect(url_for('volunteer'))
    return render_template('volunteer.html', title='Volunteer', css_file='volunteer.css', js_file='volunteer.js')

# Donate Page
@app.route('/donate')
def donate():
    return render_template('donate.html', title='Donate', css_file='donate.css', js_file='donate.js')

# Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email in users and check_password_hash(users[email], password):
            session['user'] = email
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')
    return render_template('login.html', title='Login', css_file='login.css', js_file='login.js')

# Logout Page
@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

# Contact Page
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        # Handle the contact form here, e.g., send an email
        flash('Your message has been sent. Thank you for contacting us!', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html', title='Contact Us', css_file='contact.css', js_file='contact.js')

# Privacy Page
@app.route('/privacy')
def privacy():
    return render_template('privacy.html', title='Privacy Policy', css_file='privacy.css', js_file='privacy.js')

# Terms and Conditions Page
@app.route('/terms')
def terms():
    return render_template('terms.html', title='Terms and Conditions', css_file='terms.css', js_file='terms.js')

# FAQ Page
@app.route('/faq')
def faq():
    return render_template('faq.html', title='FAQ', css_file='faq.css', js_file='faq.js')

# Subscribe Page
@app.route('/subscribe', methods=['GET', 'POST'])
def subscribe():
    if request.method == 'POST':
        email = request.form['email']
        # Handle subscription logic here, e.g., save to a database
        flash('Subscription successful! Thank you for subscribing.', 'success')
        return redirect(url_for('subscribe'))
    return render_template('subscribe.html', title='Subscribe', css_file='subscribe.css', js_file='subscribe.js')
@app.route('/apply', methods=['GET', 'POST'])
def apply():
    if request.method == 'POST':
        # Handle form submission here
        flash('Application submitted successfully!', 'success')
        # Optionally, you can clear form fields or handle other logic
        return render_template('apply.html', title='Apply', css_file='apply.css', js_file='apply.js')
    
    return render_template('apply.html', title='Apply', css_file='apply.css', js_file='apply.js')

from flask import jsonify

# Chatbot route
@app.route('/chatbot', methods=['POST'])
def chatbot():
    user_message = request.json.get('message', '').lower()

    responses = {
        'hello': 'Hello! How can I assist you today?',
        'help': 'Sure! I can help you with information about our services, volunteering, and more.',
        'volunteer': 'Thank you for your interest in volunteering! Please visit the volunteer page for more info.'
    }

    response_message = responses.get(user_message, "I'm not sure how to respond to that. Can you please rephrase?")
    return jsonify({'message': response_message})


# Error handling
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', title='404 Not Found'), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html', title='500 Internal Server Error'), 500

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

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables
    app.run(debug=True)