# Coderr Backend

Das Coderr Backend stellt die API für die Coderr-Plattform bereit. Es ermöglicht die Verwaltung von Angeboten, Bestellungen, Benutzerprofilen und Bewertungen. Dieses Projekt wurde mit Django REST Framework (DRF) entwickelt.

## Features

- Nutzerregistrierung & Authentifizierung
- Angebotserstellung & Verwaltung
- Bestellmanagement mit Status-Updates
- Bewertungsfunktion für Business-User
- API mit vollständiger Filter-, Such- und Sortierfunktionalität

## Installation & Setup

### Voraussetzungen

- Python 3.10+
- Django 4.0
- PostgreSQL oder SQLite (für lokale Tests)
- Virtual env(empfohlen für virtuelle Umgebungen)

### Projekt klonen & Abhängigkeiten installieren

```bash
git clone https://github.com/MaxLackmann/coderr-backend.git
cd coderr-backend
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

### Datenbankmigrationen ausführen

```bash
python manage.py migrate
```

### Superuser (Admin) erstellen

```bash
python manage.py createsuperuser
```

### Server starten

```bash
python manage.py runserver
```

## API Endpoints

### Angebote

GET /offers/ - Liste aller Angebote mit Filtermöglichkeiten  
POST /offers/ - Erstellen eines neuen Angebots  
GET /offers/{id}/ - Details eines spezifischen Angebots  
PATCH /offers/{id}/ - Angebot aktualisieren  
DELETE /offers/{id}/ - Angebot löschen  

### Bestellungen

GET /orders/ - Liste der Bestellungen des Users  
POST /orders/ - Neue Bestellung erstellen  
PATCH /orders/{id}/ - Status der Bestellung ändern (nur Business-User)  
DELETE /orders/{id}/ - Bestellung löschen (nur Admins)  

### Benutzerprofile & Authentifizierung

POST /login/ - Nutzer-Login  
POST /registration/ - Nutzer-Registrierung  
GET /profile/{id}/ - Nutzerprofil abrufen  
PATCH /profile/{id}/ - Profil aktualisieren  

### Bewertungen

GET /reviews/ - Liste aller Bewertungen  
POST /reviews/ - Bewertung erstellen  
PATCH /reviews/{id}/ - Bewertung bearbeiten  
DELETE /reviews/{id}/ - Bewertung löschen  

## Authentifizierung

Die API verwendet Token-Authentifizierung.  
Nach dem Login erhält der Nutzer einen Token, der in den Headern bei Anfragen mitgesendet werden muss:

```json
{
  "Authorization": "Token <dein-token>"
}
```

## Lizenz & Autor

Dieses Projekt wurde von Max Lackmann entwickelt.  
Lizenz: MIT License (falls nicht anders gewünscht).
