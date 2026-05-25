# Photo Album Management (Django)

This project implements a production-ready Photo Album Management system using Django, PostgreSQL and Cloudinary for media.

Key features:
- Class-Based Views for CRUD operations
- Role-Based Access Control via Django Groups (`album_admin`)
- Cloudinary-backed media storage (no local media in production)
- Deployable to Render (Procfile included)

Quick start (local development):

1. Create a virtualenv and install deps:
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

2. Copy `.env.example` to `.env` and fill in your Cloudinary credentials (Dashboard at https://console.cloudinary.com/):
```
DJANGO_SECRET_KEY=dev
DJANGO_DEBUG=True
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

3. Run migrations and create superuser:
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py init_groups
```

4. Run server:
```bash
python manage.py runserver
```

Production / Render deployment notes:
- Configure environment variables in Render: `DJANGO_SECRET_KEY`, `DATABASE_URL`, `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, `CLOUDINARY_API_SECRET`, `DJANGO_DEBUG`=False
- Add build and start commands in Render as: `pip install -r requirements.txt` and `gunicorn photoalbum.wsgi`

For full deployment steps, follow Render's Django + Postgres + Cloudinary guide and point environment variables to Render's Postgres and your Cloudinary account.
