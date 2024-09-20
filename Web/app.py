from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
Bootstrap(app)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key

# Dummy user data for example purposes
users = {
    'admin@example.com': generate_password_hash('password')  # Example hash; replace with real hashed passwords
}

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
@app.route('/volunteer')
def volunteer():
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

# Error handling
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', title='404 Not Found'), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html', title='500 Internal Server Error'), 500

if __name__ == '__main__':
    app.run(debug=True)
