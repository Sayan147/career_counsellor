import csv
import os
import json
from datetime import datetime
import uuid
from typing import List, Dict, Optional
from ..models.user import UserProfile

# Define the paths for CSV files
USERS_CSV = "data/users.csv"
CHATS_CSV = "data/chats.csv"
PROFILES_CSV = "data/profiles.csv"

# Ensure data directory exists
os.makedirs("data", exist_ok=True)

# Initialize CSV files if they don't exist
def init_csv_files():
    if not os.path.exists(USERS_CSV):
        with open(USERS_CSV, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'email', 'created_at'])
    
    if not os.path.exists(CHATS_CSV):
        with open(CHATS_CSV, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'user_id', 'message', 'response', 'created_at'])

    if not os.path.exists(PROFILES_CSV):
        with open(PROFILES_CSV, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['user_id', 'profile_data'])

def get_user_by_email(email: str) -> Optional[Dict]:
    user = None
    with open(USERS_CSV, 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['email'] == email:
                user = row
                break
    
    if user:
        # Get profile if exists
        profile = get_user_profile(user['id'])
        if profile:
            user['profile'] = profile
    
    return user

def create_user(email: str) -> Dict:
    user = {
        'id': str(uuid.uuid4()),
        'email': email,
        'created_at': datetime.utcnow().isoformat(),
        'profile': None
    }
    
    with open(USERS_CSV, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['id', 'email', 'created_at'])
        writer.writerow({
            'id': user['id'],
            'email': user['email'],
            'created_at': user['created_at']
        })
    
    return user

def get_user_profile(user_id: str) -> Optional[Dict]:
    if not os.path.exists(PROFILES_CSV):
        return None
        
    with open(PROFILES_CSV, 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['user_id'] == user_id:
                return json.loads(row['profile_data'])
    return None

def update_user_profile(user_id: str, profile: UserProfile) -> bool:
    profiles = []
    profile_exists = False
    
    # Read existing profiles
    if os.path.exists(PROFILES_CSV):
        with open(PROFILES_CSV, 'r', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['user_id'] == user_id:
                    profiles.append({
                        'user_id': user_id,
                        'profile_data': json.dumps(profile.dict())
                    })
                    profile_exists = True
                else:
                    profiles.append(row)
    
    # Add new profile if it doesn't exist
    if not profile_exists:
        profiles.append({
            'user_id': user_id,
            'profile_data': json.dumps(profile.dict())
        })
    
    # Write all profiles back
    with open(PROFILES_CSV, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['user_id', 'profile_data'])
        writer.writeheader()
        writer.writerows(profiles)
    
    return True

# Chat operations
def create_chat(user_id: str, message: str, response: str) -> Dict:
    chat = {
        'id': str(uuid.uuid4()),
        'user_id': user_id,
        'message': message,
        'response': response,
        'created_at': datetime.utcnow().isoformat()
    }
    
    with open(CHATS_CSV, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['id', 'user_id', 'message', 'response', 'created_at'])
        writer.writerow(chat)
    
    return chat

def get_user_chats(user_id: str) -> List[Dict]:
    chats = []
    with open(CHATS_CSV, 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['user_id'] == user_id:
                chats.append(row)
    return chats

# Initialize CSV files on module import
init_csv_files() 