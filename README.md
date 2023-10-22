# Хакатон бэк

```bash
python manage.py create_default_superuser
```


# Документация по беку v1

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


### Информация о пользователе (авторизация по JWT)
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

### Список пользователей, которых нужно оценить (авторизация по JWT) 
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

### Список всех общих отзывов о сотруднике

```GET /review/{employee_id}/```

Ответ:
```json
[
  {
    "feedback_items": [
      {
        "metric_title": "участие в корпоративной жизни компании",
        "text": "супер-пупер",
        "score_tone": 1,
        "score_tone_as_human": "положительная",
        "score": 5,
        "score_as_human": "отлично",
        "from_user": "Максим Окулов",
        "form_user_id": 4
      },
      {
        "metric_title": "участие в рабочих задачах",
        "text": "ааааа",
        "score_tone": 0,
        "score_tone_as_human": "нейтральная",
        "score": 5,
        "score_as_human": "отлично",
        "from_user": "Максим Окулов",
        "form_user_id": 4
      }
    ],
    "text": "Стажер Кирилл продемонстрировала разнонаправленные качества в рамках своей работы. В сфере участия в рабочих задачах, она была мотивированной, но иногда испытывала трудности в выполнении задач из-за коммуникативных проблем. Свой вклад в корпоративную жизнь компании она вносила в меньшей степени, ограничившись плавным плытьем по течению без активных инициатив",
    "score": 4,
    "score_as_human": "хорошо",
    "created_at": "2023-10-21T18:33:56.073744Z"
  }
]
```

Ты уж извини, Егор, но придется немного сортировать метрики, как ключ сортировки я оставил тебе form_user_id, извини, что костыляю.


### Создать отзыв (авторизация по JWT)

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
