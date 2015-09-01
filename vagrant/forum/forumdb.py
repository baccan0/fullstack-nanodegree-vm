#
# Database access functions for the web forum.
# 

import time
import psycopg2

## Database connection
DB=[]

## Get posts from database.
def GetAllPosts():
    '''Get all the posts from the database, sorted with the newest first.

    Returns:
      A list of dictionaries, where each dictionary has a 'content' key
      pointing to the post content, and 'time' key pointing to the time
      it was posted.
    '''
    conn = psycopg2.connect("dbname=forum")
    print('connect to database...')
    curs = conn.cursor()
    curs.execute("select (content,time) from posts order by time;")
    rslt = curs.fetchall()
    print('fetch all posts...')
    posts = []
    if rslt:
        for item in rslt:
            tempstr = item[0][1:-1]
            li = tempstr.split(',',1)
            posts.append({'content' : li[0][1:-1],'time' : li[1][1:-1]})
    # posts = [{'content': str(row[1]), 'time': str(row[0])} for row in DB]
    # posts.sort(key=lambda row: row['time'], reverse=True)
    conn.close()
    return posts

## Add a post to the database.
def AddPost(content):
    '''Add a new post to the database.

    Args:
      content: The text content of the new post.
    '''
    # t = time.strftime('%c', time.localtime())
    # DB.append((t, content))
    conn = psycopg2.connect('dbname=forum')
    curs = conn.cursor()
    # query = r"insert into posts (content) values ('%s ');",(content,)
    curs.execute("insert into posts (content) values (%s)", (content+' ',))
    conn.commit()
    conn.close()
