# Хакатон бэк

```bash
python manage.py create_default_superuser
```


# Документация по беку v1

## Доступна автодокументация
- Swagger: /api/v1/swagger/
- redoc: /api/v1/redoc/


### аутентификация
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
    "position": "Главный инженер по разработке",
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
```GET /list_slaves_of_head/{int:pk}/```

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

### Запросить обратную связь
```POST /ask_review/{int:pk}/```

Возвращает список пользователей, которые должны будут оценить `<int:pk>` сотрудника:
```json
[
    {
        "id": 3,
        "username": "kkkk@afs.com",
        "name": "Кирилл",
        "surname": "Куликов",
        "email": "kkkk@afs.com",
        "position": "Джун",
        "photo": "/static/photos/person1.jpeg",
        "is_intern": true,
        "is_head": false,
        "is_awaiting_feedback": true,
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
        "photo": "/static/photos/person2.jpeg",
        "is_intern": false,
        "is_head": false,
        "is_awaiting_feedback": false,
        "department": 1,
        "feedback_viewed": null
    }
]
```


### Информация о пользователе (аутентификация по JWT)
```GET /get_me/```

Ответ:
```json
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
```

### Список пользователей, которых нужно оценить (аутентификация по JWT) 
```GET /list_need_to_review_users/```

Ответ:
```json
[
  {
    "id": 6,
    "username": "evewe@gedsg.ru",
    "name": "Евгений",
    "surname": "Таримов",
    "email": "evewe@gedsg.ru",
    "position": "Лид",
    "photo": "http://127.0.0.1:8000/static/photos/person4.jpeg",
    "is_intern": false,
    "is_head": true,
    "is_awaiting_feedback": true,
    "department": 1,
    "feedback_viewed": null
  }
]
```
### Список метрик 
```GET /metric/list/```

Ответ:
```json
[
  {
    "title": "участие в рабочих задачах",
    "description": "Оцените качество выполнения сотрудником поставленных целей и задач",
    "id": 1
  },
  {
    "title": "участие в корпоративной жизни компании",
    "description": "Оцените вклад сотрудника в корпоративные ценности компании",
    "id": 2
  }
]
```

### Вывод агрегированного отзыва c айди `pk` об одном пользователе (аутентификация по JWT)

```GET /review/<int:pk>/```

Ответ:
```json
{
  "id": 1,
  "to_user": {
    "id": 2,
    "username": "kkkkk@kkkk.com",
    "name": "Kirill",
    "surname": "Kulikov",
    "email": "kkkkk@kkkk.com",
    "position": "Python",
    "photo": "http://127.0.0.1:8000/static/photos/person4_DdBaha4.jpeg",
    "is_intern": false,
    "is_head": false,
    "is_awaiting_feedback": true,
    "department": null,
    "feedback_viewed": null
  },
  "feedbacks": [
    {
      "id": 1,
      "to_user": {
        "id": 2,
        "username": "kkkkk@kkkk.com",
        "name": "Kirill",
        "surname": "Kulikov",
        "email": "kkkkk@kkkk.com",
        "position": "Python",
        "photo": "http://127.0.0.1:8000/static/photos/person4_DdBaha4.jpeg",
        "is_intern": false,
        "is_head": false,
        "is_awaiting_feedback": true,
        "department": null,
        "feedback_viewed": null
      }
    },
    {
      "id": 2,
      "to_user": {
        "id": 2,
        "username": "kkkkk@kkkk.com",
        "name": "Kirill",
        "surname": "Kulikov",
        "email": "kkkkk@kkkk.com",
        "position": "Python",
        "photo": "http://127.0.0.1:8000/static/photos/person4_DdBaha4.jpeg",
        "is_intern": false,
        "is_head": false,
        "is_awaiting_feedback": true,
        "department": null,
        "feedback_viewed": null
      }
    }
  ],
  "created_at": "2023-10-22T12:26:05.976168Z",
  "score": 2,
  "score_as_human": "плохо",
  "text": null,
  "score_tone": null,
  "is_reviewed_by_gpt": false
}
```

### Получение списка отзывов, которые принадлежат `employee_id`
```GET /review/list/for/<int:employee_id>/```

```json
[
  {
    "id": 1,
    "to_user": {
      "id": 2,
      "username": "kkkkk@kkkk.com",
      "name": "Kirill",
      "surname": "Kulikov",
      "email": "kkkkk@kkkk.com",
      "position": "Python",
      "photo": "http://127.0.0.1:8000/static/photos/person4_DdBaha4.jpeg",
      "is_intern": false,
      "is_head": false,
      "is_awaiting_feedback": true,
      "department": null,
      "feedback_viewed": null
    },
    "created_at": "2023-10-22T12:26:05.976168Z"
  }
]
```

### Создать отзыв (аутентификация по JWT)

```POST /feedback_create/```

Запрос:
```json
{
  "feedback_items": [
    {
      "text": "bad",
      "score": 2,
      "metric_id": 2
    },
    {
      "text": "cool",
      "score": 5,
      "metric_id": 1
    }
  ],
  "to_user_id": 6
}
```

Ответ:
```json
{
  "feedback_items": [
    {
      "metric_id": 2,
      "text": "bad",
      "score": 2
    },
    {
      "metric_id": 1,
      "text": "cool",
      "score": 5
    }
  ],
  "to_user_id": 6
}
```
