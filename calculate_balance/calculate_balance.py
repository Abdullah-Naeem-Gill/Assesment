def calculate_balances(transactions):

    balances = {}

    for transaction in transactions:
        user_id = transaction["user_id"]
        amount = transaction["amount"]
        trans_type = transaction["type"]

        if user_id not in balances:
            balances[user_id] = 0
        
        if trans_type == "credit":
            balances[user_id] += amount
        
        else:
            balances[user_id] -= amount
    
    return balances

if __name__ == "__main__":
    transactions = [
        {"user_id": 1, "amount": 100, "type": "credit"},
        {"user_id": 2, "amount": 50, "type": "debit"},
        {"user_id": 1, "amount": 30, "type": "debit"},
        {"user_id": 2, "amount": 200, "type": "credit"},
    ]

    result = calculate_balances(transactions)
    print(f"Result: {result}")

