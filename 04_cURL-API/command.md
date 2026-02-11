
# Commands — Lab 04 (Baseline Evidence)

## Start server (Terminal A)
```
python3 grc_lab1_baseline.py
```

## Evidence folder
```
mkdir -p EVIDENCE
```

## 1) Unauthenticated access -> 401
```
curl -i http://127.0.0.1:8080/me | tee EVIDENCE/01_me_unauth_401.txt
```

## 2) Register user
```
curl -i -X POST http://127.0.0.1:8080/register -H "Content-Type: application/json" -d '{"username":"brad","password":"pass123"}' | tee EVIDENCE/02_register_brad_201.txt
```

## 3) Login (save cookie)
```
curl -i -c cookies_brad.txt -X POST http://127.0.0.1:8080/login -H "Content-Type: application/json" -d '{"username":"brad","password":"pass123"}' | tee EVIDENCE/03_login_brad_200_setcookie.txt
```

## 4) Authenticated /me -> 200
```
curl -i -b cookies_brad.txt http://127.0.0.1:8080/me | tee EVIDENCE/04_me_auth_200.txt
```

## 5) Admin blocked -> 403
```
curl -i -b cookies_brad.txt http://127.0.0.1:8080/admin | tee EVIDENCE/05_admin_denied_403.txt
```

## 6) Create post -> 201
```
curl -i -b cookies_brad.txt -X POST http://127.0.0.1:8080/api/posts -H "Content-Type: application/json" -d '{"title":"First post","body":"Baseline evidence"}' | tee EVIDENCE/06_create_post_201.txt
```

## 7) List posts -> 200 (should only show your posts)
```
curl -i -b cookies_brad.txt http://127.0.0.1:8080/api/posts | tee EVIDENCE/07_list_posts_200.txt
```

## Optional: prove ownership enforcement
```
curl -i -X POST http://127.0.0.1:8080/register -H "Content-Type: application/json" -d '{"username":"bob","password":"pass123"}' | tee EVIDENCE/08_register_bob_201.txt

curl -i -c cookies_bob.txt -X POST http://127.0.0.1:8080/login -H "Content-Type: application/json" -d '{"username":"bob","password":"pass123"}' | tee EVIDENCE/09_login_bob_200_setcookie.txt

curl -i -b cookies_bob.txt http://127.0.0.1:8080/api/posts/1 | tee EVIDENCE/10_bob_get_brad_post_forbidden_403.txt

# Create Post

curl -i -b cookies_bob.txt -X POST http://127.0.0.1:8080/api/posts -H "Content-Type: application/json" -d '{"title":"Bob's Post","body":"Bob puts data here."}' | tee EVIDENCE/11_create_post_bob_201.txt

# list posts

curl -i -b cookies_bob.txt http://127.0.0.1:8080/api/posts/ | tee EVIDENCE/12_view_posts.txt

```
