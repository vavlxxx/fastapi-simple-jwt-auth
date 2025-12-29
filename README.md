### Шаблон для простого FastAPI приложения с JWT авторизацией

#### Генерирование ключей для JWT токенов

Ключи хранятся в директории `creds/`. Необходимо перейти в неё и воспользоваться командами ниже.

```bash
openssl genrsa -out jwt-private.pem 2048
openssl rsa -in jwt-private.pem -outform PEM -pubout -out jwt-public.pem
```
