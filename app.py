#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Интернет-магазин украшений
"""

from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import pandas as pd
import os
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Production-ready configuration
app.secret_key = os.getenv('SECRET_KEY', 'secret_key_for_jewelry_store_2024')
app.config['DEBUG'] = os.getenv('DEBUG', 'False').lower() == 'true'

# Security settings for production
if os.getenv('FLASK_ENV') == 'production':
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

class JewelryStore:
    def __init__(self):
        self.products = []
        self.load_products()
    
    def load_products(self):
        """Загружаем товары из Excel файла"""
        try:
            # Читаем Excel файл
            df = pd.read_excel('price.xlsx')
            
            # Очищаем названия колонок от пробелов
            df.columns = df.columns.str.strip()
            
            print(f"Загружено {len(df)} строк из Excel файла")
            print(f"Колонки: {df.columns.tolist()}")
            
            # Конвертируем в список словарей
            self.products = []
            for index, row in df.iterrows():
                try:
                    # Проверяем, что строка содержит данные
                    if pd.isna(row['№']) or pd.isna(row['цена']):
                        continue
                        
                    # Создаем красивое название на основе описания
                    description = str(row['описание']) if pd.notna(row['описание']) else ''
                    product_name = self._create_product_name(description, int(row['№']))
                    
                    # Обрабатываем изображение
                    image_url = str(row['фото']) if pd.notna(row['фото']) else None
                    processed_image = self._process_image_url(image_url)
                    
                    product = {
                        'id': int(row['№']),
                        'name': product_name,
                        'price': float(row['цена']),
                        'description': description if description else 'Красивое украшение ручной работы',
                        'category': self._get_category_from_description(description),
                        'size': str(row['размер']) if pd.notna(row['размер']) else 'Универсальный',
                        'image': processed_image['url'],
                        'has_external_image': processed_image['is_external'],
                        'photo_url': image_url  # Сохраняем оригинальную ссылку для справки
                    }
                    self.products.append(product)
                except (ValueError, IndexError, KeyError) as e:
                    print(f"Ошибка в строке {index}: {e}, данные: {dict(row)}")
                    continue
            
            print(f"Успешно загружено {len(self.products)} товаров")
                
        except Exception as e:
            print(f"Ошибка при загрузке Excel файла: {e}")
            # Создаем демо-данные если файл не читается
            self.products = [
                {
                    'id': 1,
                    'name': 'Золотое кольцо с бриллиантом',
                    'price': 45000.0,
                    'description': 'Элегантное золотое кольцо 585 пробы с натуральным бриллиантом 0.5 карат',
                    'category': 'Кольца',
                    'image': '/static/images/ring1.jpg'
                },
                {
                    'id': 2,
                    'name': 'Серебряные серьги с жемчугом',
                    'price': 8500.0,
                    'description': 'Изящные серебряные серьги с натуральным речным жемчугом',
                    'category': 'Серьги',
                    'image': '/static/images/earrings1.jpg'
                },
                {
                    'id': 3,
                    'name': 'Золотая цепочка',
                    'price': 25000.0,
                    'description': 'Классическая золотая цепочка плетения "Якорь" 585 пробы',
                    'category': 'Цепочки',
                    'image': '/static/images/chain1.jpg'
                },
                {
                    'id': 4,
                    'name': 'Браслет с подвесками',
                    'price': 12000.0,
                    'description': 'Стильный серебряный браслет с декоративными подвесками',
                    'category': 'Браслеты',
                    'image': '/static/images/bracelet1.jpg'
                }
            ]
    
    def get_all_products(self):
        return self.products
    
    def get_product_by_id(self, product_id):
        return next((p for p in self.products if p['id'] == product_id), None)
    
    def _process_image_url(self, image_url):
        """Обрабатываем URL изображения для корректного отображения"""
        if not image_url or image_url == 'nan':
            return {
                'url': f'/static/images/placeholder.jpg',
                'is_external': False
            }
        
        # Проверяем, если это ссылка на cloud.mail.ru
        if 'cloud.mail.ru/public/' in image_url:
            # Преобразуем URL в формат thumbnail
            # Из: https://cloud.mail.ru/public/H2DC/ML95dukgp
            # В: https://thumb.cloud.mail.ru/weblink/thumb/xw1/H2DC/ML95dukgp
            
            # Извлекаем часть после /public/
            try:
                public_part = image_url.split('/public/')[-1]
                # Создаем URL для thumbnail
                thumbnail_url = f"https://thumb.cloud.mail.ru/weblink/thumb/xw1/{public_part}"
                print(f"Конвертируем URL: {image_url} -> {thumbnail_url}")
                return {
                    'url': thumbnail_url,
                    'is_external': True
                }
            except Exception as e:
                print(f"Ошибка конвертации URL {image_url}: {e}")
                return {
                    'url': f'/static/images/placeholder.jpg',
                    'is_external': False
                }
        
        # Если это другая внешняя ссылка
        elif image_url.startswith('http'):
            return {
                'url': image_url,
                'is_external': True
            }
        
        # Локальная ссылка или неопознанный формат
        else:
            return {
                'url': f'/static/images/placeholder.jpg',
                'is_external': False
            }

    def _create_product_name(self, description, product_id):
        """Создаем красивое название товара на основе описания"""
        if not description:
            return f"Украшение №{product_id}"
        
        description_lower = description.lower()
        
        # Определяем тип украшения
        if any(word in description_lower for word in ['кольцо', 'перстень']):
            base_name = 'Кольцо'
        elif any(word in description_lower for word in ['серьги', 'серёжки']):
            base_name = 'Серьги'
        elif any(word in description_lower for word in ['цепочка', 'цепь']):
            base_name = 'Цепочка'
        elif any(word in description_lower for word in ['колье', 'ожерелье']):
            base_name = 'Колье'
        elif any(word in description_lower for word in ['браслет']):
            base_name = 'Браслет'
        elif any(word in description_lower for word in ['подвеска', 'кулон']):
            base_name = 'Подвеска'
        elif any(word in description_lower for word in ['брошь', 'брошка']):
            base_name = 'Брошь'
        elif any(word in description_lower for word in ['запонки']):
            base_name = 'Запонки'
        else:
            base_name = 'Украшение'
        
        # Добавляем материал, если есть
        if any(word in description_lower for word in ['золот', 'золоч']):
            material = 'золотой'
        elif any(word in description_lower for word in ['серебр']):
            material = 'серебряный'
        elif any(word in description_lower for word in ['платин']):
            material = 'платиновый'
        else:
            material = None
        
        # Добавляем камни, если есть
        stones = []
        if any(word in description_lower for word in ['бриллиант', 'алмаз']):
            stones.append('с бриллиантом')
        if any(word in description_lower for word in ['изумруд']):
            stones.append('с изумрудом')
        if any(word in description_lower for word in ['рубин']):
            stones.append('с рубином')
        if any(word in description_lower for word in ['сапфир']):
            stones.append('с сапфиром')
        if any(word in description_lower for word in ['жемчуг']):
            stones.append('с жемчугом')
        if any(word in description_lower for word in ['топаз']):
            stones.append('с топазом')
        
        # Формируем итоговое название
        if material and stones:
            return f"{base_name} {material} {' и '.join(stones)}"
        elif material:
            return f"{base_name} {material}"
        elif stones:
            return f"{base_name} {' и '.join(stones)}"
        else:
            return f"{base_name} №{product_id}"

    def _get_category_from_description(self, description):
        """Определяем категорию по описанию"""
        description_lower = description.lower()
        
        if any(word in description_lower for word in ['кольцо', 'перстень']):
            return 'Кольца'
        elif any(word in description_lower for word in ['серьги', 'серёжки']):
            return 'Серьги'
        elif any(word in description_lower for word in ['цепочка', 'цепь', 'колье', 'ожерелье']):
            return 'Цепочки и колье'
        elif any(word in description_lower for word in ['браслет']):
            return 'Браслеты'
        elif any(word in description_lower for word in ['подвеска', 'кулон']):
            return 'Подвески'
        elif any(word in description_lower for word in ['брошь', 'брошка']):
            return 'Броши'
        elif any(word in description_lower for word in ['запонки']):
            return 'Запонки'
        else:
            return 'Украшения'
    
    def get_categories(self):
        return list(set(p['category'] for p in self.products))

# Инициализируем магазин
store = JewelryStore()

@app.route('/')
def index():
    """Главная страница с каталогом"""
    category = request.args.get('category')
    products = store.get_all_products()
    
    if category:
        products = [p for p in products if p['category'] == category]
    
    categories = store.get_categories()
    return render_template('index.html', products=products, categories=categories, selected_category=category)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    """Детальная страница товара"""
    product = store.get_product_by_id(product_id)
    if not product:
        return redirect(url_for('index'))
    return render_template('product_detail.html', product=product)

@app.route('/cart')
def cart():
    """Страница корзины"""
    cart_items = session.get('cart', {})
    total = 0
    cart_products = []
    
    for product_id, quantity in cart_items.items():
        product = store.get_product_by_id(int(product_id))
        if product:
            item_total = product['price'] * quantity
            cart_products.append({
                'product': product,
                'quantity': quantity,
                'total': item_total
            })
            total += item_total
    
    return render_template('cart.html', cart_products=cart_products, total=total)

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    """Добавить товар в корзину"""
    if 'cart' not in session:
        session['cart'] = {}
    
    product_id_str = str(product_id)
    if product_id_str in session['cart']:
        session['cart'][product_id_str] += 1
    else:
        session['cart'][product_id_str] = 1
    
    session.modified = True
    return redirect(url_for('product_detail', product_id=product_id))

@app.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    """Удалить товар из корзины"""
    if 'cart' in session:
        product_id_str = str(product_id)
        if product_id_str in session['cart']:
            del session['cart'][product_id_str]
            session.modified = True
    
    return redirect(url_for('cart'))

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    """Оформление заказа"""
    if request.method == 'POST':
        # Обработка формы заказа
        customer_data = {
            'name': request.form['name'],
            'email': request.form['email'],
            'phone': request.form['phone'],
            'address': request.form['address'],
            'order_date': datetime.now().isoformat(),
            'cart': session.get('cart', {})
        }
        
        # Очищаем корзину
        session['cart'] = {}
        session.modified = True
        
        return render_template('order_success.html', customer_data=customer_data)
    
    return render_template('checkout.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)