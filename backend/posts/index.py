import json
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime

def handler(event, context):
    '''API для работы с постами: создание, просмотр, лайки, комментарии, репосты'''
    
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
            return get_posts(cursor, event)
        elif method == 'POST':
            body = json.loads(event.get('body', '{}'))
            action = body.get('action')
            
            if action == 'create':
                return create_post(cursor, conn, body)
            elif action == 'like':
                return toggle_like(cursor, conn, body)
            elif action == 'comment':
                return add_comment(cursor, conn, body)
            elif action == 'repost':
                return repost(cursor, conn, body)
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

def get_posts(cursor, event):
    params = event.get('queryStringParameters', {}) or {}
    user_id = params.get('user_id')
    limit = int(params.get('limit', 20))
    offset = int(params.get('offset', 0))
    
    if user_id:
        query = '''
            SELECT p.*, u.first_name, u.last_name, u.avatar_url,
                   (SELECT COUNT(*) FROM likes WHERE post_id = p.id) as likes_count
            FROM posts p
            JOIN users u ON p.user_id = u.id
            WHERE p.user_id = %s
            ORDER BY p.created_at DESC
            LIMIT %s OFFSET %s
        '''
        cursor.execute(query, (user_id, limit, offset))
    else:
        query = '''
            SELECT p.*, u.first_name, u.last_name, u.avatar_url,
                   (SELECT COUNT(*) FROM likes WHERE post_id = p.id) as likes_count
            FROM posts p
            JOIN users u ON p.user_id = u.id
            ORDER BY p.created_at DESC
            LIMIT %s OFFSET %s
        '''
        cursor.execute(query, (limit, offset))
    
    posts = cursor.fetchall()
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({
            'posts': [dict(post) for post in posts]
        }, default=str),
        'isBase64Encoded': False
    }

def create_post(cursor, conn, data):
    user_id = data.get('user_id')
    content = data.get('content', '').strip()
    post_type = data.get('post_type', 'text')
    media_urls = data.get('media_urls', [])
    
    if not user_id or not content:
        return error_response('user_id и content обязательны', 400)
    
    cursor.execute('''
        INSERT INTO posts (user_id, content, post_type, media_urls)
        VALUES (%s, %s, %s, %s)
        RETURNING id, user_id, content, post_type, media_urls, created_at
    ''', (user_id, content, post_type, media_urls))
    
    post = cursor.fetchone()
    conn.commit()
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({
            'success': True,
            'post': dict(post)
        }, default=str),
        'isBase64Encoded': False
    }

def toggle_like(cursor, conn, data):
    user_id = data.get('user_id')
    post_id = data.get('post_id')
    
    if not user_id or not post_id:
        return error_response('user_id и post_id обязательны', 400)
    
    cursor.execute('SELECT id FROM likes WHERE user_id = %s AND post_id = %s', (user_id, post_id))
    existing = cursor.fetchone()
    
    if existing:
        cursor.execute('DELETE FROM likes WHERE user_id = %s AND post_id = %s', (user_id, post_id))
        cursor.execute('UPDATE posts SET likes_count = likes_count - 1 WHERE id = %s', (post_id,))
        action = 'unliked'
    else:
        cursor.execute('INSERT INTO likes (user_id, post_id) VALUES (%s, %s)', (user_id, post_id))
        cursor.execute('UPDATE posts SET likes_count = likes_count + 1 WHERE id = %s', (post_id,))
        action = 'liked'
    
    conn.commit()
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({
            'success': True,
            'action': action
        }),
        'isBase64Encoded': False
    }

def add_comment(cursor, conn, data):
    user_id = data.get('user_id')
    post_id = data.get('post_id')
    content = data.get('content', '').strip()
    
    if not all([user_id, post_id, content]):
        return error_response('Все поля обязательны', 400)
    
    cursor.execute('UPDATE posts SET comments_count = comments_count + 1 WHERE id = %s', (post_id,))
    conn.commit()
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({
            'success': True,
            'message': 'Комментарий добавлен'
        }),
        'isBase64Encoded': False
    }

def repost(cursor, conn, data):
    user_id = data.get('user_id')
    original_post_id = data.get('post_id')
    
    if not user_id or not original_post_id:
        return error_response('user_id и post_id обязательны', 400)
    
    cursor.execute('SELECT content, post_type, media_urls FROM posts WHERE id = %s', (original_post_id,))
    original = cursor.fetchone()
    
    if not original:
        return error_response('Пост не найден', 404)
    
    cursor.execute('''
        INSERT INTO posts (user_id, content, post_type, media_urls)
        VALUES (%s, %s, %s, %s)
        RETURNING id
    ''', (user_id, original['content'], original['post_type'], original['media_urls']))
    
    conn.commit()
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({
            'success': True,
            'message': 'Пост репостнут'
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
