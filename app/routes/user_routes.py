from flask import Blueprint, request, jsonify

user_bp = Blueprint('users', __name__)

# --- GLOBAL DATABASE (The Fix) ---
# We define this OUTSIDE the functions so it remembers data
# while the application is running.
users_db = {
    1: {'id': 1, 'name': 'John Doe', 'email': 'john@example.com'},
    2: {'id': 2, 'name': 'Jane Smith', 'email': 'jane@example.com'}
}
# ---------------------------------

@user_bp.route('/', methods=['GET'])
def get_users():
    # Return all users from our global database
    return jsonify(list(users_db.values()))

@user_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    # Check our global database
    if user_id in users_db:
        return jsonify(users_db[user_id])
    return jsonify({'error': 'User not found'}), 404

@user_bp.route('/', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or 'name' not in data or 'email' not in data:
        return jsonify({'error': 'Name and email are required'}), 400
    
    # Calculate new ID: Find the highest ID and add 1
    new_id = max(users_db.keys()) + 1 if users_db else 1
    
    new_user = {
        'id': new_id,
        'name': data['name'],
        'email': data['email']
    }
    
    # SAVE the new user to the global database
    users_db[new_id] = new_user
    
    return jsonify(new_user), 201
