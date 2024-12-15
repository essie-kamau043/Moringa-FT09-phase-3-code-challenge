
from database.connection import get_db_connection

class Author:
    def __init__(self, id, name):
         
          self._id = id
          self._name = name

          
    def __repr__(self):
        return f'<Author {self.name}>'
    

    @property
    def id(self):
        
        return self._id

    @property
    def name(self):
       
        return self._name

       
    def create_in_db(self):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("INSERT INTO authors (name) VALUES (?)", (self._name,))
        conn.commit()

        
        self._id = cursor.lastrowid
        conn.close()


    def articles(self):
        from models.article import Article  
        from models.magazine import Magazine  
        conn = get_db_connection()
        cursor = conn.cursor()

        
        cursor.execute(
            "SELECT articles.* FROM articles JOIN authors ON articles.author_id = authors.id WHERE authors.id = ?",
            (self._id,)
        )
        articles_rows = cursor.fetchall()
        conn.close()

        
        articles = []
        for row in articles_rows:
            article = Article(
                author=self, 
                magazine=Magazine(id=row['magazine_id'], name='', category=''),  # Magazine info is retrieved separately
                title=row['title']
            )
            article._id = row['id'] 
            articles.append(article)

        return articles

    def magazines(self):
        from models.magazine import Magazine 
        conn = get_db_connection()
        cursor = conn.cursor()

        
        cursor.execute(
            "SELECT magazines.* FROM magazines "
            "JOIN articles ON magazines.id = articles.magazine_id "
            "JOIN authors ON authors.id = articles.author_id "
            "WHERE authors.id = ?",
            (self._id,)
        )
        magazines_rows = cursor.fetchall()
        conn.close()

      
        magazines = []
        for row in magazines_rows:
            magazine = Magazine(id=row['id'], name=row['name'], category=row['category'])
            magazines.append(magazine)

        return magazines

    

   
    
