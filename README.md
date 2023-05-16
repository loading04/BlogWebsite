# Flask Web Application

This is a simple Flask web application that allows users to view blog posts, submit a contact form, and send an email with the form data.

## Prerequisites

Before running this application, make sure you have the following:

- Python 3.x installed on your machine.
- The required Python packages installed. You can install them by running `pip install -r requirements.txt`.
- An email account with a username and password. You can create a Gmail account if you don't have one.

## Installation

1. Clone this repository to your local machine or download the source code as a ZIP file.
2. Navigate to the project directory in your terminal or command prompt.
3. Install the required 


## Configuration

Before running the application, you need to configure your email account credentials. Follow these steps:

1. Open the `app.py` file in a text editor.
2. Replace `os.getenv("OWN_EMAIL")` with your email address.
3. Replace `os.getenv("OWN_PASSWORD")` with your email account password.

## Usage

To start the Flask application, run the following command in your terminal or command prompt:

```
python app.py

```
Once the application is running, open your web browser and visit `http://localhost:5000` to access the home page.

The application provides the following routes:

- `/`: Displays a list of blog posts retrieved from an external API.
- `/about`: Displays information about the website or the author.
- `/contact`: Displays a contact form for users to submit their information.
- `/post/<int:index>`: Displays a specific blog post identified by its index.

## Sending Emails

When a user submits the contact form, the application sends an email to the specified email address with the form data. To enable this functionality, make sure you have properly configured your email account credentials as mentioned in the configuration section.


