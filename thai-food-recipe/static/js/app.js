// ==========================================================================
// APPLICATION STATE
// ==========================================================================
let cart = JSON.parse(localStorage.getItem('food_cart')) || [];
let activeCategory = 'all'; // 'all', 'ข้าวจานเดียว', 'ก๋วยเตี๋ยว', 'แกง/ซุป', 'popular', 'history'
let searchQuery = '';
let paymentTimerInterval = null;
let currentPendingOrderId = null;

// DOM Elements
const menuGrid = document.getElementById('menu-grid');
const historyContainer = document.getElementById('history-container');
const pageTitle = document.getElementById('page-title');
const categoryLabel = document.getElementById('current-category-label');
const itemsFoundLabel = document.getElementById('items-found-label');
const searchInput = document.getElementById('search-input');
const heroSec = document.getElementById('hero-sec');

const cartBtn = document.getElementById('cart-btn');
const cartSidebar = document.getElementById('cart-sidebar');
const closeCartBtn = document.getElementById('close-cart-btn');
const cartItemsContainer = document.getElementById('cart-items-container');
const cartCount = document.getElementById('cart-count');
const summaryItemsCount = document.getElementById('summary-items-count');
const summaryTotalPrice = document.getElementById('summary-total-price');
const checkoutSubmitBtn = document.getElementById('checkout-submit-btn');

// Recipe Modal Elements
const recipeModal = document.getElementById('recipe-modal');
const modalTitle = document.getElementById('modal-title');
const modalCategory = document.getElementById('modal-category');
const modalPrice = document.getElementById('modal-price');
const modalPopCount = document.getElementById('modal-pop-count');
const modalIngredientCount = document.getElementById('modal-ingredient-count');
const modalRecipeList = document.getElementById('modal-recipe-list');
const modalAddToCartBtn = document.getElementById('modal-add-to-cart-btn');
let currentOpenRecipeFood = null;

// Payment Modal Elements
const paymentModal = document.getElementById('payment-modal');
const paymentCloseBtn = document.getElementById('payment-close-btn');
const paymentCancelBtn = document.getElementById('payment-cancel-btn');
const paymentConfirmBtn = document.getElementById('payment-confirm-btn');

// ==========================================================================
// INITIALIZATION
// ==========================================================================
document.addEventListener('DOMContentLoaded', () => {
    setupSidebarNavigation();
    setupCartControls();
    setupSearchInput();
    setupRecipeModalControls();
    setupPaymentModalControls();
    
    // Load initial foods
    fetchFoods();
    updateCartUI();
});

// ==========================================================================
// NAVIGATION & SIDEBAR
// ==========================================================================
function setupSidebarNavigation() {
    const navItems = document.querySelectorAll('.nav-item');
    navItems.forEach(item => {
        item.addEventListener('click', (e) => {
            navItems.forEach(btn => btn.classList.remove('active'));
            item.classList.add('active');
            
            const tab = item.getAttribute('data-tab');
            activeCategory = tab;
            
            // Clear search when switching tabs
            searchInput.value = '';
            searchQuery = '';
            
            // Handle views
            handleTabSwitch(tab);
        });
    });
}

function handleTabSwitch(tab) {
    // Show/hide components based on tabs
    if (tab === 'history') {
        heroSec.classList.add('hidden');
        menuGrid.classList.add('hidden');
        historyContainer.classList.remove('hidden');
        pageTitle.innerText = 'ประวัติการสั่งซื้อ';
        fetchOrderHistory();
    } else {
        heroSec.classList.remove('hidden');
        menuGrid.classList.remove('hidden');
        historyContainer.classList.add('hidden');
        
        if (tab === 'all') {
            pageTitle.innerText = 'เมนูทั้งหมด';
        } else if (tab === 'popular') {
            pageTitle.innerText = 'เมนูยอดฮิตตามสูตรอาหาร';
        } else {
            pageTitle.innerText = `เมนูหมวด: ${tab}`;
        }
        
        fetchFoods();
    }
}

function scrollToMenu() {
    document.getElementById('menu-section-anchor').scrollIntoView({ behavior: 'smooth' });
}

// ==========================================================================
// SEARCH LOGIC (With Debounce)
// ==========================================================================
let debounceTimeout;
function setupSearchInput() {
    searchInput.addEventListener('input', (e) => {
        clearTimeout(debounceTimeout);
        debounceTimeout = setTimeout(() => {
            searchQuery = e.target.value;
            if (searchQuery.trim() !== '') {
                // If searching, switch to showing grid and reset active nav to 'all'
                if (activeCategory === 'history') {
                    activeCategory = 'all';
                    const navItems = document.querySelectorAll('.nav-item');
                    navItems.forEach(btn => btn.classList.remove('active'));
                    navItems[0].classList.add('active'); // Select 'all' tab
                    handleTabSwitch('all');
                }
                pageTitle.innerText = `ค้นหาสำหรับ: "${searchQuery}"`;
            } else {
                handleTabSwitch(activeCategory);
            }
            fetchFoods();
        }, 300);
    });
}

// ==========================================================================
// DATA FETCHING (API INTERACTION)
// ==========================================================================
function fetchFoods() {
    let url = '/api/foods';
    
    if (activeCategory === 'popular') {
        url = '/api/popular';
    } else {
        const params = new URLSearchParams();
        if (activeCategory !== 'all') {
            params.append('category', activeCategory);
        }
        if (searchQuery) {
            params.append('query', searchQuery);
        }
        const queryString = params.toString();
        if (queryString) {
            url += '?' + queryString;
        }
    }
    
    // Show Loading
    menuGrid.innerHTML = `
        <div class="loader-container">
            <div class="spinner"></div>
            <p>กำลังโหลดรายการเมนูอาหาร...</p>
        </div>
    `;
    
    fetch(url)
        .then(res => res.json())
        .then(foods => {
            renderFoodCards(foods);
        })
        .catch(err => {
            console.error('Error fetching foods:', err);
            menuGrid.innerHTML = `<p class="text-red text-center" style="grid-column: 1/-1;">เกิดข้อผิดพลาดในการโหลดเมนูอาหาร</p>`;
        });
}

function renderFoodCards(foods) {
    if (foods.length === 0) {
        menuGrid.innerHTML = `
            <div class="loader-container" style="padding: 40px 0;">
                <i class="fa-solid fa-face-frown-open" style="font-size: 48px; margin-bottom: 12px; opacity: 0.5;"></i>
                <p>ไม่พบรายการอาหารที่ตรงกับความต้องการ</p>
            </div>
        `;
        itemsFoundLabel.innerText = 'พบ 0 รายการ';
        return;
    }
    
    itemsFoundLabel.innerText = `พบ ${foods.length} รายการ`;
    categoryLabel.innerText = activeCategory === 'popular' ? 'เมนูที่มียอดสั่งซื้อสูงสุด' : 'เมนูพร้อมเสิร์ฟ';
    
    menuGrid.innerHTML = '';
    
    foods.forEach(food => {
        const card = document.createElement('div');
        card.classList.add('food-card');
        card.setAttribute('data-category', food.category);
        
        // Define category icon
        let iconClass = 'fa-bowl-rice';
        if (food.category === 'ก๋วยเตี๋ยว') {
            iconClass = 'fa-bowl-food';
        } else if (food.category === 'แกง/ซุป') {
            iconClass = 'fa-mug-hot';
        }
        
        // Check if popular badge is needed
        const popBadgeHtml = food.popularity > 0 
            ? `<div class="badge-pop"><i class="fa-solid fa-fire"></i> สั่งแล้ว ${food.popularity} ครั้ง</div>`
            : '';
            
        card.innerHTML = `
            <div class="card-img-wrapper">
                <i class="fa-solid ${iconClass}"></i>
                ${popBadgeHtml}
                <span class="badge-cat">${food.category}</span>
            </div>
            <div class="card-details-box">
                <h3>${food.nameTh}</h3>
                <div class="card-footer-info">
                    <span class="price">${food.price}</span>
                    <div class="card-actions">
                        <button class="action-btn recipe-trigger-btn" title="ดูสูตรวัตถุดิบ" onclick="openRecipeModal('${food.nameTh}')">
                            <i class="fa-solid fa-book-open"></i>
                        </button>
                        <button class="action-btn add-cart-trigger-btn" title="ใส่ตะกร้า" onclick="addToCart(${JSON.stringify(food).replace(/"/g, '&quot;')})">
                            <i class="fa-solid fa-plus"></i>
                        </button>
                    </div>
                </div>
            </div>
        `;
        menuGrid.appendChild(card);
    });
}

// ==========================================================================
// CART FUNCTIONALITY
// ==========================================================================
function setupCartControls() {
    cartBtn.addEventListener('click', () => cartSidebar.classList.add('open'));
    closeCartBtn.addEventListener('click', () => cartSidebar.classList.remove('open'));
    
    // Payment Trigger from Cart
    checkoutSubmitBtn.addEventListener('click', () => {
        openPaymentModal();
    });
    
    // Payment method selector click effect
    const methodOptions = document.querySelectorAll('.method-option');
    methodOptions.forEach(option => {
        option.addEventListener('click', () => {
            methodOptions.forEach(opt => opt.classList.remove('active'));
            option.classList.add('active');
            option.querySelector('input').checked = true;
        });
    });
}

function addToCart(food) {
    const existing = cart.find(item => item.nameTh === food.nameTh);
    if (existing) {
        existing.quantity += 1;
    } else {
        cart.push({
            nameTh: food.nameTh,
            category: food.category,
            price: food.price,
            quantity: 1
        });
    }
    saveCart();
    updateCartUI();
    
    // Micro-interaction: open cart to show item added
    cartSidebar.classList.add('open');
}

function updateCartQuantity(nameTh, delta) {
    const item = cart.find(item => item.nameTh === nameTh);
    if (item) {
        item.quantity += delta;
        if (item.quantity <= 0) {
            cart = cart.filter(i => i.nameTh !== nameTh);
        }
    }
    saveCart();
    updateCartUI();
}

function removeFromCart(nameTh) {
    cart = cart.filter(i => i.nameTh !== nameTh);
    saveCart();
    updateCartUI();
}

function saveCart() {
    localStorage.setItem('food_cart', JSON.stringify(cart));
}

function clearCart() {
    cart = [];
    saveCart();
    updateCartUI();
}

function updateCartUI() {
    // Update Badge
    const totalQty = cart.reduce((sum, item) => sum + item.quantity, 0);
    cartCount.innerText = totalQty;
    summaryItemsCount.innerText = `${totalQty} จาน`;
    
    // Update total price
    const totalPrice = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    summaryTotalPrice.innerText = `${totalPrice.toFixed(2)} บาท`;
    
    // Toggle checkout button
    checkoutSubmitBtn.disabled = cart.length === 0;
    
    // Render list
    if (cart.length === 0) {
        cartItemsContainer.innerHTML = `
            <div class="empty-cart">
                <i class="fa-solid fa-basket-shopping"></i>
                <p>ยังไม่มีสินค้าในตะกร้า</p>
                <span>เลือกอาหารจานโปรดของคุณเพื่อเริ่มสั่งซื้อ</span>
            </div>
        `;
        return;
    }
    
    cartItemsContainer.innerHTML = '';
    cart.forEach(item => {
        const itemEl = document.createElement('div');
        itemEl.classList.add('cart-item');
        
        let catClass = 'one-dish';
        if (item.category === 'ก๋วยเตี๋ยว') catClass = 'noodle';
        if (item.category === 'แกง/ซุป') catClass = 'soup-curry';
        
        let iconClass = 'fa-bowl-rice';
        if (item.category === 'ก๋วยเตี๋ยว') iconClass = 'fa-bowl-food';
        if (item.category === 'แกง/ซุป') iconClass = 'fa-mug-hot';
        
        itemEl.innerHTML = `
            <div class="cart-item-icon ${catClass}">
                <i class="fa-solid ${iconClass}"></i>
            </div>
            <div class="cart-item-info">
                <h4>${item.nameTh}</h4>
                <span class="item-price">${(item.price * item.quantity).toFixed(2)} ฿</span>
            </div>
            <div class="cart-item-qty">
                <button class="qty-btn" onclick="updateCartQuantity('${item.nameTh}', -1)">-</button>
                <span class="qty-val">${item.quantity}</span>
                <button class="qty-btn" onclick="updateCartQuantity('${item.nameTh}', 1)">+</button>
            </div>
            <i class="fa-regular fa-trash-can item-delete-btn" onclick="removeFromCart('${item.nameTh}')"></i>
        `;
        cartItemsContainer.appendChild(itemEl);
    });
}

// ==========================================================================
// RECIPE DETAILS MODAL
// ==========================================================================
function setupRecipeModalControls() {
    const closeTriggers = document.querySelectorAll('.modal-close-trigger');
    closeTriggers.forEach(trigger => {
        trigger.addEventListener('click', () => {
            recipeModal.classList.remove('open');
        });
    });
    
    // Add to cart inside modal
    modalAddToCartBtn.addEventListener('click', () => {
        if (currentOpenRecipeFood) {
            addToCart(currentOpenRecipeFood);
            recipeModal.classList.remove('open');
        }
    });
}

function openRecipeModal(nameTh) {
    fetch(`/api/foods/${nameTh}`)
        .then(res => res.json())
        .then(food => {
            currentOpenRecipeFood = food;
            
            // Set basic details
            modalTitle.innerText = `สูตรและวัตถุดิบ: ${food.nameTh}`;
            modalCategory.innerText = food.category;
            modalPrice.innerText = `${food.price} บาท`;
            modalPopCount.innerText = `${food.popularity} ครั้ง`;
            modalIngredientCount.innerText = `${food.recipeList.length} ชนิด`;
            
            // Set image category styling
            const visual = recipeModal.querySelector('.recipe-visual');
            visual.className = 'recipe-visual'; // Reset
            let iconClass = 'fa-bowl-rice';
            
            if (food.category === 'ข้าวจานเดียว') {
                visual.style.background = 'linear-gradient(135deg, #ffd166, #f78c6a)';
                iconClass = 'fa-bowl-rice';
            } else if (food.category === 'ก๋วยเตี๋ยว') {
                visual.style.background = 'linear-gradient(135deg, #833ab4, #fd1d1d)';
                iconClass = 'fa-bowl-food';
            } else if (food.category === 'แกง/ซุป') {
                visual.style.background = 'linear-gradient(135deg, #48cae4, #0077b6)';
                iconClass = 'fa-mug-hot';
            }
            visual.querySelector('i').className = `fa-solid ${iconClass} large-food-icon`;
            
            // Render ingredients list
            modalRecipeList.innerHTML = '';
            if (food.recipeList.length === 0) {
                modalRecipeList.innerHTML = '<div class="text-muted text-center" style="padding: 20px;">ไม่มีข้อมูลสัดส่วนวัตถุดิบ</div>';
            } else {
                food.recipeList.forEach(item => {
                    const row = document.createElement('div');
                    row.classList.add('ingredient-row');
                    row.innerHTML = `
                        <span>${item.recipeName}</span>
                        <span>${item.quantity} ${item.unitName}</span>
                    `;
                    modalRecipeList.appendChild(row);
                });
            }
            
            // Show modal
            recipeModal.classList.add('open');
        })
        .catch(err => {
            console.error('Error opening recipe details:', err);
            alert('ไม่สามารถโหลดข้อมูลสูตรวัตถุดิบได้');
        });
}

// ==========================================================================
// PAYMENT & SIMULATION LOGIC
// ==========================================================================
function setupPaymentModalControls() {
    paymentCloseBtn.addEventListener('click', cancelPaymentAction);
    paymentCancelBtn.addEventListener('click', cancelPaymentAction);
    paymentConfirmBtn.addEventListener('click', confirmPaymentAction);
    
    // Credit card number formatting
    const ccNum = document.getElementById('cc-num');
    ccNum.addEventListener('input', (e) => {
        let value = e.target.value.replace(/\s+/g, '').replace(/[^0-9]/gi, '');
        let formatted = '';
        for (let i = 0; i < value.length; i++) {
            if (i > 0 && i % 4 === 0) {
                formatted += ' ';
            }
            formatted += value[i];
        }
        e.target.value = formatted;
        
        // Update Card Layout preview
        document.querySelector('.card-number').innerText = formatted || '•••• •••• •••• ••••';
    });
    
    // Exp Date formatting
    const ccExp = document.getElementById('cc-exp');
    ccExp.addEventListener('input', (e) => {
        let value = e.target.value.replace(/\//g, '').replace(/[^0-9]/gi, '');
        if (value.length > 2) {
            e.target.value = value.substring(0, 2) + '/' + value.substring(2, 4);
        } else {
            e.target.value = value;
        }
        document.querySelector('.card-expiry div').innerText = e.target.value || 'MM/YY';
    });
}

function openPaymentModal() {
    const selectedMethod = document.querySelector('input[name="payment_method"]:checked').value;
    const totalPrice = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    
    // 1. Setup payment views layout
    document.querySelectorAll('.payment-view').forEach(view => view.classList.add('hidden'));
    
    // 2. Register Order on Backend first (Pending state)
    const orderItems = cart.map(item => ({
        food_name: item.nameTh,
        quantity: item.quantity
    }));
    
    fetch('/api/orders', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            items: orderItems,
            payment_method: selectedMethod
        })
    })
    .then(res => res.json())
    .then(order => {
        if (order.error) {
            alert(order.error);
            return;
        }
        
        currentPendingOrderId = order.order_id;
        
        // Show active view
        if (selectedMethod === 'PromptPay') {
            const ppView = document.getElementById('payment-view-promptpay');
            ppView.classList.remove('hidden');
            document.getElementById('pp-amount').innerText = `${totalPrice.toFixed(2)} บาท`;
            document.getElementById('pp-ref').innerText = order.order_id;
            startCountdownTimer();
        } else if (selectedMethod === 'Credit Card') {
            const cardView = document.getElementById('payment-view-card');
            cardView.classList.remove('hidden');
            document.getElementById('card-amount').innerText = `${totalPrice.toFixed(2)} บาท`;
            // Reset form
            document.getElementById('credit-card-form').reset();
            document.querySelector('.card-number').innerText = '•••• •••• •••• ••••';
            document.querySelector('.card-expiry div').innerText = 'MM/YY';
        } else if (selectedMethod === 'Cash') {
            const cashView = document.getElementById('payment-view-cash');
            cashView.classList.remove('hidden');
            document.getElementById('cash-amount').innerText = `${totalPrice.toFixed(2)} บาท`;
        }
        
        cartSidebar.classList.remove('open');
        paymentModal.classList.add('open');
    })
    .catch(err => {
        console.error('Error creating order:', err);
        alert('เกิดข้อผิดพลาดในการเริ่มสั่งซื้อสินค้า');
    });
}

function startCountdownTimer() {
    clearInterval(paymentTimerInterval);
    let time = 120; // 2 minutes
    const timerDisplay = document.getElementById('payment-timer');
    
    paymentTimerInterval = setInterval(() => {
        let minutes = Math.floor(time / 60);
        let seconds = time % 60;
        
        seconds = seconds < 10 ? '0' + seconds : seconds;
        timerDisplay.innerText = `0${minutes}:${seconds}`;
        
        if (--time < 0) {
            clearInterval(paymentTimerInterval);
            alert('หมดเวลาการสแกนชำระเงิน กรุณาทำรายการใหม่อีกครั้ง');
            cancelPaymentAction();
        }
    }, 1000);
}

function cancelPaymentAction() {
    clearInterval(paymentTimerInterval);
    paymentModal.classList.remove('open');
    currentPendingOrderId = null;
    alert('ยกเลิกการชำระเงินเรียบร้อยแล้ว');
}

function confirmPaymentAction() {
    clearInterval(paymentTimerInterval);
    
    if (!currentPendingOrderId) return;
    
    // Simulate loading effect on the button
    paymentConfirmBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> กำลังตรวจสอบ...';
    paymentConfirmBtn.disabled = true;
    
    // Make call to backend to finalize payment
    setTimeout(() => {
        fetch(`/api/orders/${currentPendingOrderId}/pay`, {
            method: 'POST'
        })
        .then(res => res.json())
        .then(order => {
            paymentConfirmBtn.innerHTML = '<i class="fa-solid fa-circle-check"></i> ยืนยันการชำระเงิน';
            paymentConfirmBtn.disabled = false;
            paymentModal.classList.remove('open');
            
            if (order.error) {
                alert(order.error);
                return;
            }
            
            // Show Success Notification Toast
            alert(`ชำระเงินสำเร็จ! คำสั่งซื้อของคุณคือหมายเลข: ${order.order_id}\nสถานะ: ชำระเงินเรียบร้อยแล้ว`);
            
            // Clear cart
            clearCart();
            
            // Redirect to Order History
            activeCategory = 'history';
            const navItems = document.querySelectorAll('.nav-item');
            navItems.forEach(btn => btn.classList.remove('active'));
            document.querySelector('.nav-item[data-tab="history"]').classList.add('active');
            handleTabSwitch('history');
            
            currentPendingOrderId = null;
        })
        .catch(err => {
            console.error('Error processing payment:', err);
            paymentConfirmBtn.innerHTML = '<i class="fa-solid fa-circle-check"></i> ยืนยันการชำระเงิน';
            paymentConfirmBtn.disabled = false;
            alert('เกิดข้อผิดพลาดในการยืนยันชำระเงิน');
        });
    }, 1200); // Small realistic delay
}

// ==========================================================================
// ORDER HISTORY VIEW RENDERING
// ==========================================================================
function fetchOrderHistory() {
    const tableBody = document.getElementById('history-table-body');
    tableBody.innerHTML = `
        <tr>
            <td colspan="7" class="text-center" style="padding: 40px 0;">
                <div class="spinner" style="margin: 0 auto 12px;"></div>
                กำลังโหลดประวัติคำสั่งซื้อ...
            </td>
        </tr>
    `;
    
    fetch('/api/orders')
        .then(res => res.json())
        .then(orders => {
            renderOrderHistoryTable(orders);
        })
        .catch(err => {
            console.error('Error fetching orders:', err);
            tableBody.innerHTML = `<tr><td colspan="7" class="text-center text-red">ไม่สามารถดึงข้อมูลประวัติได้</td></tr>`;
        });
}

function renderOrderHistoryTable(orders) {
    const tableBody = document.getElementById('history-table-body');
    
    if (orders.length === 0) {
        tableBody.innerHTML = `
            <tr>
                <td colspan="7" class="text-center text-muted" style="padding: 40px 0;">
                    <i class="fa-regular fa-folder-open" style="font-size: 38px; margin-bottom: 12px; opacity: 0.5;"></i>
                    <p>ยังไม่มีประวัติการทำรายการคำสั่งซื้อ</p>
                </td>
            </tr>
        `;
        return;
    }
    
    tableBody.innerHTML = '';
    orders.forEach(order => {
        const row = document.createElement('tr');
        
        // Status Badge Html
        let statusBadge = '<span class="status-badge pending"><i class="fa-solid fa-hourglass-half"></i> รอชำระเงิน</span>';
        if (order.status === 'paid') {
            statusBadge = '<span class="status-badge paid"><i class="fa-solid fa-circle-check"></i> ชำระเงินแล้ว</span>';
        } else if (order.status === 'cancelled') {
            statusBadge = '<span class="status-badge cancelled"><i class="fa-solid fa-circle-xmark"></i> ยกเลิกแล้ว</span>';
        }
        
        // Format Items list string
        const itemsStr = order.items.map(item => `${item.food_name} x${item.quantity}`).join(', ');
        
        // Setup Simulated Receipt print trigger
        const receiptBtnHtml = order.status === 'paid' 
            ? `<button class="action-btn" title="ดูใบเสร็จ" onclick="printMockReceipt(${JSON.stringify(order).replace(/"/g, '&quot;')})"><i class="fa-solid fa-file-invoice"></i></button>`
            : '<span class="text-muted">-</span>';
            
        row.innerHTML = `
            <td><strong>${order.order_id}</strong></td>
            <td>${order.created_at}</td>
            <td style="max-width: 250px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;" title="${itemsStr}">${itemsStr}</td>
            <td><i class="${getPaymentMethodIcon(order.payment_method)}"></i> ${order.payment_method}</td>
            <td><strong class="text-bold">${order.total_price.toFixed(2)} ฿</strong></td>
            <td>${statusBadge}</td>
            <td>${receiptBtnHtml}</td>
        `;
        tableBody.appendChild(row);
    });
}

function getPaymentMethodIcon(method) {
    if (method === 'PromptPay') return 'fa-solid fa-qrcode text-green';
    if (method === 'Credit Card') return 'fa-solid fa-credit-card text-orange';
    return 'fa-solid fa-money-bill-wave text-muted';
}

function printMockReceipt(order) {
    const itemsText = order.items.map(item => `  - ${item.food_name} (${item.quantity} จาน) : ${item.subtotal.toFixed(2)} ฿`).join('\n');
    const receiptTemplate = `
========================================
           ใบเสร็จรับเงิน (รสไทย)
========================================
หมายเลขสั่งซื้อ: ${order.order_id}
วันที่ทำรายการ: ${order.created_at}
การชำระเงิน: ${order.payment_method} (สำเร็จ)
สถานะ: ชำระเงินแล้ว
----------------------------------------
รายการสินค้า:
${itemsText}
----------------------------------------
ยอดรวมสุทธิ: ${order.total_price.toFixed(2)} บาท

     *** ขอบคุณที่ใช้บริการรสไทย ***
========================================
    `;
    alert(receiptTemplate);
}
