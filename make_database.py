import sqlite3
conn = sqlite3.connect('ema.db')
c = conn.cursor()
c.execute('''CREATE TABLE conversations (user1 text, user2 text, topic text, isEnded text, convo_id text)''')
conn.commit()
conn.close()
print 'Database Created'