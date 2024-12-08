import os
from google.cloud import bigquery
from flask import Flask, jsonify, render_template
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "JSON_Key/g23ai2059-big-data-management-080dca6ac18e.json"

app = Flask(__name__)
client = bigquery.Client()

def get_order_summary():
    query = """
    SELECT OrderStatus, COUNT(*) AS count
    FROM `g23ai2059-big-data-management.food_delivery_dataset.Orders`
    GROUP BY OrderStatus
    """
    query_job = client.query(query)
    results = query_job.result()

    summary = {'Completed': 0, 'Pending': 0, 'Cancelled': 0}
    for row in results:
        summary[row['OrderStatus']] = row['count']

    return summary

@app.route('/orders_summary', methods=['GET'])
def orders_summary():
    summary = get_order_summary()
    #return jsonify(summary)
    return render_template('index.html', summary=summary)

app.run(debug=True)