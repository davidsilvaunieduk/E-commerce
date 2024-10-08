from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT,
            price REAL,
            image_url TEXT
        )
    ''')
    cursor.execute("SELECT COUNT(*) FROM products")
    if cursor.fetchone()[0] == 0:
        cursor.execute('''
            INSERT INTO products (name, price, image_url) VALUES
            ('Planta 1', 10.0, 'static/images/planta1.jpg'),
            ('Planta 2', 15.0, 'static/images/planta2.jpg'),
            ('Planta 3', 20.0, 'static/images/planta3.jpg'),
            ('Planta 4', 25.0, 'static/images/planta4.jpg'),
            ('Planta 5', 30.0, 'static/images/planta5.jpg'),
            ('Planta 6', 35.0, 'static/images/planta6.jpg')
        ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()
    conn.close()
    return render_template('index.html', products=products)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_id = request.form.get('product_id')
    quantity = request.form.get('quantity')
    if 'cart' not in session:
        session['cart'] = {}
    if product_id in session['cart']:
        session['cart'][product_id] += int(quantity)
    else:
        session['cart'][product_id] = int(quantity)
    
    session['added'] = f'Produto {product_id} adicionado ao carrinho com sucesso!'
    return redirect(url_for('index'))

@app.route('/cart')
def cart():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()
    conn.close()
    return render_template('cart.html', cart=session.get('cart', {}), products=products)

@app.route('/checkout', methods=['POST'])
def checkout():
    name = request.form.get('name')
    address = request.form.get('address')
    phone = request.form.get('phone')
    email = request.form.get('email')
    city = request.form.get('city')

    order_summary = f'Compra finalizada! Nome: {name}, Endereço: {address}, Telefone: {phone}, E-mail: {email}, Cidade: {city}'
    
    session.pop('cart', None)
    return order_summary

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
