from database import get_connection


def compare_quotations(rfq_id):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        query = """
            SELECT
                q.quotation_id,
                q.supplier_id,
                s.supplier_name,
                q.payment_terms,
                qi.rfq_item_id,
                qi.unit_price,
                qi.quantity_quoted,
                qi.delivery_days,
                qi.warranty_months,
                qi.discount_percent,
                rfi.item_id,
                rfi.quantity AS quantity_requested
            FROM quotations q
            JOIN suppliers s
                ON q.supplier_id = s.supplier_id
            JOIN quotation_items qi
                ON q.quotation_id = qi.quotation_id
            JOIN rfq_items rfi
                ON qi.rfq_item_id = rfi.rfq_item_id
            WHERE q.rfq_id = %s
            ORDER BY q.quotation_id;
        """

        cursor.execute(query, (rfq_id,))
        rows = cursor.fetchall()

        results = []

        for row in rows:
            (
                quotation_id,
                supplier_id,
                supplier_name,
                payment_terms,
                rfq_item_id,
                unit_price,
                quantity_quoted,
                delivery_days,
                warranty_months,
                discount_percent,
                item_id,
                quantity_requested,
            ) = row

            gross_value = float(unit_price) * quantity_quoted

            discount_amount = (
                gross_value * float(discount_percent) / 100
            )

            net_value = gross_value - discount_amount

            results.append({
                "quotation_id": quotation_id,
                "supplier_id": supplier_id,
                "supplier_name": supplier_name,
                "item_id": item_id,
                "quantity_requested": quantity_requested,
                "quantity_quoted": quantity_quoted,
                "unit_price": float(unit_price),
                "gross_value": round(gross_value, 2),
                "discount_percent": float(discount_percent),
                "discount_amount": round(discount_amount, 2),
                "net_value": round(net_value, 2),
                "delivery_days": delivery_days,
                "warranty_months": warranty_months,
                "payment_terms": payment_terms,
            })

        return results

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":

    rfq_id = "RFQ0256"

    print("=" * 70)
    print("PROCURA AI — QUOTATION COMPARISON")
    print("=" * 70)
    print(f"RFQ: {rfq_id}")
    print()

    results = compare_quotations(rfq_id)

    if not results:
        print("No quotations found.")
    else:
        for result in results:
            print("-" * 70)

            for key, value in result.items():
                print(f"{key}: {value}")