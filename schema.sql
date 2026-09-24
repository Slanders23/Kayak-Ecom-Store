DROP TABLE IF EXISTS products;

CREATE TABLE products 
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product TEXT NOT NULL,
    description TEXT,
    price FLOAT NOT NULL,
    category TEXT NOT NULL,
    brand TEXT NOT NULL,
    image TEXT NOT NULL
);

DROP TABLE IF EXISTS users;
CREATE TABLE users
(
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_name TEXT Not NULL,
    password TEXT NOT NULL,
    firstName TEXT,
    lastName TEXT,
    address1 TEXT,
    address2 TEXT,
    address3 TEXT,
    postCode TEXT
);


DROP TABLE IF EXISTS orders;
CREATE TABLE orders
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    product TEXT NOT NULL,
    size TEXT NOT NULL,
    color TEXT NOT NULL,    
    price FLOAT NOT NULL,
    quantity INTEGER NOT NULL,
    Name TEXT NOT NULL,
    address TEXT NOT NULL,
    orderDate TEXT NOT NULL,
    status TEXT NOT NULL
);
DROP TABLE IF EXISTS reviews;
CREATE TABLE reviews
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id NOT NULL,
    user_id TEXT NOT NULL,
    rating FLOAT NOT NULL,
    image text,
    review TEXT NOT NULL
);

DROP TABLE IF EXISTS reviewsReply;
CREATE TABLE reviewsReply
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id NOT NULL,
    reviewId NOT NULL,
    rUser_id TEXT NOT NULL,
    rReview TEXT NOT NULL
);
DROP TABLE productsSize;


CREATE TABLE productsSize
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id TEXT NOT NULL,
    size TEXT NOT NULL,
    color TEXT NOT NULL,
    image TEXT,
    stock INTEGER NOT NULL
    );
 DELETE from productsSize WHERE stock < 0;


 DROP TABLE IF EXISTS Wish;
CREATE TABLE Wish
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    product_id TEXT NOT NULL,
    color TEXT NOT NULL,
    size TEXT NOT NULL,
    privacy TEXT NOT NULL
    );

    SELECT * 
    FROM orders as o
    JOIN products as p
    ON w.product_id = p.id 
    WHERE w.user_id = ?;