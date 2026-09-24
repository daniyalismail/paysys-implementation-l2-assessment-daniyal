import pytest
from playwright.sync_api import Page, expect

# Ensure Playwright is installed: pip install playwright pytest-playwright && playwright install

BASE_URL = "http://localhost:8080"

def test_login_and_search_transaction(page: Page):
    # 1. Open/login to the application
    page.goto(f"{BASE_URL}/login")
    page.fill('input[name="username"]', 'admin')
    page.fill('input[name="password"]', 'password123')
    page.click('button[type="submit"]')
    
    # Assert login success
    expect(page.locator('text=Welcome, admin')).to_be_visible()

    # 2. Search for a transaction
    page.goto(f"{BASE_URL}/transactions")
    page.fill('input[id="search-box"]', 'TXN000123')
    page.click('button[id="search-btn"]')
    
    # Assert transaction appears
    expect(page.locator('table#tx-results >> text=TXN000123')).to_be_visible()

def test_create_payment_success(page: Page):
    # 3. Create/submit a test payment
    page.goto(f"{BASE_URL}/payments/new")
    page.fill('input[name="customer_id"]', 'CUST001')
    page.fill('input[name="amount"]', '250.00')
    page.click('button#submit-payment')
    
    # 4. Validate a successful result
    expect(page.locator('.alert-success')).to_contain_text('Payment created successfully')
    expect(page.locator('text=$250.00')).to_be_visible()

def test_create_payment_invalid_amount(page: Page):
    # 5. Validate at least one negative/error scenario
    page.goto(f"{BASE_URL}/payments/new")
    page.fill('input[name="customer_id"]', 'CUST001')
    page.fill('input[name="amount"]', '-50.00') # Invalid
    page.click('button#submit-payment')
    
    # Validate error message
    expect(page.locator('.alert-danger')).to_contain_text('Amount must be greater than zero')
