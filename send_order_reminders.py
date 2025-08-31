#!/usr/bin/env python3
import sys
import logging
from datetime import datetime, timedelta
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

# Configure logging
LOG_FILE = "/tmp/order_reminders_log.txt"
logging.basicConfig(filename=LOG_FILE, level=logging.INFO)

# GraphQL endpoint
transport = RequestsHTTPTransport(
    url="http://localhost:8000/graphql",
    verify=True,
    retries=3,
)

client = Client(transport=transport, fetch_schema_from_transport=True)

# Calculate date range (last 7 days)
today = datetime.today().date()
seven_days_ago = today - timedelta(days=7)

query = gql(
    """
    query GetRecentOrders($startDate: Date!, $endDate: Date!) {
        orders(orderDate_Gte: $startDate, orderDate_Lte: $endDate) {
            id
            customer {
                email
            }
        }
    }
    """
)

params = {
    "startDate": seven_days_ago.isoformat(),
    "endDate": today.isoformat()
}

try:
    result = client.execute(query, variable_values=params)
    orders = result.get("orders", [])

    for order in orders:
        order_id = order["id"]
        customer_email = order["customer"]["email"]
        log_entry = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Order {order_id} reminder sent to {customer_email}"
        logging.info(log_entry)

    print("Order reminders processed!")

except Exception as e:
    logging.error(f"Error processing order reminders: {e}")
    sys.exit(1)
