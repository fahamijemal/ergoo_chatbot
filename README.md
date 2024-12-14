Ergoo_Chatbot
Ergoo Chatbot is my first Django project, built to allow users to interact with a chatbot. It includes seamless authentication through Google OAuth2 using Django-Allauth, offering an easy login/signup experience. This project showcases my journey in web development, specifically in backend with Django.

Key Features
Google Login/Signup: Allows users to log in or create an account using their Google credentials, powered by Google OAuth2.
Simple Django Backend: The backend is built with Django to manage user sessions and handle chatbot interactions.
Frontend Templates: Includes easy-to-use templates to interact with the chatbot, designed for a smooth user experience.
“Battery Included”: Everything you need to get started with Django is included, from authentication to app structure.
Installation
Prerequisites
Python 3.12 or higher
Django 4.0 or higher
Pip (Python's package installer)
Steps to Get Started
Clone the repository:

bash
Copy code
git clone https://github.com/fahamijemal/ergoo_chatbot.git
Navigate to the project directory:

bash
Copy code
cd ergoo_chatbot
Set up a virtual environment (optional but recommended):

bash
Copy code
python -m venv venv
Activate the virtual environment:

On Windows:

bash
Copy code
venv\Scripts\activate
On MacOS/Linux:

bash
Copy code
source venv/bin/activate
Install the dependencies:

bash
Copy code
pip install -r requirements.txt
Set up environment variables:

Create a .env file in the root directory and add your Google OAuth2 credentials:

makefile
Copy code
GOOGLE_CLIENT_ID=your-client-id
GOOGLE_SECRET_KEY=your-secret-key
Run migrations:

bash
Copy code
python manage.py migrate
Run the development server:

bash
Copy code
python manage.py runserver
Your app should now be running at http://127.0.0.1:8000/.

Usage
Visit the app in your browser.
You can log in using your Google account or create a new account.
Start interacting with the chatbot!
Future Improvements
Enhance the backend to support more complex chatbot functionalities.
Implement user profiles and data storage.
Explore additional authentication methods and integrate other APIs.
Contributing
Feel free to fork the repository, submit pull requests, or open issues. Contributions are welcome!
