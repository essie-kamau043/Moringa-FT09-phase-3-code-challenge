# models/article.py
from database.connection import get_db_connection
from models.author import Author  
 
class Article:
    def __init__(self, author, magazine, title,content):
        from models.magazine import Magazine 
        self._id = None
        self._author = author
        self._magazine = magazine
        self._title = title
        self._content = content
        if isinstance(author, Author) and isinstance(magazine, Magazine):
           
            self._author_id = author.id
            self._magazine_id = magazine.id
        else:
            raise ValueError("author must be an Author instance and magazine must be a Magazine instance.")
        
        self.create_in_db()

    def create_in_db(self):
        
        if not isinstance(self._title, str) or len(self._title) < 5 or len(self._title) > 50:
            raise ValueError("Article title must be between 5 and 50 characters.")
        if not isinstance(self._content, str) or len(self._content) < 5:
            raise ValueError("Article content must be at least 5 characters.")
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO articles (author_id, magazine_id, title, content) VALUES (?, ?, ?, ?)",
            (self._author_id, self._magazine_id, self._title, self._content)
        )
        conn.commit()
        self._id = cursor.lastrowid  
        conn.close()


   
    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, new_title):
        raise ValueError("Title cannot be changed after the article is created.")

    def __repr__(self):
        return f"<Article {self._title}>"
    
    @property
    def content(self):
        return self._content

    @property
    def author(self):
         conn = get_db_connection()
         cursor = conn.cursor()
         cursor.execute(
            "SELECT authors.* FROM authors JOIN articles ON authors.id = articles.author_id WHERE articles.id = ?",
            (self._id,)
        )
         author_row = cursor.fetchone()
         conn.close()
        
         if author_row:
            return Author(id=author_row['id'], name=author_row['name'])
         return None

        
        

    @property
    def magazine(self):
         from models.magazine import Magazine 
         conn = get_db_connection()
         cursor = conn.cursor()
         cursor.execute(
            "SELECT magazines.* FROM magazines JOIN articles ON magazines.id = articles.magazine_id WHERE articles.id = ?",
            (self._id,)
        )
         magazine_row = cursor.fetchone()
         conn.close()

         if magazine_row:
            return Magazine(id=magazine_row['id'], name=magazine_row['name'], category=magazine_row['category'])
         return None
      
    

