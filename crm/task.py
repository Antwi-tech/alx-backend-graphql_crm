from celery import shared_task
from datetime import datetime
import requests

@shared_task
def generate_crm_report():
    query = """
    query {
        totalCustomers
        totalOrders
        totalRevenue
    }
    """

    try:
        response = requests.post(
            "http://localhost:8000/graphql",
            json={"query": query},
            timeout=10
        )

        data = response.json().get("data", {})
        customers = data.get("totalCustomers", 0)
        orders = data.get("totalOrders", 0)
        revenue = data.get("totalRevenue", 0)

        log_entry = (
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - "
            f"Report: {customers} customers, {orders} orders, {revenue} revenue\n"
        )

        with open("/tmp/crm_report_log.txt", "a") as f:
            f.write(log_entry)

    except Exception as e:
        with open("/tmp/crm_report_log.txt", "a") as f:
            f.write(f"{datetime.now()} - ERROR: {e}\n")
