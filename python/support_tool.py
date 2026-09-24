import argparse
import os
import sys
import json
import logging
from datetime import datetime
try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
except ImportError:
    psycopg2 = None

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("support_tool")

class Config:
    DB_HOST = os.environ.get("DB_HOST", "localhost")
    DB_PORT = os.environ.get("DB_PORT", "5432")
    DB_NAME = os.environ.get("DB_NAME", "minipay")
    DB_USER = os.environ.get("DB_USER", "postgres")
    DB_PASSWORD = os.environ.get("DB_PASSWORD", "postgres")

def get_db_connection():
    if not psycopg2:
        logger.error("psycopg2 is not installed. Please install requirements.")
        sys.exit(1)
    try:
        conn = psycopg2.connect(
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            dbname=Config.DB_NAME,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            connect_timeout=5
        )
        return conn
    except psycopg2.OperationalError as e:
        logger.error(f"Database connection failed: {e}")
        return None

def fetch_transaction_data(conn, tx_ref):
    query = """
    SELECT 
        t.id, t.transaction_ref, t.amount, t.status, 
        t.created_at, t.completed_at, t.failure_code,
        c.name as customer_name, c.customer_ref
    FROM transactions t
    JOIN customers c ON t.customer_id = c.id
    WHERE t.transaction_ref = %s
    """
    callback_query = """
    SELECT attempt_no, http_status, callback_status, attempted_at
    FROM callbacks
    WHERE transaction_id = %s
    ORDER BY attempt_no ASC
    """
    
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(query, (tx_ref,))
        tx = cur.fetchone()
        
        if not tx:
            return None
            
        cur.execute(callback_query, (tx['id'],))
        callbacks = cur.fetchall()
        
        tx['callbacks'] = callbacks
        return dict(tx)

def analyze_transaction(tx_data):
    anomalies = []
    next_action = "None"
    
    if tx_data['status'] == 'PROCESSING':
        time_diff = datetime.now() - tx_data['created_at']
        if time_diff.total_seconds() > 900: # 15 minutes
            anomalies.append("Transaction stuck in PROCESSING for over 15 minutes.")
            next_action = "Check background worker queue and API logs for deadlocks."
    elif tx_data['status'] == 'FAILED':
        anomalies.append(f"Transaction failed with code: {tx_data.get('failure_code')}")
        next_action = "Review failure code documentation and contact customer if necessary."
        
    callbacks = tx_data.get('callbacks', [])
    if tx_data['status'] == 'SUCCESS':
        if not callbacks:
            anomalies.append("Transaction successful but no callback attempts recorded.")
            next_action = "Check callback dispatcher service."
        else:
            success_cbs = [cb for cb in callbacks if cb['callback_status'] == 'SUCCESS']
            if not success_cbs:
                anomalies.append("All callback attempts failed.")
                next_action = "Verify customer endpoint and trigger manual callback retry."
                
    tx_data['anomalies'] = anomalies
    tx_data['next_action'] = next_action
    
    # Format datetime objects for JSON serialization
    for key in ['created_at', 'completed_at']:
        if tx_data.get(key):
            tx_data[key] = tx_data[key].isoformat()
            
    for cb in tx_data['callbacks']:
        if cb.get('attempted_at'):
            cb['attempted_at'] = cb['attempted_at'].isoformat()
            
    return tx_data

def print_text_report(tx_data):
    print("="*40)
    print("      TRANSACTION DIAGNOSTIC REPORT")
    print("="*40)
    print(f"Reference : {tx_data['transaction_ref']}")
    print(f"Customer  : {tx_data['customer_name']} ({tx_data['customer_ref']})")
    print(f"Amount    : {tx_data['amount']}")
    print(f"Status    : {tx_data['status']}")
    if tx_data.get('failure_code'):
        print(f"Failure   : {tx_data['failure_code']}")
    print(f"Created   : {tx_data['created_at']}")
    print(f"Completed : {tx_data['completed_at']}")
    
    print("\n--- Callbacks ---")
    if not tx_data['callbacks']:
        print("No callbacks recorded.")
    for cb in tx_data['callbacks']:
        print(f"Attempt {cb['attempt_no']}: {cb['callback_status']} (HTTP {cb['http_status']}) at {cb['attempted_at']}")
        
    print("\n--- Analysis ---")
    if tx_data['anomalies']:
        for anomaly in tx_data['anomalies']:
            print(f"[!] ANOMALY: {anomaly}")
    else:
        print("[+] No anomalies detected.")
        
    print(f"\n=> NEXT ACTION: {tx_data['next_action']}")
    print("="*40)

def main():
    parser = argparse.ArgumentParser(description="MiniPay L2 Support Utility")
    parser.add_argument("--transaction", help="Transaction reference to inspect")
    parser.add_argument("--json", action="store_true", help="Output in JSON format")
    args = parser.parse_args()

    if not args.transaction:
        parser.print_help()
        sys.exit(1)

    if not args.json:
        logger.info(f"Connecting to database at {Config.DB_HOST}...")
        
    conn = get_db_connection()
    if not conn:
        # For demonstration purposes in a disconnected environment, use mock data
        logger.warning("Using mock data as DB is unreachable.")
        tx_data = {
            'id': 1, 'transaction_ref': args.transaction, 'amount': 150.00,
            'status': 'PROCESSING', 'created_at': datetime(2023, 1, 1, 10, 0, 0),
            'completed_at': None, 'failure_code': None,
            'customer_name': 'Test User', 'customer_ref': 'CUST123',
            'callbacks': []
        }
    else:
        try:
            tx_data = fetch_transaction_data(conn, args.transaction)
            conn.close()
        except Exception as e:
            logger.error(f"Error fetching data: {e}")
            sys.exit(1)

    if not tx_data:
        logger.error(f"Transaction {args.transaction} not found.")
        sys.exit(2)

    analyzed_data = analyze_transaction(tx_data)

    if args.json:
        print(json.dumps(analyzed_data, indent=2))
    else:
        print_text_report(analyzed_data)

if __name__ == "__main__":
    main()
