from flask import Flask, jsonify, request, render_template
from services.food_manager import FoodManager
from services.order_manager import OrderManager
from models.category import Category

app = Flask(__name__)

# Initialize managers
food_manager = FoodManager()
order_manager = OrderManager()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/categories', methods=['GET'])
def get_categories():
    return jsonify(Category.get_all_categories())

@app.route('/api/foods', methods=['GET'])
def get_foods():
    category = request.args.get('category')
    query = request.args.get('query')
    
    if query:
        foods = food_manager.search_foods(query)
    elif category:
        foods = food_manager.get_foods_by_category(category)
    else:
        foods = food_manager.get_all_foods()
        
    return jsonify([f.to_dict() for f in foods])

@app.route('/api/foods/<name>', methods=['GET'])
def get_food(name):
    food = food_manager.get_food_by_name(name)
    if not food:
        return jsonify({"error": f"ไม่พบเมนูอาหาร '{name}'"}), 404
    return jsonify(food.to_dict())

@app.route('/api/popular', methods=['GET'])
def get_popular():
    # Return top 6 popular dishes
    popular_foods = food_manager.get_popular_foods(limit=6)
    return jsonify([f.to_dict() for f in popular_foods])

@app.route('/api/orders', methods=['GET'])
def get_orders():
    orders = order_manager.get_order_history()
    return jsonify([o.to_dict() for o in orders])

@app.route('/api/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    if not data:
        return jsonify({"error": "ไม่พบข้อมูลการสั่งซื้อ"}), 400
        
    items = data.get("items", [])
    payment_method = data.get("payment_method", "Cash")
    
    try:
        new_order = order_manager.create_order(items_data=items, payment_method=payment_method)
        return jsonify(new_order.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"เกิดข้อผิดพลาด: {str(e)}"}), 500

@app.route('/api/orders/<order_id>/pay', methods=['POST'])
def pay_order(order_id):
    order = order_manager.pay_order(order_id)
    if not order:
        return jsonify({"error": f"ไม่พบคำสั่งซื้อหมายเลข '{order_id}'"}), 404
    return jsonify(order.to_dict())

if __name__ == '__main__':
    app.run(debug=True, port=5000)
