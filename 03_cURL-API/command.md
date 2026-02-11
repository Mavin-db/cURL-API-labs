
# Commands — Lab 03

## Start server
```
python3 mini_api_auth.py
```

Token default: `password123`

## Public read
```
curl -i http://127.0.0.1:8080/api/posts
```

## Write without token (401)
```
curl -i -X POST http://127.0.0.1:8080/api/posts -H "Content-Type: application/json" -d '{"title":"should fail"}'
```

## Write with token (201)
```
curl -i -X POST http://127.0.0.1:8080/api/posts -H "Authorization: Bearer password123" -H "Content-Type: application/json" -d '{"title":"with token","body":"ok"}'
```

## Patch / Delete
```
curl -i -X PATCH http://127.0.0.1:8080/api/posts/1 -H "Authorization: Bearer password123" -H "Content-Type: application/json" -d '{"title":"patched"}'

curl -i -X DELETE http://127.0.0.1:8080/api/posts/1 -H "Authorization: Bearer password123"
```
