import json
import os
import psycopg2
from psycopg2.extras import RealDictCursor

def handler(event, context):
    '''API для управления друзьями: поиск, добавление, удаление, запросы'''
    
    method = event.get('httpMethod', 'GET')
    
    if method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type, X-Auth-Token'
            },
            'body': '',
            'isBase64Encoded': False
        }
    
    dsn = os.environ.get('DATABASE_URL')
    if not dsn:
        return error_response('Database not configured', 500)
    
    conn = psycopg2.connect(dsn)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        if method == 'GET':
            return get_friends_or_search(cursor, event)
        elif method == 'POST':
            body = json.loads(event.get('body', '{}'))
            action = body.get('action')
            
            if action == 'add':
                return add_friend(cursor, conn, body)
            elif action == 'accept':
                return accept_friend(cursor, conn, body)
            elif action == 'reject':
                return reject_friend(cursor, conn, body)
            elif action == 'remove':
                return remove_friend(cursor, conn, body)
            else:
                return error_response('Invalid action', 400)
        else:
            return error_response('Method not allowed', 405)
            
    except Exception as e:
        conn.rollback()
        return error_response(str(e), 500)
    finally:
        cursor.close()
        conn.close()

def get_friends_or_search(cursor, event):
    params = event.get('queryStringParameters', {}) or {}
    user_id = params.get('user_id')
    search = params.get('search', '').strip()
    
    if search:
        query = '''
            SELECT id, phone, email, first_name, last_name, avatar_url, online
            FROM users
            WHERE (first_name ILIKE %s OR last_name ILIKE %s OR phone LIKE %s)
            AND id != %s
            LIMIT 20
        '''
        search_pattern = f'%{search}%'
        cursor.execute(query, (search_pattern, search_pattern, search_pattern, user_id or 0))
        users = cursor.fetchall()
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'users': [dict(u) for u in users]
            }, default=str),
            'isBase64Encoded': False
        }
    
    if not user_id:
        return error_response('user_id required', 400)
    
    query = '''
        SELECT u.id, u.first_name, u.last_name, u.avatar_url, u.online, f.status
        FROM friends f
        JOIN users u ON (f.friend_id = u.id OR f.user_id = u.id)
        WHERE (f.user_id = %s OR f.friend_id = %s) AND u.id != %s
        AND f.status = 'accepted'
    '''
    cursor.execute(query, (user_id, user_id, user_id))
    friends = cursor.fetchall()
    
    query_requests = '''
        SELECT u.id, u.first_name, u.last_name, u.avatar_url, f.created_at
        FROM friends f
        JOIN users u ON f.user_id = u.id
        WHERE f.friend_id = %s AND f.status = 'pending'
    '''
    cursor.execute(query_requests, (user_id,))
    requests = cursor.fetchall()
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({
            'friends': [dict(f) for f in friends],
            'requests': [dict(r) for r in requests]
        }, default=str),
        'isBase64Encoded': False
    }

def add_friend(cursor, conn, data):
    user_id = data.get('user_id')
    friend_id = data.get('friend_id')
    
    if not user_id or not friend_id:
        return error_response('user_id и friend_id обязательны', 400)
    
    cursor.execute('''
        SELECT id FROM friends 
        WHERE (user_id = %s AND friend_id = %s) OR (user_id = %s AND friend_id = %s)
    ''', (user_id, friend_id, friend_id, user_id))
    
    if cursor.fetchone():
        return error_response('Заявка уже существует', 400)
    
    cursor.execute('''
        INSERT INTO friends (user_id, friend_id, status)
        VALUES (%s, %s, 'pending')
    ''', (user_id, friend_id))
    
    conn.commit()
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({
            'success': True,
            'message': 'Заявка в друзья отправлена'
        }),
        'isBase64Encoded': False
    }

def accept_friend(cursor, conn, data):
    user_id = data.get('user_id')
    friend_id = data.get('friend_id')
    
    if not user_id or not friend_id:
        return error_response('user_id и friend_id обязательны', 400)
    
    cursor.execute('''
        UPDATE friends 
        SET status = 'accepted'
        WHERE user_id = %s AND friend_id = %s AND status = 'pending'
    ''', (friend_id, user_id))
    
    conn.commit()
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({
            'success': True,
            'message': 'Заявка принята'
        }),
        'isBase64Encoded': False
    }

def reject_friend(cursor, conn, data):
    user_id = data.get('user_id')
    friend_id = data.get('friend_id')
    
    if not user_id or not friend_id:
        return error_response('user_id и friend_id обязательны', 400)
    
    cursor.execute('''
        DELETE FROM friends 
        WHERE user_id = %s AND friend_id = %s AND status = 'pending'
    ''', (friend_id, user_id))
    
    conn.commit()
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({
            'success': True,
            'message': 'Заявка отклонена'
        }),
        'isBase64Encoded': False
    }

def remove_friend(cursor, conn, data):
    user_id = data.get('user_id')
    friend_id = data.get('friend_id')
    
    if not user_id or not friend_id:
        return error_response('user_id и friend_id обязательны', 400)
    
    cursor.execute('''
        DELETE FROM friends 
        WHERE (user_id = %s AND friend_id = %s) OR (user_id = %s AND friend_id = %s)
    ''', (user_id, friend_id, friend_id, user_id))
    
    conn.commit()
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({
            'success': True,
            'message': 'Друг удален'
        }),
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
