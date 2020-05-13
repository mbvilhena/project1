CREATE TABLE books (
    isbn VARCHAR PRIMARY KEY,
    title VARCHAR NOT NULL,
    author VARCHAR NOT NULL,
    year INTEGER NOT NULL
);

CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  username  VARCHAR UNIQUE,
  name VARCHAR NOT NULL,
  password CHAR NOT NULL,
  admin BOOLEAN
);  
