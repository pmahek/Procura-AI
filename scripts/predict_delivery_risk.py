import sys
from pathlib import Path

import joblib
import pandas as pd

sys.path.append(str(Path(__file__).resolve().parent))

from database import get_connection


MODEL_PATH = Path(__file__).resolve().parent.parent / "models" / "delivery_risk_model.pkl"


def get_supplier_features(supplier_id, total_amount):
    connection = get_connection()
    cursor = connection.cursor()

    query = """
        SELECT
            s.supplier_id,
            s.years_in_business,
            s.category,
            s.location,

            COUNT(DISTINCT o.order_id) AS prior_order_count,

            COALESCE(SUM(o.total_amount), 0) AS prior_total_spend,

            COALESCE(AVG(o.total_amount), 0) AS prior_avg_order_value,

            COALESCE(
                AVG(
                    CASE
                        WHEN d.actual_delivery_date > d.promised_date
                        THEN 1.0
                        ELSE 0.0
                    END
                ),
                0
            ) AS prior_late_rate,

            COALESCE(
                AVG(
                    CASE
                        WHEN d.actual_delivery_date > d.promised_date
                        THEN d.actual_delivery_date - d.promised_date
                        ELSE 0
                    END
                ),
                0
            ) AS prior_avg_delivery_delay,

            COALESCE(
                AVG(
                    CASE
                        WHEN q.quantity_inspected > 0
                        THEN q.quantity_accepted::FLOAT / q.quantity_inspected
                        ELSE 0
                    END
                ),
                0
            ) AS prior_quality_acceptance_rate,

            COALESCE(
                AVG(
                    CASE
                        WHEN q.quantity_inspected > 0
                        THEN q.defective_quantity::FLOAT / q.quantity_inspected
                        ELSE 0
                    END
                ),
                0
            ) AS prior_defect_rate

        FROM suppliers s

        LEFT JOIN orders o
            ON s.supplier_id = o.supplier_id

        LEFT JOIN deliveries d
            ON o.order_id = d.order_id

        LEFT JOIN quality q
            ON o.order_id = q.order_id

        WHERE s.supplier_id = %s

        GROUP BY
            s.supplier_id,
            s.years_in_business,
            s.category,
            s.location;
    """

    cursor.execute(query, (supplier_id,))
    result = cursor.fetchone()

    cursor.close()
    connection.close()

    if result is None:
        raise ValueError(f"Supplier {supplier_id} was not found.")

    (
        supplier_id,
        years_in_business,
        category,
        location,
        prior_order_count,
        prior_total_spend,
        prior_avg_order_value,
        prior_late_rate,
        prior_avg_delivery_delay,
        prior_quality_acceptance_rate,
        prior_defect_rate,
    ) = result

    return {
        "total_amount": total_amount,
        "years_in_business": years_in_business,
        "prior_order_count": prior_order_count,
        "prior_total_spend": float(prior_total_spend),
        "prior_avg_order_value": float(prior_avg_order_value),
        "prior_late_rate": float(prior_late_rate),
        "prior_avg_delivery_delay": float(prior_avg_delivery_delay),
        "prior_quality_acceptance_rate": float(prior_quality_acceptance_rate),
        "prior_defect_rate": float(prior_defect_rate),
        "category": category,
        "location": location,
    }


def predict_delivery_risk(supplier_id, total_amount):
    model = joblib.load(MODEL_PATH)

    features = get_supplier_features(
        supplier_id=supplier_id,
        total_amount=total_amount,
    )

    input_data = pd.DataFrame([features])

    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(input_data)[0, 1]

    risk = "HIGH" if prediction == 1 else "LOW"

    return features, risk, probability


if __name__ == "__main__":

    supplier_id = "SUP001"
    total_amount = 85000

    features, risk, probability = predict_delivery_risk(
        supplier_id=supplier_id,
        total_amount=total_amount,
    )

    print("=" * 60)
    print("PROCURA AI — DATABASE-BACKED DELIVERY RISK")
    print("=" * 60)

    print("\nSupplier:")
    print(supplier_id)

    print("\nHistorical features retrieved from PostgreSQL:")

    for feature, value in features.items():
        print(f"{feature}: {value}")

    print("\nPredicted delivery risk:")
    print(risk)

    print("\nProbability of late delivery:")
    print(f"{probability:.2%}")

    print("\n" + "=" * 60)