
# Commands — Lab 01

## Start the server (Terminal A)
```
python3 curl_lab_server.py
```

## Commands (Terminal B)

### GET
```
curl http://127.0.0.1:8080/get

curl -i http://127.0.0.1:8080/get
```

### POST JSON
```
curl -i -X POST http://127.0.0.1:8080/post -H "Content-Type: application/json" -d '{"title":"Hello"}'
```

### PUT / PATCH / DELETE
```
curl -i -X PUT http://127.0.0.1:8080/put -H "Content-Type: application/json" -d '{"status":"replaced"}'

curl -i -X PATCH http://127.0.0.1:8080/patch -H "Content-Type: application/json" -d '{"status":"patched"}'

curl -i -X DELETE http://127.0.0.1:8080/delete
```

### Cookies / Redirects / Status
```
curl -i -c cookies.txt http://127.0.0.1:8080/cookie/set

curl -i -b cookies.txt http://127.0.0.1:8080/cookies

curl -i http://127.0.0.1:8080/redirect

curl -i -L http://127.0.0.1:8080/redirect

curl -i http://127.0.0.1:8080/status/404
```

### Debugging
```
curl -v http://127.0.0.1:8080/get

curl --trace-ascii - http://127.0.0.1:8080/get
```

## Collect Evidence
```
mkdir -p Evidence

curl -i http://127.0.0.1:8080/get | tee EVIDENCE/get_headers.txt
```
