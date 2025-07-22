from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'

# Database setup
def init_db():
    conn = sqlite3.connect('restaurant.db')
    c = conn.cursor()
    
    # Menu items table
    c.execute('''CREATE TABLE IF NOT EXISTS menu_items (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT NOT NULL,
                 category TEXT NOT NULL,
                 price REAL NOT NULL,
                 description TEXT,
                 available BOOLEAN DEFAULT 1
                 )''')
    
    # Bills table
    c.execute('''CREATE TABLE IF NOT EXISTS bills (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 customer_name TEXT NOT NULL,
                 table_number INTEGER,
                 total_amount REAL NOT NULL,
                 tax_amount REAL NOT NULL,
                 final_amount REAL NOT NULL,
                 date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                 )''')
    
    # Bill items table
    c.execute('''CREATE TABLE IF NOT EXISTS bill_items (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 bill_id INTEGER,
                 menu_item_id INTEGER,
                 quantity INTEGER NOT NULL,
                 unit_price REAL NOT NULL,
                 total_price REAL NOT NULL,
                 FOREIGN KEY (bill_id) REFERENCES bills (id),
                 FOREIGN KEY (menu_item_id) REFERENCES menu_items (id)
                 )''')
    
    # Insert sample menu items if empty
    c.execute('SELECT COUNT(*) FROM menu_items')
    if c.fetchone()[0] == 0:
        sample_items = [
            ('Margherita Pizza', 'Main Course', 12.99, 'Classic pizza with tomato sauce, mozzarella, and basil'),
            ('Caesar Salad', 'Appetizers', 8.50, 'Crisp romaine lettuce with caesar dressing and croutons'),
            ('Chicken Burger', 'Main Course', 14.99, 'Grilled chicken burger with fries'),
            ('Chocolate Cake', 'Desserts', 6.99, 'Rich chocolate cake with vanilla ice cream'),
            ('Coca Cola', 'Beverages', 2.99, 'Refreshing soft drink'),
            ('Pasta Carbonara', 'Main Course', 13.50, 'Creamy pasta with bacon and parmesan'),
            ('Garlic Bread', 'Appetizers', 4.99, 'Toasted bread with garlic butter'),
            ('Tiramisu', 'Desserts', 7.50, 'Classic Italian dessert'),
            ('Fresh Juice', 'Beverages', 3.99, 'Freshly squeezed orange juice'),
            ('Fish & Chips', 'Main Course', 16.99, 'Beer battered fish with crispy chips')
        ]
        c.executemany('INSERT INTO menu_items (name, category, price, description) VALUES (?, ?, ?, ?)', 
                     sample_items)
    
    conn.commit()
    conn.close()

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/menu')
def menu():
    conn = sqlite3.connect('restaurant.db')
    c = conn.cursor()
    c.execute('SELECT * FROM menu_items WHERE available = 1 ORDER BY category, name')
    items = c.fetchall()
    conn.close()
    
    # Group items by category
    menu_dict = {}
    for item in items:
        category = item[2]
        if category not in menu_dict:
            menu_dict[category] = []
        menu_dict[category].append(item)
    
    return render_template('menu.html', menu_dict=menu_dict)

@app.route('/create_bill')
def create_bill():
    conn = sqlite3.connect('restaurant.db')
    c = conn.cursor()
    c.execute('SELECT * FROM menu_items WHERE available = 1 ORDER BY category, name')
    items = c.fetchall()
    conn.close()
    
    menu_dict = {}
    for item in items:
        category = item[2]
        if category not in menu_dict:
            menu_dict[category] = []
        menu_dict[category].append(item)
    
    return render_template('create_bill.html', menu_dict=menu_dict)

@app.route('/generate_bill', methods=['POST'])
def generate_bill():
    customer_name = request.form['customer_name']
    table_number = request.form.get('table_number', '')
    selected_items = request.form.getlist('items')
    quantities = request.form.getlist('quantities')
    
    if not customer_name or not selected_items:
        flash('Please provide customer name and select at least one item', 'error')
        return redirect(url_for('create_bill'))
    
    conn = sqlite3.connect('restaurant.db')
    c = conn.cursor()
    
    # Calculate total
    total_amount = 0
    bill_items = []
    
    for i, item_id in enumerate(selected_items):
        if int(quantities[i]) > 0:
            c.execute('SELECT name, price FROM menu_items WHERE id = ?', (item_id,))
            item = c.fetchone()
            if item:
                qty = int(quantities[i])
                unit_price = item[1]
                item_total = qty * unit_price
                total_amount += item_total
                bill_items.append((item_id, qty, unit_price, item_total, item[0]))
    
    # Calculate tax (10%)
    tax_rate = 0.10
    tax_amount = total_amount * tax_rate
    final_amount = total_amount + tax_amount
    
    # Insert bill
    c.execute('''INSERT INTO bills (customer_name, table_number, total_amount, tax_amount, final_amount)
                 VALUES (?, ?, ?, ?, ?)''',
              (customer_name, table_number if table_number else None, total_amount, tax_amount, final_amount))
    
    bill_id = c.lastrowid
    
    # Insert bill items
    for item_id, qty, unit_price, item_total, _ in bill_items:
        c.execute('''INSERT INTO bill_items (bill_id, menu_item_id, quantity, unit_price, total_price)
                     VALUES (?, ?, ?, ?, ?)''',
                  (bill_id, item_id, qty, unit_price, item_total))
    
    conn.commit()
    conn.close()
    
    return redirect(url_for('view_bill', bill_id=bill_id))

@app.route('/bill/<int:bill_id>')
def view_bill(bill_id):
    conn = sqlite3.connect('restaurant.db')
    c = conn.cursor()
    
    # Get bill details
    c.execute('SELECT * FROM bills WHERE id = ?', (bill_id,))
    bill = c.fetchone()
    
    if not bill:
        flash('Bill not found', 'error')
        return redirect(url_for('index'))
    
    # Get bill items with menu item details
    c.execute('''SELECT bi.quantity, bi.unit_price, bi.total_price, mi.name
                 FROM bill_items bi
                 JOIN menu_items mi ON bi.menu_item_id = mi.id
                 WHERE bi.bill_id = ?''', (bill_id,))
    items = c.fetchall()
    
    conn.close()
    
    return render_template('bill_view.html', bill=bill, items=items)

@app.route('/bills')
def view_bills():
    conn = sqlite3.connect('restaurant.db')
    c = conn.cursor()
    c.execute('SELECT * FROM bills ORDER BY date_created DESC LIMIT 50')
    bills = c.fetchall()
    conn.close()
    
    return render_template('bill_list.html', bills=bills)

@app.route('/admin')
def admin():
    conn = sqlite3.connect('restaurant.db')
    c = conn.cursor()
    
    # Get recent stats
    c.execute('SELECT COUNT(*) FROM bills WHERE date(date_created) = date("now")')
    today_bills = c.fetchone()[0]
    
    c.execute('SELECT SUM(final_amount) FROM bills WHERE date(date_created) = date("now")')
    today_revenue = c.fetchone()[0] or 0
    
    c.execute('SELECT COUNT(*) FROM menu_items WHERE available = 1')
    active_items = c.fetchone()[0]
    
    conn.close()
    
    return render_template('admin.html', 
                         today_bills=today_bills,
                         today_revenue=today_revenue,
                         active_items=active_items)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)