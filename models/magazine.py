# models/magazine.py
from database.connection import get_db_connection
 
from models.author import Author  

class Magazine:
    def __init__(self, id, name, category):
        self._id = id
        self._name = name
        self._category = category

    def __repr__(self):
        return f"<Magazine {self._name}>"

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        if len(new_name) < 2 or len(new_name) > 16:
            raise ValueError("Magazine name must be between 2 and 16 characters.")
        self._name = new_name

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, new_category):
        if len(new_category) < 1:
            raise ValueError("Category must be at least 1 character long.")
        self._category = new_category

    def create_in_db(self):
      
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO magazines (name, category) VALUES (?, ?)", (self._name, self._category)
        )
        conn.commit()
        self._id = cursor.lastrowid 

    def articles(self):
        from models.article import Article 
        conn = get_db_connection()
        cursor = conn.cursor()

       
        cursor.execute(
            "SELECT articles.* FROM articles JOIN magazines ON articles.magazine_id = magazines.id WHERE magazines.id = ?",
            (self._id,)
        )
        articles_rows = cursor.fetchall()
        conn.close()

       
        articles = []
        for row in articles_rows:
            article = Article(
                author=Author(id=row['author_id'], name=''),  
                magazine=self, 
                title=row['title']
            )
            article._id = row['id'] 
            articles.append(article)

        return articles

    def contributors(self):
        
        conn = get_db_connection()
        cursor = conn.cursor()

       
        cursor.execute(
            "SELECT authors.* FROM authors "
            "JOIN articles ON authors.id = articles.author_id "
            "JOIN magazines ON magazines.id = articles.magazine_id "
            "WHERE magazines.id = ?",
            (self._id,)
        )
        authors_rows = cursor.fetchall()
        conn.close()

       
        authors = []
        for row in authors_rows:
            author = Author(id=row['id'], name=row['name'])
            authors.append(author)

        return authors

    def article_titles(self):
        
        conn = get_db_connection()
        cursor = conn.cursor()

       
        cursor.execute(
            "SELECT articles.title FROM articles "
            "JOIN magazines ON articles.magazine_id = magazines.id "
            "WHERE magazines.id = ?",
            (self._id,)
        )
        articles_rows = cursor.fetchall()
        conn.close()

        
        if not articles_rows:
            return None

       
        return [row['title'] for row in articles_rows]

def contributing_authors(self):
        
        conn = get_db_connection()
        cursor = conn.cursor()

       
        cursor.execute(
            "SELECT authors.id, authors.name FROM authors "
            "JOIN articles ON authors.id = articles.author_id "
            "JOIN magazines ON magazines.id = articles.magazine_id "
            "WHERE magazines.id = ? "
            "GROUP BY authors.id "
            "HAVING COUNT(articles.id) > 2",
            (self._id,)
        )
        authors_rows = cursor.fetchall()
        conn.close()

        
        if not authors_rows:
            return None

        
        authors = [Author(id=row['id'], name=row['name']) for row in authors_rows]
        return authors