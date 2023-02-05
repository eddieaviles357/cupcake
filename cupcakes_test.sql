-- from the terminal run:
-- psql < cupcake.sql

DROP DATABASE IF EXISTS cupcake;

CREATE DATABASE cupcake;

\c cupcake

CREATE TABLE cupcakes
(
    id SERIAL PRIMARY KEY,
    flavor TEXT NOT NULL,
    size TEXT NOT NULL,
    rating DECIMAL NOT NULL,
    image TEXT NOT NULL DEFAULT 'https://tinyurl.com/demo-cupcake'
);

INSERT INTO cupcakes ( flavor, size, rating, image )
VALUES
('chocolate', 'sm', 3.5, 'https://dinnerthendessert.com/wp-content/uploads/2021/02/Chocolate-Cupcakes-1x1-1.jpg'),
('vanilla', 'md', 2.5, 'https://encrypted-tbn3.gstatic.com/shopping?q=tbn:ANd9GcSceX1jlTG8Jz4ePeqoFkvzOg5CSj-xAX32Be-ravkgSHD37JkSCZP0b5g07MY&usqp=CAE'),
('blueberry', 'lg', 1.0, 'https://encrypted-tbn1.gstatic.com/shopping?q=tbn:ANd9GcT1UiB8LUuwJFZKR_TF7i-cJLX4_BnKsusAHAkoGLmGfQemHBs&usqp=CAE');