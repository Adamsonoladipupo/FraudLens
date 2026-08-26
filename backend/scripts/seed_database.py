import random
from datetime import datetime, timedelta

from app.db.cognodb import cognodb


random.seed(42)

CUSTOMER_COUNT = 50
ACCOUNT_COUNT = 75
TRANSACTION_COUNT = 200
MERCHANT_COUNT = 20
DEVICE_COUNT = 30
IP_COUNT = 40


def generate_customers():
    first_names = [
        "James", "Sarah", "Michael", "David", "Daniel",
        "Grace", "John", "Emily", "Robert", "Sophia",
        "Samuel", "Olivia", "Benjamin", "Aisha", "Daniel",
    ]

    last_names = [
        "Smith", "Johnson", "Williams", "Brown", "Jones",
        "Miller", "Davis", "Wilson", "Anderson", "Taylor",
        "Thomas", "Moore", "Jackson", "Martin", "Lee",
    ]

    customers = []

    for i in range(1, CUSTOMER_COUNT + 1):
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)

        customers.append({
            "id": f"CUST-{i:04d}",
            "full_name": f"{first_name} {last_name}",
            "email": f"customer{i}@example.com",
            "phone": f"+234801{random.randint(1000000, 9999999)}",
            "status": "ACTIVE",
        })

    return customers


def generate_accounts():
    account_types = ["CHECKING", "SAVINGS", "BUSINESS"]

    accounts = []

    for i in range(1, ACCOUNT_COUNT + 1):
        accounts.append({
            "id": f"ACC-{i:04d}",
            "account_number": f"10{random.randint(10000000, 99999999)}",
            "account_type": random.choice(account_types),
            "status": "ACTIVE",
            "risk_level": random.choices(
                ["LOW", "MEDIUM", "HIGH"],
                weights=[70, 25, 5],
            )[0],
        })

    return accounts


def generate_merchants():
    merchant_names = [
        "Amazon",
        "Walmart",
        "Apple Store",
        "Netflix",
        "Uber",
        "Airbnb",
        "Steam",
        "Best Buy",
        "Target",
        "Shopify Store",
        "Jumia",
        "Konga",
        "MTN",
        "Airtel",
        "Flutterwave",
        "Paystack",
        "GameStop",
        "eBay",
        "AliExpress",
        "Microsoft Store",
    ]

    merchants = []

    for i in range(1, MERCHANT_COUNT + 1):
        merchants.append({
            "id": f"MER-{i:04d}",
            "name": merchant_names[i - 1],
            "category": random.choice([
                "RETAIL",
                "E_COMMERCE",
                "TRAVEL",
                "ENTERTAINMENT",
                "TELECOM",
                "DIGITAL_SERVICES",
            ]),
            "country": random.choice([
                "NG",
                "US",
                "GB",
                "CA",
            ]),
            "status": "ACTIVE",
        })

    return merchants


def generate_devices():
    devices = []

    for i in range(1, DEVICE_COUNT + 1):
        devices.append({
            "id": f"DEV-{i:04d}",
            "device_fingerprint": f"device-fingerprint-{i:04d}",
            "device_type": random.choice([
                "MOBILE",
                "DESKTOP",
                "TABLET",
            ]),
        })

    return devices


def generate_ips():
    ips = []

    for i in range(1, IP_COUNT + 1):
        ips.append({
            "id": f"IP-{i:04d}",
            "address": f"192.168.{i // 255}.{i % 255}",
            "country": random.choice([
                "NG",
                "US",
                "GB",
                "CA",
            ]),
        })

    return ips


def create_constraints():
    queries = [
        """
        CREATE CONSTRAINT customer_id_unique IF NOT EXISTS
        FOR (c:Customer)
        REQUIRE c.id IS UNIQUE
        """,
        """
        CREATE CONSTRAINT account_id_unique IF NOT EXISTS
        FOR (a:Account)
        REQUIRE a.id IS UNIQUE
        """,
        """
        CREATE CONSTRAINT transaction_id_unique IF NOT EXISTS
        FOR (t:Transaction)
        REQUIRE t.id IS UNIQUE
        """,
        """
        CREATE CONSTRAINT merchant_id_unique IF NOT EXISTS
        FOR (m:Merchant)
        REQUIRE m.id IS UNIQUE
        """,
        """
        CREATE CONSTRAINT device_id_unique IF NOT EXISTS
        FOR (d:Device)
        REQUIRE d.id IS UNIQUE
        """,
        """
        CREATE CONSTRAINT ip_id_unique IF NOT EXISTS
        FOR (ip:IPAddress)
        REQUIRE ip.id IS UNIQUE
        """,
    ]

    for query in queries:
        cognodb.execute_query(query)


def seed_customers(customers):
    query = """
    UNWIND $customers AS customer
    MERGE (c:Customer {id: customer.id})
    SET
        c.fullName = customer.full_name,
        c.email = customer.email,
        c.phone = customer.phone,
        c.status = customer.status
    """

    cognodb.execute_query(query, {"customers": customers})


def seed_accounts(accounts):
    query = """
    UNWIND $accounts AS account
    MERGE (a:Account {id: account.id})
    SET
        a.accountNumber = account.account_number,
        a.accountType = account.account_type,
        a.status = account.status,
        a.riskLevel = account.risk_level
    """

    cognodb.execute_query(query, {"accounts": accounts})


def seed_merchants(merchants):
    query = """
    UNWIND $merchants AS merchant
    MERGE (m:Merchant {id: merchant.id})
    SET
        m.name = merchant.name,
        m.category = merchant.category,
        m.country = merchant.country,
        m.status = merchant.status
    """

    cognodb.execute_query(query, {"merchants": merchants})


def seed_devices(devices):
    query = """
    UNWIND $devices AS device
    MERGE (d:Device {id: device.id})
    SET
        d.deviceFingerprint = device.device_fingerprint,
        d.deviceType = device.device_type
    """

    cognodb.execute_query(query, {"devices": devices})


def seed_ips(ips):
    query = """
    UNWIND $ips AS ip
    MERGE (i:IPAddress {id: ip.id})
    SET
        i.address = ip.address,
        i.country = ip.country
    """

    cognodb.execute_query(query, {"ips": ips})


def connect_customers_to_accounts():
    query = """
    MATCH (c:Customer)
    WITH collect(c) AS customers

    MATCH (a:Account)
    WITH customers, collect(a) AS accounts

    UNWIND accounts AS account

    WITH
        account,
        customers[
            toInteger(
                substring(account.id, 4)
            ) % size(customers)
        ] AS customer

    MERGE (customer)-[:OWNS]->(account)
    """

    cognodb.execute_query(query)


def connect_accounts_to_devices():
    query = """
    MATCH (a:Account)
    WITH collect(a) AS accounts

    MATCH (d:Device)
    WITH accounts, collect(d) AS devices

    UNWIND accounts AS account

    WITH
        account,
        devices[
            toInteger(
                substring(account.id, 4)
            ) % size(devices)
        ] AS device

    MERGE (account)-[:USES_DEVICE]->(device)
    """

    cognodb.execute_query(query)


def connect_accounts_to_ips():
    query = """
    MATCH (a:Account)
    WITH collect(a) AS accounts

    MATCH (ip:IPAddress)
    WITH accounts, collect(ip) AS ips

    UNWIND accounts AS account

    WITH
        account,
        ips[
            toInteger(
                substring(account.id, 4)
            ) % size(ips)
        ] AS ip

    MERGE (account)-[:USES_IP]->(ip)
    """

    cognodb.execute_query(query)


def create_suspicious_device_relationships():
    """
    Deliberately connect multiple accounts to the same devices.
    These relationships will be useful for fraud investigation.
    """

    suspicious_pairs = [
        ("ACC-0001", "ACC-0002", "DEV-0001"),
        ("ACC-0002", "ACC-0007", "DEV-0001"),
        ("ACC-0010", "ACC-0011", "DEV-0003"),
        ("ACC-0011", "ACC-0015", "DEV-0003"),
        ("ACC-0020", "ACC-0021", "DEV-0005"),
        ("ACC-0021", "ACC-0024", "DEV-0005"),
    ]

    query = """
    UNWIND $pairs AS pair

    MATCH (a1:Account {id: pair.account1})
    MATCH (a2:Account {id: pair.account2})
    MATCH (d:Device {id: pair.device})

    MERGE (a1)-[:USES_DEVICE]->(d)
    MERGE (a2)-[:USES_DEVICE]->(d)
    """

    pairs = [
        {
            "account1": a1,
            "account2": a2,
            "device": device,
        }
        for a1, a2, device in suspicious_pairs
    ]

    cognodb.execute_query(query, {"pairs": pairs})


def create_suspicious_ip_relationships():
    suspicious_pairs = [
        ("ACC-0001", "ACC-0004", "IP-0001"),
        ("ACC-0004", "ACC-0008", "IP-0001"),
        ("ACC-0010", "ACC-0012", "IP-0005"),
        ("ACC-0012", "ACC-0018", "IP-0005"),
        ("ACC-0020", "ACC-0025", "IP-0010"),
    ]

    query = """
    UNWIND $pairs AS pair

    MATCH (a1:Account {id: pair.account1})
    MATCH (a2:Account {id: pair.account2})
    MATCH (ip:IPAddress {id: pair.ip})

    MERGE (a1)-[:USES_IP]->(ip)
    MERGE (a2)-[:USES_IP]->(ip)
    """

    pairs = [
        {
            "account1": a1,
            "account2": a2,
            "ip": ip,
        }
        for a1, a2, ip in suspicious_pairs
    ]

    cognodb.execute_query(query, {"pairs": pairs})


def generate_transactions(accounts, merchants):
    transactions = []

    start_date = datetime.utcnow() - timedelta(days=30)

    for i in range(1, TRANSACTION_COUNT + 1):
        account = random.choice(accounts)
        merchant = random.choice(merchants)

        amount = round(
            random.uniform(20, 5000),
            2,
        )

        risk_score = random.randint(5, 45)

        transaction_type = random.choice([
            "PURCHASE",
            "TRANSFER",
            "WITHDRAWAL",
            "PAYMENT",
        ])

        transactions.append({
            "id": f"TXN-{i:04d}",
            "amount": amount,
            "currency": "USD",
            "timestamp": start_date + timedelta(
                minutes=random.randint(0, 43200)
            ),
            "transaction_type": transaction_type,
            "status": "COMPLETED",
            "risk_score": risk_score,
            "account_id": account["id"],
            "merchant_id": merchant["id"],
        })

    return transactions


def seed_transactions(transactions):
    query = """
    UNWIND $transactions AS tx

    MATCH (a:Account {id: tx.account_id})
    MATCH (m:Merchant {id: tx.merchant_id})

    MERGE (t:Transaction {id: tx.id})

    SET
        t.amount = tx.amount,
        t.currency = tx.currency,
        t.timestamp = tx.timestamp,
        t.transactionType = tx.transaction_type,
        t.status = tx.status,
        t.riskScore = tx.risk_score

    MERGE (a)-[:MAKES]->(t)
    MERGE (t)-[:TO]->(m)
    """

    cognodb.execute_query(
        query,
        {"transactions": transactions},
    )


def create_suspicious_transactions():
    """
    Create transactions with deliberately high risk scores.
    """

    query = """
    MATCH (t:Transaction)
    WHERE t.id IN [
        'TXN-0001',
        'TXN-0002',
        'TXN-0003',
        'TXN-0010',
        'TXN-0020',
        'TXN-0030',
        'TXN-0040',
        'TXN-0050',
        'TXN-0060',
        'TXN-0070',
        'TXN-0080',
        'TXN-0090'
    ]

    SET t.riskScore = 80
    """

    cognodb.execute_query(query)


def create_transfer_relationships():
    """
    Create account-to-account transfer relationships.
    """

    query = """
    MATCH (a1:Account)
    WITH collect(a1) AS accounts

    UNWIND range(0, 20) AS i

    WITH
        accounts[i % size(accounts)] AS source,
        accounts[(i + 1) % size(accounts)] AS target

    MERGE (source)-[:TRANSFERRED_TO]->(target)
    """

    cognodb.execute_query(query)


def print_statistics():
    queries = {
        "customers": """
            MATCH (c:Customer)
            RETURN count(c) AS count
        """,
        "accounts": """
            MATCH (a:Account)
            RETURN count(a) AS count
        """,
        "transactions": """
            MATCH (t:Transaction)
            RETURN count(t) AS count
        """,
        "merchants": """
            MATCH (m:Merchant)
            RETURN count(m) AS count
        """,
        "devices": """
            MATCH (d:Device)
            RETURN count(d) AS count
        """,
        "ip_addresses": """
            MATCH (ip:IPAddress)
            RETURN count(ip) AS count
        """,
    }

    print("\nFraudLens Graph Statistics")
    print("-" * 30)

    for name, query in queries.items():
        result = cognodb.execute_query(query)

        count = result[0]["count"]

        print(f"{name}: {count}")


def main():
    print("Connecting to CognoDB...")

    cognodb.connect()

    try:
        cognodb.verify_connection()

        print("Connected successfully.")

        print("Creating constraints...")
        create_constraints()

        print("Generating data...")

        customers = generate_customers()
        accounts = generate_accounts()
        merchants = generate_merchants()
        devices = generate_devices()
        ips = generate_ips()

        print("Seeding customers...")
        seed_customers(customers)

        print("Seeding accounts...")
        seed_accounts(accounts)

        print("Seeding merchants...")
        seed_merchants(merchants)

        print("Seeding devices...")
        seed_devices(devices)

        print("Seeding IP addresses...")
        seed_ips(ips)

        print("Creating customer-account relationships...")
        connect_customers_to_accounts()

        print("Creating account-device relationships...")
        connect_accounts_to_devices()

        print("Creating account-IP relationships...")
        connect_accounts_to_ips()

        print("Creating suspicious device relationships...")
        create_suspicious_device_relationships()

        print("Creating suspicious IP relationships...")
        create_suspicious_ip_relationships()

        print("Generating transactions...")

        transactions = generate_transactions(
            accounts,
            merchants,
        )

        print("Seeding transactions...")
        seed_transactions(transactions)

        print("Creating suspicious transactions...")
        create_suspicious_transactions()

        print("Creating account transfer relationships...")
        create_transfer_relationships()

        print_statistics()

        print("\nDatabase seeding completed successfully.")

    finally:
        cognodb.close()


if __name__ == "__main__":
    main()