from faker import Faker
import csv
import random

fake = Faker()

# Generating Users
users = [{"user_id": i, "name": fake.name(), "email": fake.email()} for i in range(1, 101)]

# Generating Products
products = [{"product_id": i, "name": fake.word(), "price": round(random.uniform(10, 500), 2)} for i in range(1, 51)]

# Generating Orders
orders = [{"order_id": i, "user_id": random.choice(users)["user_id"], "date": fake.date()} for i in range(1, 201)]

# Generating OrderDetails
order_details = [{"order_detail_id": i, "order_id": random.choice(orders)["order_id"], "product_id": random.choice(products)["product_id"], "quantity": random.randint(1, 5)} for i in range(1, 501)]

# Generating Addresses
addresses = [{"address_id": i, "user_id": random.choice(users)["user_id"], "address": fake.address()} for i in range(1, 151)]

# Function to save data to CSV
def save_to_csv(data, filename, fieldnames):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

# Saving each table as a CSV file
save_to_csv(users, 'users.csv', ['user_id', 'name', 'email'])
save_to_csv(products, 'products.csv', ['product_id', 'name', 'price'])
save_to_csv(orders, 'orders.csv', ['order_id', 'user_id', 'date'])
save_to_csv(order_details, 'order_details.csv', ['order_detail_id', 'order_id', 'product_id', 'quantity'])
save_to_csv(addresses, 'addresses.csv', ['address_id', 'user_id', 'address'])

print("Data successfully saved to CSV files.")
