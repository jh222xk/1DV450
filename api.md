API calls
=========

# Positions

## Default
http://localhost:8000/api/v1/positions/?key=YOUR_KEY

## A single instance
http://localhost:8000/api/v1/positions/1/?key=YOUR_KEY

## Ordering ASC
http://localhost:8000/api/v1/positions/?key=YOUR_KEY&ordering=created_at

## Ordering DESC
http://localhost:8000/api/v1/positions/?key=YOUR_KEY&ordering=-created_at

## Ordering by name
http://localhost:8000/api/v1/positions/?key=YOUR_KEY&ordering=name

## Ordering by address

http://localhost:8000/api/v1/positions/?key=YOUR_KEY&ordering=address

## Pages

http://localhost:8000/api/v1/positions/?key=YOUR_KEY&page=2

## Page size (Max 100)
http://localhost:8000/api/v1/positions/?key=YOUR_KEY&page_size=100

# Tags

## Default
http://localhost:8000/api/v1/tags/?key=YOUR_KEY

## A single instance
http://localhost:8000/api/v1/tags/1/?key=YOUR_KEY

## Ordering ASC
http://localhost:8000/api/v1/tags/?key=YOUR_KEY&ordering=created_at

## Ordering DESC
http://localhost:8000/api/v1/tags/?key=YOUR_KEY&ordering=-created_at

## Ordering by name
http://localhost:8000/api/v1/tags/?key=YOUR_KEY&ordering=name

## Ordering by created_at

http://localhost:8000/api/v1/tags/?key=YOUR_KEY&ordering=created_at

## Pages

http://localhost:8000/api/v1/tags/?key=YOUR_KEY&page=2

## Page size (Max 100)
http://localhost:8000/api/v1/tags/?key=YOUR_KEY&page_size=100

# Coffeehouses

# Smart query
http://localhost:8000/api/v1/coffeehouses/?key=asd&longitude=56.6604584&latitude=16.3484457

Will search for coffeehouses within a radius at the location (lat, lng) and find the best match (rating, location)

http://localhost:8000/api/v1/coffeehouses/?key=asd&longitude=56.6604584&latitude=16.3484457&query=espresso

Will search for coffeehouses within a radius at the location (lat, lng) and find the best match
(rating, location, query("espresso"))

http://localhost:8000/api/v1/coffeehouses/?key=asd&query=espresso

Will find all the coffeehouses that has some association with the term "espresso"