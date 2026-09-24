import pytest
from datetime import datetime, timedelta
from support_tool import analyze_transaction

def test_analyze_transaction_processing_anomaly():
    # Setup mock data for a stuck transaction
    tx_data = {
        'id': 1, 'transaction_ref': 'TXN123', 'amount': 100.0,
        'status': 'PROCESSING', 
        'created_at': datetime.now() - timedelta(minutes=20), # Older than 15 min
        'completed_at': None, 'failure_code': None,
        'customer_name': 'Test', 'customer_ref': 'C1',
        'callbacks': []
    }
    
    result = analyze_transaction(tx_data)
    
    assert "Transaction stuck in PROCESSING for over 15 minutes." in result['anomalies']
    assert "deadlocks" in result['next_action']

def test_analyze_transaction_success_no_callback():
    tx_data = {
        'id': 2, 'transaction_ref': 'TXN456', 'amount': 50.0,
        'status': 'SUCCESS', 
        'created_at': datetime.now() - timedelta(minutes=5),
        'completed_at': datetime.now() - timedelta(minutes=4), 
        'failure_code': None,
        'customer_name': 'Test', 'customer_ref': 'C1',
        'callbacks': []
    }
    
    result = analyze_transaction(tx_data)
    
    assert "Transaction successful but no callback attempts recorded." in result['anomalies']

def test_analyze_transaction_success_with_failed_callbacks():
    tx_data = {
        'id': 3, 'transaction_ref': 'TXN789', 'amount': 75.0,
        'status': 'SUCCESS', 
        'created_at': datetime.now(),
        'completed_at': datetime.now(), 
        'failure_code': None,
        'customer_name': 'Test', 'customer_ref': 'C1',
        'callbacks': [
            {'attempt_no': 1, 'http_status': 500, 'callback_status': 'FAILED', 'attempted_at': datetime.now()}
        ]
    }
    
    result = analyze_transaction(tx_data)
    
    assert "All callback attempts failed." in result['anomalies']

def test_analyze_transaction_perfect():
    tx_data = {
        'id': 4, 'transaction_ref': 'TXN000', 'amount': 10.0,
        'status': 'SUCCESS', 
        'created_at': datetime.now(),
        'completed_at': datetime.now(), 
        'failure_code': None,
        'customer_name': 'Test', 'customer_ref': 'C1',
        'callbacks': [
            {'attempt_no': 1, 'http_status': 200, 'callback_status': 'SUCCESS', 'attempted_at': datetime.now()}
        ]
    }
    
    result = analyze_transaction(tx_data)
    
    assert len(result['anomalies']) == 0
    assert result['next_action'] == "None"
