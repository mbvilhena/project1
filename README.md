# CS50'W Project 1

## Books

**Book Search Tool**

## Structure

- **application.py** base python application (flask run)
- **models.py** class and table definitions (to import to application.py)
- **create.py** creates all tables in Database
- **import.py** imports all data from **books.csv** to books table (defined in models.py and created in create.py)
- **templates folder** folder with html pages
    - **book.html** book page structure for each book in the list (with review system)
    - **booklist.html** search results
    - **books.html** list of all books with links for each book page
    - **index.html** index page with link to books.html
    - **layout.html** base layout for all html pages
    - **login.html** login page / redirect to index
    - **logout.html** logout page / redirect to login
    - **register.html** register page / redirect to login
    - **search.html** search bar / redirect to booklist (search results)
- **static folder** style file and images

## Built With
Python/Flask/SQLAlchemy/HTML/CSS/Bootstrap <br>
**Database** "postgres://qqnufqcpwpshpw:c60e8f61830b48d35b02f34333507c90c005165dfb4e3fe8a81809177acae8af@ec2-79-125-26-232.eu-west-1.compute.amazonaws.com:5432/dc2tgav9tm02ds"

## Author
Maria Beatriz de Vilhena
