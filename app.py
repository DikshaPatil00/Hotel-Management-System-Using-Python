from flask import Flask, render_template, request, redirect, url_for
import random

app = Flask(__name__)

# Global variables to store temporary data
room_booking = {}
food_order = {}
payment_info = {}

# Home Page
@app.route('/')
def home():
    return render_template('home.html')

#Book Room
@app.route('/book', methods=['GET', 'POST'])
def book_room():
    if request.method == 'POST':
        name = request.form['name']
        days = int(request.form['days'])
        room_choice = int(request.form['room_choice'])

        room_types = ['Standard Non-AC', 'Standard AC', '3-Bed Non-AC', '3-Bed AC']
        room_prices = [3500, 4000, 4500, 5000]

        room_type = room_types[room_choice - 1]
        room_price = room_prices[room_choice - 1]
        room_no = random.randint(100, 500)
        cust_id = random.randint(10, 99)
        total_cost = room_price * days

        room_booking.update({
            "name": name,
            "days": days,
            "room_type": room_type,
            "room_price": room_price,
            "room_no": room_no,
            "cust_id": cust_id,
            "total_cost": total_cost
        })

        return redirect(url_for('home'))

    return render_template('book.html')

# Rooms Info
@app.route('/rooms')
def rooms_info():
    room_types = ['Standard Non-AC', 'Standard AC', '3-Bed Non-AC', '3-Bed AC']
    room_prices = [3500, 4000, 4500, 5000]
    room_details = [
        "Double Bed, TV, Balcony, Washroom",
        "Double Bed, TV, Balcony, AC, Washroom",
        "3 Beds, TV, Balcony, Washroom",
        "3 Beds, TV, Balcony, AC, Washroom"
    ]
    rooms = list(zip(room_types, room_prices, room_details))
    return render_template('rooms.html', rooms=rooms)

#Restaurant Order
@app.route('/order', methods=['GET', 'POST'])
def restaurant_order():
    menu = {
        '1': ('Pizza', 330),
        '2': ('Pasta', 220),
        '3': ('Burger', 130),
        '4': ('Salad', 100)
    }
    if request.method == 'POST':
        items = request.form.getlist('items')
        total = 0
        ordered_items = []
        for item in items:
            ordered_items.append(menu[item][0])
            total += menu[item][1]
        food_order.update({
            "items": ordered_items,
            "total": total
        })
        return redirect(url_for('home'))

    return render_template('order.html', menu=menu)

#Payment
@app.route('/payment', methods=['GET', 'POST'])
def payment():
    total_room = room_booking.get("total_cost", 0)
    total_food = food_order.get("total", 0)
    total_amount = total_room + total_food

    if request.method == 'POST':
        method = request.form['method']
        confirm = request.form.get('confirm')
        if confirm == 'yes':
            payment_info.update({
                "method": method,
                "total": total_amount
            })
            return redirect(url_for('thank_you'))

    return render_template('payment.html', total=total_amount)

#Thank You Page
@app.route('/thankyou')
def thank_you():
    total = payment_info.get("total", 0)
    method = payment_info.get("method", "")
    return render_template('thankyou.html', total=total, method=method)

#Run app
if __name__ == '__main__':
    app.run(debug=True)