E-commerce Sales Chatbot (eBay)
Overview
This project is a full-stack e-commerce sales chatbot developed as part of an internship assignment. The chatbot allows users to sign up, log in, search for products on eBay (e.g., "laptops under $1000"), purchase items, and view their orders. It is built using React for the frontend, Python Flask for the backend, SQLite for data storage, and the eBay Sandbox API for product searches.
Features

User Authentication: Sign up, log in, and sign out functionality.
Product Search: Search for products using keywords (e.g., "laptops", "mobile phones"), price filters (e.g., "laptops under $1000"), and categories (e.g., "electronics").
Purchase Items: Buy items directly from search results with a "Buy Now" button or via the "buy [item ID]" command.
Order Tracking: View past purchases (though currently facing an issue, see below).
Responsive UI: Styled with Tailwind CSS, featuring a chat interface, product cards, and an orders modal.

Tech Stack

Frontend: React, Tailwind CSS, Axios, Babel
Backend: Python, Flask, Flask-CORS, SQLite, Requests
API: eBay Sandbox Finding API (findItemsByKeywords)

Setup Instructions
Prerequisites

Python 3.x installed
Node.js is not required as the frontend uses CDN-hosted React libraries
eBay Sandbox API OAuth token (obtain from developer.ebay.com)

Installation

Clone the Repository:
git clone https://github.com/your-username/ecommerce-chatbot.git
cd ecommerce-chatbot


Install Python Dependencies:
pip install flask flask-cors requests


Configure eBay API:

Obtain an OAuth token from the eBay Developer Portal (Sandbox environment).
Open app.py and replace YOUR_EBAY_OAUTH_TOKEN with your token:EBAY_OAUTH_TOKEN = "your-oauth-token-here"





Running the Application

Start the Flask Backend:
python app.py

The server will run on http://127.0.0.1:5000.

Access the Chatbot:

Open your browser and navigate to http://127.0.0.1:5000.
Sign up or log in to start using the chatbot.



Usage

Sign Up/Login: Create a new account or log in with existing credentials.
Search for Products:
General search: "laptops", "mobile phones"
Price-based search: "laptops under $1000"
Category search: "electronics", "jewelery", "clothing"
Cheapest item: "cheapest laptops"


Purchase Items: Click "Buy Now" on a product card or type "buy [item ID]".
View Orders: Click the "View Orders" button (currently not working, see known issues).
Reset Chat/Sign Out: Use the buttons in the top-right corner to reset the conversation or log out.

Project Structure

app.py: Backend Flask server handling API endpoints, eBay API integration, and SQLite database.
index.html: Frontend React application with the chatbot UI.
chatbot.db: SQLite database (auto-generated on first run) storing users, sessions, preferences, and purchases.

Known Issues

Orders Not Showing in "View Orders" Tab: Purchases are recorded in the database, but they do not appear in the "View Orders" modal. This is likely due to a session or database retrieval issue. Debug logs show the purchases are saved, but retrieval fails.
Images Not Loading: Product images from the eBay Sandbox API are not loading due to invalid or inaccessible galleryURL values. A placeholder image ("Image Not Available") is displayed instead. This is a limitation of the Sandbox environment, and switching to the eBay Production API would resolve this.

Future Improvements

Fix the "View Orders" issue by ensuring session consistency and debugging the database retrieval process.
Switch to the eBay Production API to resolve image loading issues and provide real product data.
Deploy the app to a hosting platform like Vercel or Render for public access.
Add more advanced features like product sorting, filters, and user profile customization.

Screenshots
(You can add screenshots of your application here if desired. Use a tool like Snipping Tool or a screen recorder to capture the UI, then upload the images to GitHub and link them here.)
License
This project is licensed under the MIT License. See the LICENSE file for details.
Contact
For any questions or feedback, please reach out to [Your Name] at [your-email@example.com].
