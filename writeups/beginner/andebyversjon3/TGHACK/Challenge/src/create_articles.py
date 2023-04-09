import sqlite3

conn = sqlite3.connect("articles.db")
c = conn.cursor()

c.execute("""CREATE TABLE articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    date_published TEXT NOT NULL
);""")

articles = [
    "INSERT INTO articles (title, content, date_published) VALUES ('Fugleinfluensa sesongen', 'Fugleinfluensa sesongen er her! På tide å innføre 2 meters regelen og antibac. Kan også være lurt å vaksinere seg og sine andunger. ...', '24.03.23')",
    "INSERT INTO articles (title, content, date_published) VALUES ('Fugletrekk: hvor og når?','På tide å fly til varmere strøk. Men hvor skal turen gå denne gang? Har hørt mye bra om frøene i italia. ...','01.08.22')",
    "INSERT INTO articles (title, content, date_published) VALUES ('Trekkfugler vender ikke tilbake','Etter nyheter om snø mmidt i påska er trekkfuglene fristet til å ikke returnere til Andeby. ...','05.04.23')",
    "INSERT INTO articles (title, content, date_published) VALUES ('Brød: en ands mening','Det blir mye brød om dagen når man kruser rundt i en dam. Brød inneholder ikke næringen vi trenger. ...','30.03.23')",
    "INSERT INTO articles (title, content, date_published) VALUES ('Vann kvalitet i Andeby','Vi må utsette årets vannkvalitetssjekk da alle vann i Andeby er isbelagt. ...','01.01.23')",
    "INSERT INTO articles (title, content, date_published) VALUES ('Den beste andedansen','Enda ikke fått teket på dansingen? Her er 10 tips til heftige danse moves som enhver and kommer til å sette pris på. ...','06.02.23')",
    "INSERT INTO articles (title, content, date_published) VALUES ('Vannplanter','Som ender spiser vi mye vannplanter. Dette er en guide på hvilke planter som er digge og hvilke som er giftige. ...','23.03.23')",
    "INSERT INTO articles (title, content, date_published) VALUES ('Super secret burried so deep in the database, that you will never find it!','TG23{so_many_ducking_articles}','176.167')"
]

for article in articles:
    c.execute(article)

conn.commit()