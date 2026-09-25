from database import get_connection


def get_supplier_history(supplier_id):
    connection = get_connection()
    cursor = connection.cursor()

    query = """
        SELECT
            s.supplier_id,
            s.supplier_name,
            COUNT(DISTINCT o.order_id) AS total_orders,
            COALESCE(ROUND(AVG(o.total_amount), 2), 0) AS avg_order_value,
            COALESCE(
                ROUND(
                    AVG(
                        CASE
                            WHEN d.actual_delivery_date > d.promised_date
                            THEN 1.0
                            ELSE 0.0
                        END
                    ),
                    3
                ),
                0
            ) AS late_delivery_rate
        FROM suppliers s
        LEFT JOIN orders o
            ON s.supplier_id = o.supplier_id
        LEFT JOIN deliveries d
            ON o.order_id = d.order_id
        WHERE s.supplier_id = %s
        GROUP BY s.supplier_id, s.supplier_name;
    """

    cursor.execute(query, (supplier_id,))

    result = cursor.fetchone()

    cursor.close()
    connection.close()

    return result


supplier = get_supplier_history("SUP001")

print("Supplier history:")
print(supplier)