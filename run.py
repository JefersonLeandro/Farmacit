from flask import Flask, render_template
from app import create_app
import os

app = create_app()



with app.app_context():
    from app.extensiones import db
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
