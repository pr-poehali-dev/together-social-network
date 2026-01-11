import json
import os
import re
from datetime import datetime, timedelta
import psycopg2
from psycopg2.extras import RealDictCursor
import hashlib
import secrets

def handler(event, context):
    '''API для регистрации и входа пользователей'''
    
    method = event.get('httpMethod', 'GET')
    
    if method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type, X-Auth-Token'
            },
            'body': '',
            'isBase64Encoded': False
        }
    
    dsn = os.environ.get('DATABASE_URL')
    if not dsn:
        return error_response('Database connection not configured', 500)
    
    conn = psycopg2.connect(dsn)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        body = json.loads(event.get('body', '{}'))
        action = body.get('action')
        
        if action == 'register':
            return handle_register(cursor, conn, body)
        elif action == 'login':
            return handle_login(cursor, body)
        elif action == 'check_token':
            token = event.get('headers', {}).get('X-Auth-Token')
            return handle_check_token(cursor, token)
        else:
            return error_response('Invalid action', 400)
            
    except Exception as e:
        conn.rollback()
        return error_response(str(e), 500)
    finally:
        cursor.close()
        conn.close()

def handle_register(cursor, conn, data):
    phone = data.get('phone', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '').strip()
    first_name = data.get('first_name', '').strip()
    last_name = data.get('last_name', '').strip()
    birth_date = data.get('birth_date')
    
    if not all([phone, email, password, first_name, last_name]):
        return error_response('Все поля обязательны', 400)
    
    if not re.match(r'^[\+]?[0-9]{10,15}$', phone.replace(' ', '')):
        return error_response('Неверный формат телефона', 400)
    
    if not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
        return error_response('Неверный формат email', 400)
    
    if len(password) < 6:
        return error_response('Пароль должен быть не менее 6 символов', 400)
    
    cursor.execute('SELECT id FROM users WHERE phone = %s OR email = %s', (phone, email))
    if cursor.fetchone():
        return error_response('Пользователь с таким телефоном или email уже существует', 400)
    
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    cursor.execute('''
        INSERT INTO users (phone, email, password_hash, first_name, last_name, birth_date)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id, phone, email, first_name, last_name, birth_date
    ''', (phone, email, password_hash, first_name, last_name, birth_date))
    
    user = cursor.fetchone()
    conn.commit()
    
    token = secrets.token_urlsafe(32)
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({
            'success': True,
            'user': dict(user),
            'token': token
        }),
        'isBase64Encoded': False
    }

def handle_login(cursor, data):
    login = data.get('login', '').strip()
    password = data.get('password', '').strip()
    
    if not login or not password:
        return error_response('Введите логин и пароль', 400)
    
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    cursor.execute('''
        SELECT id, phone, email, first_name, last_name, birth_date, avatar_url, media_status, bio
        FROM users 
        WHERE (phone = %s OR email = %s) AND password_hash = %s
    ''', (login, login, password_hash))
    
    user = cursor.fetchone()
    
    if not user:
        return error_response('Неверный логин или пароль', 401)
    
    token = secrets.token_urlsafe(32)
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({
            'success': True,
            'user': dict(user),
            'token': token
        }),
        'isBase64Encoded': False
    }

def handle_check_token(cursor, token):
    if not token:
        return error_response('Token not provided', 401)
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({'valid': True}),
        'isBase64Encoded': False
    }

def error_response(message, status_code):
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({'error': message}),
        'isBase64Encoded': False
    }
