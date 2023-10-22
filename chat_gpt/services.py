import openai
import g4f

# API_KEY = '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'
# openai.api_key = API_KEY
from api.models import Feedback, Metric, FeedbackItem

openai.api_base = "http://localhost:1337/v1"


def ask_gpt():
    response = g4f.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hello"}],
        stream=True,
    )


def generate_text(feedback: Feedback):
    metrics = {"metrics": []}
    for metric in Metric.objects.all():
        metrics["metrics"].append(
            {"id": metric.id, "name": metric.title},
        )

    worker_name = f"{feedback.to_user.name.capitalize()} {feedback.to_user.surname.capitalize()}"

    data = []
    feedback_items = FeedbackItem.objects.filter(feedback=feedback)
    for item in feedback_items:
        data.append({"author": 123})
    data = [
        {
            "author": "Максим Окулов",
            "metrics": [
                {
                    "metrics_id": 0,
                    "score": 3,
                    "text": "Сотрудник был мотивирован, но не всегда выполнял задачи "
                    "корректно из-за плохой коммуникации.",
                },
                {
                    "metrics_id": 1,
                    "score": 2,
                    "text": "Сотрудник не предлагал ничего нового, а просто плыл по " "течению.",
                },
            ],
        },
        {
            "author": "Кирилл Куликов",
            "metrics": [
                {
                    "metrics_id": 0,
                    "score": 2,
                    "text": "Сотрудник выполнил лишь 26% от поставленных задач. Выполнял " "задачи долго.",
                },
                {
                    "metrics_id": 1,
                    "score": 5,
                    "text": "Cотрудник организовывает мероприятие 'пятница настольных игр'. "
                    "Это делает команду дружнее, что соответствует корпоративным "
                    "ценностям.",
                },
            ],
        },
    ]

    text = f"""Ты ассистент, который должен анализировать отзывы авторов о стажерах. Я буду предоставлять тебе данные в таком 
    формате: 

[NAME OF FORKER]: Имя стажера, о котором пишут отзыв, это не тот, о котором пишут отзывы. 

Массив названий метрик с ID 
{{"metrics": ["id": Айди метрики, "name": Название метрики]}}

Массив метрик в формате json: {{"author": Имя автора, который оставляет отзыв, "metriks": [{{"metrics_id": id 
метрики из массива названий метрик, "score": Оценка по 5 бальной шкале, "text": Отзыв по метрике}}] 


Твоя определить эмоциональную окраску каждого отзыва (положительный, нейтральный, отрицательный отзыв). 
Так же, тебе нужно сделать один ОБЩИЙ ОТЗЫВ, который тебе нужно сделать исходя из отзывов, которые я тебе предоставлю.
Этот отзыв должен содержать в себе рекомендации по устранению слабых сторон сотрудника.

Так же, мне нужно, что бы ты посчитал общую оценку по 5 бальной шкале, где 1 это ужасно, а 5 это отлично


[NAME OF FORKER]:  {worker_name}

{metrics}

{data}

Когда будешь формировать ответ, пользуйся таким правилом:
Оценка по 5 бальной шкале должна быть числом, без пояснений
Оценка тональности должна быть выражена в числе, где 0 - нейтрально, -1 - негативно, 1 положительно. Оценка тональности должна быть без пояснений.

Выводи в ответ только в формате json, только json и ничего более, без каких либо пояснений: {{"main": ОБЩИЙ ОТЗЫВ, "tonal": [{{"name": ИМЯ АВТОРА, 
"metrik_list": ["id": АЙДИ МЕТРИКИ, "score": Оценка тональности метрики]]}}, "score": ОБЩИЙ БАЛЛ}} 


"""
    return text
