"""Flask application with database support for record management."""
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///records.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@app.route("/")
def index():
    return "Hello, World!!!!!!"

@app.route("/api/records", methods=['POST'])
def add_record():
    data = request.get_json()
    
    if not data or 'title' not in data or 'content' not in data:
        return jsonify({'error': 'Missing required fields'}), 400
    
    new_record = Record(
        title=data['title'],
        content=data['content']
    )
    
    try:
        db.session.add(new_record)
        db.session.commit()
        return jsonify({
            'id': new_record.id,
            'title': new_record.title,
            'content': new_record.content,
            'created_at': new_record.created_at.isoformat()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
