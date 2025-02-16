# Coderr Backend

The Coderr Backend provides the API for the Coderr platform. It enables the management of offers, orders, user profiles, and reviews. This project was developed using Django REST Framework (DRF).

## Features

- User registration & authentication
- Offer creation & management
- Order management with status updates
- Review function for business users
- API with full filtering, search, and sorting functionality

## Installation & Setup

### Requirements

- Python 3.10+
- Django 4.0
- PostgreSQL oder SQLite (for local testing)
- Virtual env(recommended for virtual environments)

### Clone project & install dependencies

```bash
git clone https://github.com/MaxLackmann/coderr-backend.git
cd coderr-backend
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

### Run database migrations

```bash
python manage.py migrate
```

### Create superuser (Admin)

```bash
python manage.py createsuperuser
```

### Start server

```bash
python manage.py runserver
```

## API Endpoints

### Offers

GET /offers/ - Liste aller Angebote mit Filtermöglichkeiten  
POST /offers/ - Erstellen eines neuen Angebots  
GET /offers/{id}/ - Details eines spezifischen Angebots  
PATCH /offers/{id}/ - Angebot aktualisieren  
DELETE /offers/{id}/ - Angebot löschen  

### Orders

GET /orders/ - Liste der Bestellungen des Users  
POST /orders/ - Neue Bestellung erstellen  
PATCH /orders/{id}/ - Status der Bestellung ändern (nur Business-User)  
DELETE /orders/{id}/ - Bestellung löschen (nur Admins)  

### User Profiles & Authentication

POST /login/ - Nutzer-Login  
POST /registration/ - Nutzer-Registrierung  
GET /profile/{id}/ - Nutzerprofil abrufen  
PATCH /profile/{id}/ - Profil aktualisieren  

### Reviews

GET /reviews/ - Liste aller Bewertungen  
POST /reviews/ - Bewertung erstellen  
PATCH /reviews/{id}/ - Bewertung bearbeiten  
DELETE /reviews/{id}/ - Bewertung löschen  

## Authentication

The API uses token authentication.
After logging in, the user receives a token that must be sent in the headers with requests:

```json
{
  "Authorization": "Token <dein-token>"
}
```

## Author

This project was developed by Max Lackmann.