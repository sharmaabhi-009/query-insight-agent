import mysql.connector
from mysql.connector import Error

# ===========================
# MySQL Configuration
# ===========================
MYSQL_CONFIG = {
    "host": "localhost",
    "user": "trade",
    "password": "trade",
    "database": "trade_db",
    "port": 3306,
}

# ===========================
# Database Connection Function
# ===========================
def get_db_connection():
    """
    Creates and returns a MySQL database connection.
    Remember to close the connection after use.
    """
    try:
        connection = mysql.connector.connect(**MYSQL_CONFIG)
        if connection.is_connected():
            print("✅ Connected to MySQL")
            return connection
    except Error as e:
        print(f"❌ Error connecting to MySQL: {e}")
        return None



