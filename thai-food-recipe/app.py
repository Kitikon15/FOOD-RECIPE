# app.py

# นำเข้าเครื่องมือสร้างเว็บจากโมดูล Flask
from flask import Flask, jsonify, request, render_template
# นำเข้าตัวจัดการอาหารและสูตร (FoodManager Object)
from services.food_manager import FoodManager
# นำเข้าตัวบันทึกประวัติการสั่งซื้อ (OrderManager Object)
from services.order_manager import OrderManager
# นำเข้าเครื่องมือคุมหมวดหมู่หลัก
from models.category import Category

# เริ่มต้นสร้างแอปพลิเคชันหลังบ้าน Flask Web App
app = Flask(__name__)

# ดึงหรือสร้างออบเจกต์จัดการของเซิร์ฟเวอร์หลังบ้าน (Singleton)
food_manager = FoodManager()
order_manager = OrderManager()

@app.route('/')
def index():
    # แสดงผลหน้าจอกรอบเว็บหลักของโปรแกรม (index.html)
    return render_template('index.html')

@app.route('/api/categories', methods=['GET'])
def get_categories():
    # ส่งคืนประเภทหมวดหมู่อาหารหลักทั้งหมดในระบบเป็น JSON Array
    return jsonify(Category.get_all_categories())

@app.route('/api/foods', methods=['GET'])
def get_foods():
    # ส่งคืนรายการจานอาหารทั้งหมด รองรับการกรองตามประเภท หรือสืบค้นตามวัตถุดิบ/ชื่อเมนู
    category = request.args.get('category')
    query = request.args.get('query')
    
    # ดำเนินการคัดกรองข้อมูลตามพารามิเตอร์ที่ส่งเข้ามาในลิงก์ Url
    if query:
        foods = food_manager.search_foods(query)
    elif category:
        foods = food_manager.get_foods_by_category(category)
    else:
        foods = food_manager.get_all_foods()
        
    # แปลงออบเจกต์อาหารทุกจานในลิสต์เป็น Dictionary และส่งออกเป็นข้อมูล JSON Array
    return jsonify([f.to_dict() for f in foods])

@app.route('/api/foods/<name>', methods=['GET'])
def get_food(name):
    # ส่งคืนสูตรส่วนผสมและรายละเอียดอาหารเจาะจงเฉพาะตัวจานอาหาร
    food = food_manager.get_food_by_name(name)
    if not food:
        # ส่งค่าแจ้งล้มเหลวกลับไปพร้อม HTTP status 404 (Not Found)
        return jsonify({"error": f"ไม่พบเมนูอาหาร '{name}'"}), 404
    # ส่งโครงสร้างสูตรปรุงจานอาหารกลับไป
    return jsonify(food.to_dict())

@app.route('/api/popular', methods=['GET'])
def get_popular():
    # ส่งคืนรายชื่อเมนูอาหารยอดฮิตขายดีที่สุด 6 ลำดับแรก
    popular_foods = food_manager.get_popular_foods(limit=6)
    return jsonify([f.to_dict() for f in popular_foods])

@app.route('/api/orders', methods=['GET'])
def get_orders():
    # ส่งคืนประวัติประวัติบิลสั่งซื้ออาหารทั้งหมด
    orders = order_manager.get_order_history()
    return jsonify([o.to_dict() for o in orders])

@app.route('/api/orders', methods=['POST'])
def create_order():
    # รับบันทึกรายการตะกร้าสั่งซื้อใบใหม่เข้ามาในประวัติคำสั่งซื้อ
    data = request.get_json()
    if not data:
        return jsonify({"error": "ไม่พบข้อมูลการสั่งซื้อ"}), 400
        
    items = data.get("items", [])
    payment_method = data.get("payment_method", "Cash")
    
    try:
        # ลงทะเบียนบิลใบสั่งซื้อใหม่
        new_order = order_manager.create_order(items_data=items, payment_method=payment_method)
        # ส่งออกบิลใหม่พร้อมรหัส HTTP 201 (Created)
        return jsonify(new_order.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"เกิดข้อผิดพลาด: {str(e)}"}), 500

@app.route('/api/orders/<order_id>/pay', methods=['POST'])
def pay_order(order_id):
    # รับชำระเงินบิลออเดอร์ในระบบ พร้อมอัปเดตสถิติยอดสะสมขายดี
    order = order_manager.pay_order(order_id)
    if not order:
        return jsonify({"error": f"ไม่พบคำสั่งซื้อหมายเลข '{order_id}'"}), 404
    # ส่งข้อมูลบิลที่ทำการชำระเงินสำเร็จกลับคืนไป
    return jsonify(order.to_dict())

if __name__ == '__main__':
    app.run(debug=True, port=5000)
