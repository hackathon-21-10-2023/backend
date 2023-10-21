# Хакатон бэк

```bash
python manage.py create_default_superuser
```


# Документация по беку

## Доступна автодокументация
- Swagger: /api/v1/swagger/
- redoc: /api/v1/redoc/


### Авторизация
Мы используем JWT токены для авторизации.
Получить токен можно так:

```POST /auth/login```

```json
{"login": "root", "password": "12344321"}
```
Ответ:
```json
{
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZXhwIjoxNzAzMDkwMjM1fQ.0lp7gTO7U5tq-DiMxq7miz99m_uRdLQo5tEYgmqTRns",
    "name": "",
    "surname": "",
    "department": null,
    "position": "Главный долбаеб",
    "photo": "",
    "is_intern": false,
    "is_head": true,
    "is_awaiting_feedback": true,
    "feedback_viewed": null
}
```

Для аутентификации мы используем Header такого формата:
```
"Authorization": "Bearer <JWT_TOKEN>" 
```

Пример работы с токеном в AxiosJWT (взял с другого проекта)

```js
<script>
    function setCookie(name,value,days) {
        let expires = "";
        if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days*24*60*60*1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "")  + expires + "; path=/";
}
    setCookie('JWTAuthToken', "{{ token }}", 30)
 
    location.href = "/";
</script>
 
 
const JWTAuthToken = getCookie('JWTAuthToken');
 
const axiosJWT = axios.create({
    headers: {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + JWTAuthToken.toString(),
    },
});

if (JWTAuthToken) {


} else {
    console.log("Not auth!");
}
 
```

Хранить токен можешь как угодно, в кукисах, в локалсторадже, да хоть в блокнот запиши, главное передай его при 
запросе на API



### Получение подчиненных руководителя
```GET /list_slaves_of_head/<int:pk>/```

Ответ:
```json
[
  {
    "id": 3,
    "username": "kkkk@afs.com",
    "name": "Кирилл",
    "surname": "Куликов",
    "email": "kkkk@afs.com",
    "position": "Джун",
    "photo": "http://127.0.0.1:8000/static/photos/person1.jpeg",
    "is_intern": false,
    "is_head": false,
    "is_awaiting_feedback": false,
    "department": 1,
    "feedback_viewed": null
  },
  {
    "id": 4,
    "username": "mmm@aadg.com",
    "name": "Максим",
    "surname": "Окулов",
    "email": "mmm@aadg.com",
    "position": "Мидл+",
    "photo": "http://127.0.0.1:8000/static/photos/person2.jpeg",
    "is_intern": false,
    "is_head": false,
    "is_awaiting_feedback": false,
    "department": 1,
    "feedback_viewed": null
  }
]
```

