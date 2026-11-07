"""
Instâncias de extensões compartilhadas entre as camadas da aplicação.
Mantidas em um módulo separado para evitar import circular entre
app/__init__.py e os módulos de models.
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
