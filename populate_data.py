import os
import django
import random
from decimal import Decimal

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_cache.settings.local')
django.setup()

# Import models
from django.contrib.auth.models import User
from products.models import Product
from cart.models import Cart, CartItem
from order.models import Address, Order, OrderItem

def create_users(num_users=5):
    """Create sample users"""
    users = []
    for i in range(1, num_users + 1):
        username = f"user{i}"
        email = f"user{i}@example.com"
        password = "password123"
        user, created = User.objects.get_or_create(
            username=username,
            defaults={"email": email, "is_active": True}
        )
        if created:
            user.set_password(password)
            user.save()
            print(f"Created user: {username}")
        users.append(user)
    
    # Create a superuser if it doesn't exist
    superuser, created = User.objects.get_or_create(
        username="admin",
        defaults={
            "email": "admin@example.com",
            "is_staff": True,
            "is_superuser": True,
            "is_active": True
        }
    )
    if created:
        superuser.set_password("admin123")
        superuser.save()
        print("Created superuser: admin")
    
    return users

def create_products(num_products=10):
    """Create sample products"""
    products = []
    product_names = [
        "Smartphone", "Laptop", "Headphones", "Tablet", 
        "Smartwatch", "Camera", "Bluetooth Speaker", 
        "Gaming Console", "Wireless Earbuds", "Monitor",
        "Keyboard", "Mouse", "External Hard Drive", "USB Drive",
        "Power Bank", "Router", "Printer", "Desk Lamp"
    ]
    
    descriptions = [
        "Latest model with advanced features",
        "High performance and sleek design",
        "Premium quality with noise cancellation",
        "Lightweight and powerful",
        "Water resistant with health tracking",
        "High resolution with optical zoom",
        "Portable with excellent sound quality",
        "Next-gen gaming experience",
        "True wireless with long battery life",
        "Ultra-wide with high refresh rate"
    ]
    
    for i in range(1, num_products + 1):
        name = random.choice(product_names) + f" {i}"
        price = Decimal(random.randint(999, 9999))
        description = random.choice(descriptions)
        stock = random.randint(10, 100)
        
        product, created = Product.objects.get_or_create(
            name=name,
            defaults={
                "price_in_inr": price,
                "description": description,
                "stock": stock
            }
        )
        if created:
            print(f"Created product: {name}")
        products.append(product)
    
    return products

def create_addresses(users):
    """Create sample addresses for users"""
    addresses = []
    cities = ["Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai"]
    states = ["Maharashtra", "Delhi", "Karnataka", "Telangana", "Tamil Nadu"]
    
    for user in users:
        for i in range(1, random.randint(1, 3) + 1):
            is_default = (i == 1)
            city = random.choice(cities)
            state = random.choice(states)
            
            address, created = Address.objects.get_or_create(
                user=user,
                address_line_1=f"{random.randint(1, 999)} Main Street",
                city=city,
                defaults={
                    "address_line_2": f"Apt {random.randint(1, 100)}",
                    "state": state,
                    "postal_code": f"{random.randint(100000, 999999)}",
                    "country": "India",
                    "is_default": is_default
                }
            )
            if created:
                print(f"Created address for {user.username} in {city}")
            addresses.append(address)
    
    return addresses

def create_carts(users, products):
    """Create sample carts for users"""
    carts = []
    
    for user in users:
        cart, created = Cart.objects.get_or_create(
            user=user
        )
        if created:
            print(f"Created cart for {user.username}")
        
        # Add random products to cart
        num_items = random.randint(1, 5)
        for _ in range(num_items):
            product = random.choice(products)
            quantity = random.randint(1, 3)
            
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                defaults={"quantity": quantity}
            )
            if not created:
                cart_item.quantity = quantity
                cart_item.save()
            
            print(f"Added {quantity} x {product.name} to {user.username}'s cart")
        
        carts.append(cart)
    
    return carts

def create_orders(users, products, addresses):
    """Create sample orders for users"""
    orders = []
    statuses = ['PENDING', 'PROCESSING', 'SHIPPED', 'DELIVERED']
    
    for user in users:
        # Get user's addresses
        user_addresses = [addr for addr in addresses if addr.user == user]
        if not user_addresses:
            continue
        
        # Create 1-3 orders per user
        for _ in range(random.randint(1, 3)):
            shipping_address = random.choice(user_addresses)
            status = random.choice(statuses)
            
            order = Order.objects.create(
                user=user,
                shipping_address=shipping_address,
                status=status
            )
            print(f"Created order for {user.username} with status {status}")
            
            # Add random products to order
            num_items = random.randint(1, 5)
            total_amount = Decimal('0.00')
            
            for _ in range(num_items):
                product = random.choice(products)
                quantity = random.randint(1, 3)
                price = product.price_in_inr
                
                order_item = OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price_at_purchase=price
                )
                
                item_total = price * quantity
                total_amount += item_total
                print(f"Added {quantity} x {product.name} to order")
            
            # Update order total
            order.total_amount = total_amount
            order.save()
            print(f"Order total: ₹{total_amount}")
            
            orders.append(order)
    
    return orders

def run():
    """Run the population script"""
    print("Starting data population...")
    
    # Create sample data
    users = create_users()
    products = create_products()
    addresses = create_addresses(users)
    carts = create_carts(users, products)
    orders = create_orders(users, products, addresses)
    
    print("\nData population complete!")
    print(f"Created {len(users)} users")
    print(f"Created {len(products)} products")
    print(f"Created {len(addresses)} addresses")
    print(f"Created {len(carts)} carts")
    print(f"Created {len(orders)} orders")

if __name__ == "__main__":
    run()