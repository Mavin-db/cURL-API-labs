
# Commands — Lab 02

## Start server
```
python3 mini_api.py
```

## Create / list / read
```
curl -i -X POST http://127.0.0.1:8080/api/posts -H "Content-Type: application/json" -d '{"title":"Hello","body":"Created from curl"}'

curl -i http://127.0.0.1:8080/api/posts

curl -i http://127.0.0.1:8080/api/posts/1
```

## Update / replace / delete
```bash
curl -i -X PATCH http://127.0.0.1:8080/api/posts/1 -H "Content-Type: application/json" -d '{"title":"Updated"}'

curl -i -X PUT http://127.0.0.1:8080/api/posts/1 -H "Content-Type: application/json" -d '{"title":"Replaced","body":"New body"}'

curl -i -X DELETE http://127.0.0.1:8080/api/posts/1
```

## Evidence tip
``` 
mkdir -p Evidence

curl -i http://127.0.0.1:8080/api/posts | tee EVIDENCE/list_posts.txt
```
