Overview
This is a Flask-based RESTful API for managing a library system. It supports user authentication via JWT, allows admin operations like user creation, and enables listing available books.

GET /init - Initialize and seed the database.
POST /login - Log in and get a JWT token.

Initialize the database via GET /init.
Log in via POST /login to get a JWT token.
Use the token to access protected endpoints with the Authorization: Bearer <token> header.

Configuration store it in Config.py file