import requests
import re
import random
import pandas as pd
import logging
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from tokens import tokens

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Функция для отправки ответа на отзыв
def send_response(token, text, feedback_id):
    url = 'https://feedbacks-api.wildberries.ru/api/v1/feedbacks'
    headers = {'Authorization': token}
    body = {"id": feedback_id, "text": text}
    
    try:
        response = requests.patch(url, headers=headers, json=body)
        if response.status_code == 200:
            logging.info(f"Successfully sent response for feedback ID {feedback_id}")
        else:
            logging.error(f"Failed to send response for feedback ID {feedback_id}: {response.status_code}")
    except Exception as e:
        logging.error(f"Error occurred while sending response: {e}")

# Функция для сбора отзывов
def collect_feedbacks(tokens):
    extracted_negative = []
    extracted_positive = []
    url = 'https://feedbacks-api.wildberries.ru/api/v1/feedbacks'

    for token in tokens:
        headers = {'Authorization': token}
        params = {"isAnswered": 'false', "take": '5000', "skip": '0'}
        
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()

            feedbacks = data.get('data', {}).get('feedbacks', [])
            logging.info(f"Collected {len(feedbacks)} feedbacks")
            
            for feedback in feedbacks:
                product_id = feedback['productDetails']['nmId']
                supplier_article = feedback['productDetails']['supplierArticle']
                product_name = feedback['productDetails']['productName']
                text = feedback['text']
                rating = feedback['productValuation']
                feedback_id = feedback['id']
                creation_date = feedback['createdDate']

                # Если рейтинг 5 и текст не пустой, отправляем ответ
                if rating == 5 and text:
                    generate_response(text, feedback_id, token)

                # Собираем данные о негативных и позитивных отзывах
                if rating in [1, 2, 3, 4]:
                    extracted_negative.append({
                        'date': creation_date,
                        'product_id': product_id,
                        'supplier_article': supplier_article,
                        'product_name': product_name,
                        'rating': rating,
                        'text': text,
                    })
                if rating in [4, 5]:
                    extracted_positive.append({
                        'date': creation_date,
                        'product_id': product_id,
                        'supplier_article': supplier_article,
                        'product_name': product_name,
                        'rating': rating,
                        'text': text,
                    })
        except requests.RequestException as e:
            logging.error(f"Failed to collect feedbacks: {e}")
    
    df_negative = pd.DataFrame(extracted_negative)
    df_positive = pd.DataFrame(extracted_positive)
    
    # Возвращаем DataFrame'ы для дальнейшего использования
    return df_negative, df_positive

# Проверка на наличие негативных фраз в тексте
def contains_negative_phrases(text, negative_phrases):
    clean_text = re.sub(r'[^\p{L}\s]', '', text).lower()
    for phrase in negative_phrases:
        if re.search(r'\b' + re.escape(phrase.lower()) + r'\b', clean_text):
            return True
    return False

# Генерация ответа на отзыв
def generate_response(text, feedback_id, token):
    negative_phrases = ['смотри фото', 'засохли', 'рваная упаковка', 'поврежден']
    response_templates = {
        'podarok': 'Спасибо за ваш отзыв и за выбор нашего товара в качестве подарка! Ждем Вас за новыми покупками для творчества.',
        'udovolstvie': 'Рады, что наши товары приносят Вам удовольствие! Ждем Вас за новыми покупками.',
        'quality': 'Спасибо за высокую оценку качества нашего товара. Надеемся, что вы останетесь довольны новыми покупками.',
        'like': 'Спасибо за положительный отзыв о нашем товаре! Желаем творческих успехов.',
        'recomendation': 'Спасибо за рекомендацию нашего бренда. Ждем Вас за новыми покупками!',
        'smile': 'Благодарим за отзыв! Мы рады, что наш товар принес Вам радость.',
        'default': 'Спасибо за Ваш отзыв! Ждем Вас за новыми покупками в PRIMEHOBBY.'
    }

    keywords = {
        'podarok': ['подарок', 'сюрприз', 'поздравил'],
        'udovolstvie': ['удовольствие', 'удовлетворение'],
        'quality': ['качество', 'качественный'],
        'smile': ['❤️', '👍🏻', '🥰', '🔥', '😍'],
        'like': ['понравилось', 'нравиться'],
        'recomendation': ['рекомендую', 'рекомендуем']
    }

    # Если отзыв содержит негативные фразы, не отвечаем
    if contains_negative_phrases(text, negative_phrases):
        logging.info(f"Feedback ID {feedback_id} contains negative phrases, skipping response.")
        return

    # Поиск ключевых слов в тексте
    for category, words in keywords.items():
        if any(word in text.lower() for word in words):
            response_text = response_templates.get(category, response_templates['default'])
            send_response(token, response_text, feedback_id)
            return

    # Если ключевые слова не найдены, используем типичный ответ
    send_response(token, response_templates['default'], feedback_id)


collect_feedbacks(tokens)