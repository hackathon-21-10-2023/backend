import g4f
import openai
# API_KEY = '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'
# openai.api_key = API_KEY
from django.core.management import BaseCommand

from api.models import FeedbackForUser, Metric, FeedbackItem

openai.api_base = "http://127.0.0.1:1337/v1"


def ask_gpt(feedback_for_user_id):
    feedback_for_user = FeedbackForUser.objects.get(id=feedback_for_user_id)
    text = generate_text(feedback_for_user)
    print(f"{text=}")
    response = g4f.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": text}],
    )
    return response


def generate_text(feedback_for_user: FeedbackForUser):
    metrics = {'metrics': []}
    for metric in Metric.objects.all():
        metrics['metrics'].append(
            {"id": metric.id, "name": metric.title},
        )
    feedback = feedback_for_user.feedbacks.last()
    worker_name = f'{feedback.to_user.name.capitalize()} {feedback.to_user.surname.capitalize()}'

    data = []
    feedbacks = feedback_for_user.feedbacks.all()
    for feedback in feedbacks:
        i = {
            "author": f'{feedback.from_user.name.capitalize()} {feedback.from_user.surname.capitalize()}',
            'metrics': []
        }
        feedback_items = FeedbackItem.objects.filter(feedback=feedback)
        for feedback_item in feedback_items:
            i['metrics'].append(
                {
                    "metrics_id": feedback_item.metric.id,
                    'score': feedback_item.score,
                    'text': feedback_item.text,
                    'feedback_item_id': feedback_item.id
                }
            )

        data.append(i)
    # print(metrics)
    # print(data)

    text = f'''Ты ассистент, который должен анализировать отзывы авторов о стажерах. Я буду предоставлять тебе данные в таком 
    формате: 

[NAME OF FORKER]: Имя стажера, о котором пишут отзыв, это не тот, о котором пишут отзывы. 

Массив названий метрик с ID 
{{"metrics": ["id": Айди метрики, "name": Название метрики]}}

Массив метрик в формате json: {{"author": Имя автора, который оставляет отзыв, "metriks": [{{"metrics_id": id 
метрики из массива названий метрик, "score": Оценка по 5 бальной шкале, "text": Отзыв по метрике, "feedback_item_id": АЙДИ ОТЗЫВА ВНУТРИ СИСТЕМЫ}}] 


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
"metrik_list": ["id": АЙДИ МЕТРИКИ, "score": Оценка тональности метрики, "item_id": АЙДИ ОТЗЫВА ВНУТРИ СИСТЕМЫ]]}}, "score": ОБЩИЙ БАЛЛ}} 


'''
    return text


class Command(BaseCommand):

    def handle(self, *args, **options):
        print(ask_gpt(1))
