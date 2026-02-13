from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from datetime import datetime
import json
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

app = Flask(__name__)
CORS(app)

# Configuration
app.config['SECRET_KEY'] = 'your-secret-key-here-change-in-production'

# Email Configuration
# TODO: Get your API key from https://app.sendgrid.com/settings/api_keys
# TODO: Verify your sender identity at https://app.sendgrid.com/settings/sender_auth
SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY', 'YOUR_SENDGRID_API_KEY_HERE')
SENDER_EMAIL = 'your-verified-sender-email@example.com'  # Replace with your verified sender email

# Data storage (in production, use a proper database)
DATA_DIR = 'data'
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Routes for pages
@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/about')
def about():
    """About the doctor page"""
    return render_template('about.html')

@app.route('/services')
def services():
    """Services and treatments page"""
    return render_template('services.html')

@app.route('/appointment')
def appointment():
    """Appointment booking page"""
    return render_template('appointment.html')

@app.route('/contact')
def contact():
    """Contact page"""
    return render_template('contact.html')

def send_email(to_email, subject, content):
    """Helper function to send email via SendGrid"""
    if 'YOUR_SENDGRID_API_KEY' in SENDGRID_API_KEY:
        print("⚠️ SendGrid API Key not configured. Email not sent.")
        return False

    message = Mail(
        from_email=SENDER_EMAIL,
        to_emails=to_email,
        subject=subject,
        html_content=content)
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print(f"📧 Email sent! Status Code: {response.status_code}")
        return True
    except Exception as e:
        print(f"❌ Error sending email: {e}")
        return False

# API endpoints
@app.route('/api/book-appointment', methods=['POST'])
def book_appointment():
    """Handle appointment booking submissions"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'email', 'phone', 'date', 'time', 'reason']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({
                    'success': False,
                    'message': f'Missing required field: {field}'
                }), 400
        
        # Add timestamp
        data['submitted_at'] = datetime.now().isoformat()
        
        # Save to file (in production, save to database)
        appointments_file = os.path.join(DATA_DIR, 'appointments.json')
        appointments = []
        
        if os.path.exists(appointments_file):
            with open(appointments_file, 'r') as f:
                appointments = json.load(f)
        
        appointments.append(data)
        
        with open(appointments_file, 'w') as f:
            json.dump(appointments, f, indent=2)
        
        # Send email notification
        email_subject = f"Appointment Confirmation: {data['date']} at {data['time']}"
        email_content = f"""
        <h1>Appointment Confirmed</h1>
        <p>Dear {data['name']},</p>
        <p>Your appointment has been successfully booked.</p>
        <ul>
            <li><strong>Date:</strong> {data['date']}</li>
            <li><strong>Time:</strong> {data['time']}</li>
            <li><strong>Reason:</strong> {data['reason']}</li>
        </ul>
        <p>If you need to reschedule, please contact us.</p>
        <br>
        <p>Best regards,<br>Dr. Pulmonologist Team</p>
        """
        
        # Send to patient
        send_email(data['email'], email_subject, email_content)
        
        # Optional: Send notification to doctor/admin
        # send_email(SENDER_EMAIL, f"New Appointment: {data['name']}", f"New booking from {data['name']} for {data['date']}")
        
        return jsonify({
            'success': True,
            'message': 'Appointment request submitted successfully! We will contact you shortly to confirm.'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'An error occurred: {str(e)}'
        }), 500

@app.route('/api/contact', methods=['POST'])
def contact_form():
    """Handle contact form submissions"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'email', 'subject', 'message']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({
                    'success': False,
                    'message': f'Missing required field: {field}'
                }), 400
        
        # Add timestamp
        data['submitted_at'] = datetime.now().isoformat()
        
        # Save to file (in production, save to database)
        contacts_file = os.path.join(DATA_DIR, 'contacts.json')
        contacts = []
        
        if os.path.exists(contacts_file):
            with open(contacts_file, 'r') as f:
                contacts = json.load(f)
        
        contacts.append(data)
        
        with open(contacts_file, 'w') as f:
            json.dump(contacts, f, indent=2)
        
        # Here you would typically send an email notification
        
        return jsonify({
            'success': True,
            'message': 'Thank you for your message! We will get back to you soon.'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'An error occurred: {str(e)}'
        }), 500

if __name__ == '__main__':
    # Development server
    print("=" * 60)
    print("🏥 Pulmonologist Doctor Website Starting...")
    print("=" * 60)
    print("📍 Local URL: http://127.0.0.1:5000")
    print("🌐 Network URL: http://localhost:5000")
    print("=" * 60)
    print("\n✨ Press CTRL+C to stop the server\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
