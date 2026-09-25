from database import get_connection


connection = get_connection()

cursor = connection.cursor()

cursor.execute("SELECT COUNT(*) FROM suppliers;")

supplier_count = cursor.fetchone()[0]

print(f"Database connection successful.")
print(f"Suppliers in database: {supplier_count}")

cursor.close()
connection.close()