# FraudLens

## Graph-Powered Retail Banking Fraud Investigation & Risk Explorer

<p align="center">
  <a href="https://fraudlens-ui.onrender.com">
    <img src="https://img.shields.io/badge/Live%20Frontend-FraudLens-blue?style=for-the-badge" alt="Live Frontend">
  </a>
  <a href="https://fraudlens-backend-api.onrender.com/docs">
    <img src="https://img.shields.io/badge/Interactive%20Swagger-API%20Docs-green?style=for-the-badge" alt="Interactive Swagger UI">
  </a>
  <a href="https://fraudlens-backend-api.onrender.com/health">
    <img src="https://img.shields.io/badge/API-Health-orange?style=for-the-badge" alt="API Health">
  </a>
</p>

<p align="center">
  <a href="https://fraudlens-ui.onrender.com">🚀 Launch FraudLens</a>
  &nbsp;&nbsp;|&nbsp;&nbsp;
  <a href="https://fraudlens-backend-api.onrender.com/docs">📚 Interactive Swagger UI</a>
  &nbsp;&nbsp;|&nbsp;&nbsp;
  <a href="https://fraudlens-backend-api.onrender.com/health">❤️ API Health</a>
</p>

FraudLens is a graph-powered fraud investigation application designed to help retail banking investigators identify and understand suspicious relationships between customers, accounts, transactions, devices, IP addresses, and merchants.

Instead of analyzing transactions independently, FraudLens uses **CognoDB Cloud**, a graph database, to model and explore relationships between financial entities. This allows investigators to discover multi-hop connections and patterns that may indicate coordinated fraudulent activity.

---

## Table of Contents

- [Overview](#overview)
- [Problem Statement](#problem-statement)
- [Solution](#solution)
- [Use Case](#use-case)
- [Why a Graph Database?](#why-a-graph-database)
- [How FraudLens Works](#how-fraudlens-works)
- [Key Fraud Scenarios](#key-fraud-scenarios)
- [Graph Data Model](#graph-data-model)
- [Risk Assessment](#risk-assessment)
- [System Architecture](#system-architecture)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [API](#api)
- [Graph Queries](#graph-queries)
- [Seed Data](#seed-data)
- [Getting Started](#getting-started)
- [CognoDB Cloud Setup](#cognodb-cloud-setup)
- [Environment Variables](#environment-variables)
- [Running the Backend](#running-the-backend)
- [Running the Frontend](#running-the-frontend)
- [Testing](#testing)
- [API Documentation](#api-documentation)
- [Deployment](#deployment)
- [User Workflow](#user-workflow)
- [Screenshots](#screenshots)
- [Design Decisions](#design-decisions)
- [Limitations](#limitations)
- [Future Improvements](#future-improvements)
- [Assessment Alignment](#assessment-alignment)
- [Security Considerations](#security-considerations)
- [License](#license)

---

# Overview

Fraud detection is often treated as a transaction-level problem:

> "Does this particular transaction look suspicious?"

However, financial fraud can involve multiple entities acting together.

For example, a transaction may appear normal when viewed independently:

```text
Account A
    |
    v
Transaction
    |
    v
Merchant X
```

When the surrounding relationships are examined, a different pattern may emerge:

```text
                         Device X
                       /    |    \
                      /     |     \
                     v      v      v
                Account A Account B Account C
                    |         |         |
                    v         v         v
                   TX1       TX2       TX3
```

The three accounts may appear unrelated in a traditional transaction list, but their shared device creates a potentially important relationship.

FraudLens is designed to make these relationships visible.

---

# Problem Statement

Retail banking institutions process large numbers of transactions involving customers, accounts, merchants, devices, IP addresses, and other entities.

Fraud investigators need to answer questions such as:

- Which accounts are connected to this suspicious transaction?
- Is the same device being used by multiple accounts?
- Are multiple accounts operating from the same IP address?
- Is this account connected to another suspicious account?
- Are several suspicious transactions connected to the same merchant?
- What other entities are connected to this transaction?
- How many relationship hops separate this transaction from previously flagged activity?

These questions are fundamentally about **relationships and connections**.

FraudLens addresses this by representing the banking environment as a graph.

---

# Solution

FraudLens provides a web-based investigation interface where a fraud investigator can:

1. View an overview of transaction and fraud activity.
2. Search for a transaction or account.
3. Investigate a suspicious transaction.
4. View its connected entities.
5. Identify risk indicators.
6. Explore multi-hop relationships.
7. Investigate suspicious account networks.
8. Understand why an entity received a particular risk level.

The application uses pre-seeded synthetic data containing both normal and deliberately constructed suspicious scenarios.

Therefore, a user does **not** need to manually create transactions before using the application.

---

# Use Case

## Primary Actor

### Fraud Investigator

The primary user of FraudLens is a fraud investigator working in a retail banking environment.

The investigator does not need to understand graph databases or Cypher.

They interact with the system through a normal web interface.

## Main Investigation Flow

```text
Search Transaction
       |
       v
Investigate Transaction
       |
       v
View Transaction Details
       |
       v
View Risk Indicators
       |
       v
Explore Connected Entities
       |
       v
Explore Suspicious Network
```

## Example Investigation

An investigator searches for:

```text
TXN-001024
```

FraudLens may discover:

```text
Transaction
     |
     v
Account A
     |
     v
Device X
     |
     +------> Account B
     |
     +------> Account C
     |
     +------> Account D
```

The application can then report:

```text
HIGH RISK

- Device X is associated with 4 accounts.
- Two connected accounts have previous risk indicators.
- Multiple transactions are connected to the same merchant.
```

The investigator can then explore the network to understand the relationships behind the risk assessment.

---

# Why a Graph Database?

FraudLens uses **CognoDB Cloud** as its graph database.

The primary reason is that fraud investigation is highly relationship-oriented.

A relational database can represent:

```text
customers
accounts
transactions
devices
merchants
ip_addresses
```

However, investigating relationships across several of these entities often requires multiple joins.

For example:

```text
Customer
   |
   +-- Account
         |
         +-- Transaction
               |
               +-- Device
                     |
                     +-- Other Transaction
                           |
                           +-- Other Account
```

The query becomes increasingly focused on reconstructing a network from relational tables.

A graph database represents those relationships directly.

For example:

```text
(Customer)-[:OWNS]->(Account)

(Account)-[:MAKES]->(Transaction)

(Transaction)-[:FROM_DEVICE]->(Device)

(Transaction)-[:FROM_IP]->(IPAddress)

(Transaction)-[:TO]->(Merchant)
```

The relationship itself becomes part of the data model.

## Multi-Hop Investigation

One of the important capabilities demonstrated by FraudLens is multi-hop traversal.

For example:

```text
Transaction
    |
    v
Account A
    |
    v
Device X
    |
    v
Account B
    |
    v
Transaction B
    |
    v
Merchant X
```

An investigator can start with one transaction and discover other related entities without manually querying each entity independently.

This is particularly useful for identifying:

- shared infrastructure;
- connected accounts;
- suspicious transaction clusters;
- potential fraud networks.

---

# How FraudLens Works

FraudLens has three primary layers:

```text
+-----------------------------+
|       React Frontend        |
|                             |
| Dashboard                   |
| Investigation UI            |
| Risk Analysis               |
| Graph Explorer              |
+-------------+---------------+
              |
              | REST / JSON
              |
+-------------v---------------+
|        FastAPI Backend      |
|                             |
| API Routes                  |
| Investigation Service       |
| Risk Service                |
| Graph Repository            |
+-------------+---------------+
              |
              | Bolt / openCypher
              |
+-------------v---------------+
|        CognoDB Cloud        |
|                             |
| Customer                    |
| Account                     |
| Transaction                 |
| Merchant                    |
| Device                      |
| IPAddress                   |
+-----------------------------+
```

---

# Key Fraud Scenarios

## 1. Normal Transaction

```text
Customer
    |
    v
Account
    |
    v
Transaction
    |
    v
Merchant
```

Expected risk:

```text
LOW
```

## 2. Shared Device

```text
Account A ----\
Account B -----+----> Device X
Account C ----/
```

Potential indicator:

```text
SHARED_DEVICE
```

## 3. Shared IP Address

```text
Account A ----\
Account B -----+----> IP X
Account C ----/
```

Potential indicator:

```text
SHARED_IP
```

## 4. Connected Suspicious Accounts

```text
Account A
    |
    v
Device X
    ^
    |
Account B
    |
    v
Transaction B
    |
    v
Merchant X
```

The relationship may increase the overall risk assessment.

## 5. Suspicious Network

```text
                   Device X
                  /   |   \
                 /    |    \
                v     v     v
           Account A Account B Account C
               |         |         |
               v         v         v
              TX1       TX2       TX3
                \         |        /
                 \        |       /
                  \       |      /
                   v      v     v
                     Merchant X
```

This is the primary graph-based demonstration in FraudLens.

---

# Graph Data Model

The core graph consists of six primary node types.

## Nodes

| Node | Description |
|---|---|
| `Customer` | Bank customer |
| `Account` | Customer bank account |
| `Transaction` | Financial transaction |
| `Merchant` | Merchant involved in a transaction |
| `Device` | Device used to perform activity |
| `IPAddress` | IP address associated with activity |

## Node Properties

### Customer

```text
Customer
├── id
├── fullName
├── email
├── phone
├── status
└── createdAt
```

### Account

```text
Account
├── id
├── accountNumber
├── accountType
├── status
├── openedAt
└── riskLevel
```

### Transaction

```text
Transaction
├── id
├── amount
├── currency
├── timestamp
├── transactionType
├── status
└── riskScore
```

### Merchant

```text
Merchant
├── id
├── name
├── category
├── country
└── status
```

### Device

```text
Device
├── id
├── deviceFingerprint
├── deviceType
├── firstSeenAt
└── lastSeenAt
```

### IPAddress

```text
IPAddress
├── id
├── address
├── country
├── firstSeenAt
└── lastSeenAt
```

## Relationships

| Relationship | Meaning |
|---|---|
| `OWNS` | Customer owns an account |
| `MAKES` | Account makes a transaction |
| `TO` | Transaction is directed to a merchant |
| `FROM_DEVICE` | Transaction originated from a device |
| `FROM_IP` | Transaction originated from an IP address |
| `USES` | Customer uses a device |
| `USES_IP` | Customer is associated with an IP address |
| `TRANSFERRED_TO` | Account transferred funds to another account |

## Graph Model

```text
                         +-------------+
                         |   Customer  |
                         +------+------+
                                |
                              OWNS
                                |
                                v
                         +-------------+
                         |   Account   |
                         +------+------+
                                |
                              MAKES
                                |
                                v
                       +----------------+
                       |  Transaction   |
                       +---+---------+--+
                           |         |
                          TO      FROM_DEVICE
                           |         |
                           v         v
                     +----------+ +----------+
                     | Merchant | |  Device  |
                     +----------+ +----------+

                       Transaction
                            |
                        FROM_IP
                            |
                            v
                     +-------------+
                     |  IPAddress  |
                     +-------------+
```

The graph can additionally contain:

```text
(Account)-[:TRANSFERRED_TO]->(Account)
```

which allows investigation of account-to-account transaction networks.

---

# Risk Assessment

FraudLens uses a deterministic, rule-based risk assessment for the MVP.

The purpose is to identify **risk indicators**, not to make a definitive claim that a transaction is fraudulent.

## Example Rules

| Risk Indicator | Score |
|---|---:|
| Device shared by 3 or more accounts | +30 |
| IP shared by 3 or more accounts | +20 |
| Connection to flagged account | +30 |
| Connection to suspicious merchant | +20 |

## Risk Levels

```text
0 - 29       LOW
30 - 59      MEDIUM
60 - 100     HIGH
```

## Example

```text
HIGH RISK — 80

Shared Device              +30
Shared IP                   +20
Connected Flagged Account   +30
--------------------------------
Total                       80
```

The UI exposes the indicators that contributed to the score so that investigators can understand the reasoning behind the result.

---

# System Architecture

```text
                         USER
                           |
                           v
                 +-------------------+
                 |   React Frontend  |
                 |                   |
                 | Dashboard         |
                 | Investigations    |
                 | Risk Analysis     |
                 | Graph Explorer    |
                 +---------+---------+
                           |
                       REST / JSON
                           |
                           v
                 +-------------------+
                 |   FastAPI Backend |
                 |                   |
                 | API Routes        |
                 | Services          |
                 | Risk Engine       |
                 | Graph Repository  |
                 +---------+---------+
                           |
                       Bolt Driver
                           |
                           v
                 +-------------------+
                 |   CognoDB Cloud   |
                 |                   |
                 | Graph Data        |
                 | openCypher        |
                 +-------------------+
```

---

# Technology Stack

## Frontend

- React
- JavaScript / TypeScript
- Vite
- Graph visualization library

## Backend

- Python
- FastAPI
- Pydantic
- Neo4j Python Driver
- pytest

## Database

- CognoDB Cloud
- openCypher
- Bolt

## Deployment

- Render
- CognoDB Cloud

---

# Project Structure

```text
fraudlens/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes/
│   │   ├── core/
│   │   ├── db/
│   │   ├── models/
│   │   ├── repositories/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── config.py
│   │   └── main.py
│   │
│   ├── tests/
│   │   ├── unit/
│   │   └── integration/
│   │
│   ├── scripts/
│   │   └── seed_database.py
│   │
│   ├── requirements.txt
│   ├── .env.example
│   └── README.md
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── hooks/
│   │   └── App.jsx
│   │
│   ├── public/
│   ├── package.json
│   └── vite.config.js
│
├── cypher/
│   ├── schema.cypher
│   └── investigation_queries.cypher
│
├── docs/
│   ├── use-case.puml
│   ├── class-diagram.puml
│   ├── graph-model.puml
│   └── screenshots/
│
├── .gitignore
└── README.md
```

---

# API

The backend exposes REST endpoints for the frontend.

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/health` | API/database health |
| `GET` | `/api/v1/dashboard/summary` | Dashboard statistics |
| `GET` | `/api/v1/transactions/{id}` | Retrieve transaction |
| `GET` | `/api/v1/accounts/{id}` | Retrieve account |
| `GET` | `/api/v1/investigations/transactions/{id}` | Investigate transaction |
| `GET` | `/api/v1/investigations/accounts/{id}` | Investigate account |
| `GET` | `/api/v1/investigations/{type}/{id}/network` | Explore entity network |

---

# Graph Queries

FraudLens uses parameterized openCypher queries.

## Find a Transaction

```cypher
MATCH (t:Transaction {id: $transaction_id})
RETURN t
```

## Find Transaction Context

```cypher
MATCH (c:Customer)-[:OWNS]->(a:Account)
      -[:MAKES]->(t:Transaction {id: $transaction_id})
      -[:TO]->(m:Merchant)
RETURN c, a, t, m
```

This retrieves:

```text
Customer
    |
    v
Account
    |
    v
Transaction
    |
    v
Merchant
```

## Find Accounts Sharing a Device

```cypher
MATCH (a1:Account)-[:MAKES]->(t1:Transaction)
      -[:FROM_DEVICE]->(d:Device)
      <-[:FROM_DEVICE]-(t2:Transaction)
      <-[:MAKES]-(a2:Account)
WHERE a1.id <> a2.id
RETURN a1, d, a2
```

This identifies accounts connected through the same device.

## Multi-Hop Investigation

```cypher
MATCH path =
  (t:Transaction {id: $transaction_id})
  -[:FROM_DEVICE|FROM_IP|TO*1..3]-
  (connected)
RETURN path
```

The production query will be constrained to the intended relationship types and entity paths to prevent irrelevant graph traversal.

---

# Parameterized Queries

FraudLens does not construct Cypher by concatenating user input.

The application uses parameters:

```python
query = """
MATCH (t:Transaction {id: $transaction_id})
RETURN t
"""

parameters = {
    "transaction_id": transaction_id
}
```

rather than:

```python
# Do not do this
query = f"""
MATCH (t:Transaction {{id: '{transaction_id}'}})
RETURN t
"""
```

This keeps database parameters separate from query structure and avoids treating user input as Cypher syntax.

---

# Seed Data

FraudLens uses synthetic data.

The seed script creates:

- Customers
- Accounts
- Transactions
- Merchants
- Devices
- IP addresses

It also creates deliberate patterns for investigation:

```text
Normal Transactions
        |
        +-- Shared Devices
        |
        +-- Shared IP Addresses
        |
        +-- Connected Accounts
        |
        +-- Suspicious Merchants
        |
        +-- Suspicious Networks
```

The purpose of the seed data is to provide realistic scenarios that demonstrate graph-based fraud investigation.

---

# Getting Started

## Prerequisites

Install the following:

- Python 3.11+
- Node.js 20+
- npm
- Git
- CognoDB Cloud account

---

# CognoDB Cloud Setup

1. Create a CognoDB Cloud account.
2. Create a free `c0` instance.
3. Select the desired region.
4. Copy the database connection URI.
5. Copy the generated database password.
6. Configure the backend environment variables.

The connection URI should follow the CognoDB format:

```text
bolt+s://<instance-id>.databases.cognodb.cloud
```

The database username is:

```text
cognodb
```

The password should be stored securely and must not be committed to source control.

---

# Environment Variables

Create:

```text
backend/.env
```

Example:

```env
COGNODB_URI=bolt+s://<instance-id>.databases.cognodb.cloud
COGNODB_USERNAME=cognodb
COGNODB_PASSWORD=your-password
```

The repository includes:

```text
backend/.env.example
```

Example:

```env
COGNODB_URI=
COGNODB_USERNAME=cognodb
COGNODB_PASSWORD=
```

Never commit:

```text
.env
```

to Git.

---

# Running the Backend

Navigate to the backend:

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv .venv
```

### Linux / macOS

```bash
source .venv/bin/activate
```

### Windows

```powershell
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Seed the Database

Run:

```bash
python scripts/seed_database.py
```

This creates the graph data required by the application.

---

# Start FastAPI

Run:

```bash
uvicorn app.main:app --reload
```

The backend will be available at:

```text
http://localhost:8000
```

---

# Running the Frontend

Open another terminal:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

The terminal will display the local frontend URL.

---

# API Documentation

FastAPI automatically exposes interactive API documentation.

Open:

```text
http://localhost:8000/docs
```

Alternative documentation:

```text
http://localhost:8000/redoc
```

These can be used to test the API before connecting the React frontend.

---

# Testing

FraudLens uses `pytest` for backend testing.

Run:

```bash
pytest
```

For more detailed output:

```bash
pytest -v
```

## Unit Tests

Unit tests cover:

- Risk score calculation
- Risk-level determination
- Risk indicator generation
- Investigation service behavior
- Error handling

Example:

```text
tests/
└── unit/
    ├── test_risk_service.py
    ├── test_investigation_service.py
    └── test_transaction_service.py
```

## Integration Tests

Integration tests verify interactions between application components and the graph database where appropriate.

Example:

```text
tests/
└── integration/
    ├── test_graph_repository.py
    └── test_investigation_api.py
```

---

# Error Handling

FraudLens handles database and API failures without exposing raw implementation errors to the user.

For example, if CognoDB is temporarily unavailable, the frontend should display:

```text
Unable to load investigation.

The graph database is currently unavailable.

[Retry]
```

The backend returns appropriate HTTP status codes and structured error responses.

---

# User Workflow

A typical user session follows this workflow:

```text
             Open FraudLens
                    |
                    v
             View Dashboard
                    |
                    v
          Select Investigation
                    |
                    v
          View Transaction
                    |
                    v
           Risk Assessment
                    |
                    v
          Risk Indicators
                    |
                    v
         Connected Entities
                    |
                    v
          Graph Exploration
                    |
                    v
         Suspicious Network
```

---

# Example Investigation

A user selects:

```text
TXN-001024
```

FraudLens returns:

```text
Transaction: TXN-001024
Amount: $4,820
Merchant: Electronics Store
Account: ACC-1023

Risk Level: HIGH
Risk Score: 80
```

Risk indicators:

```text
+------------------------------+
| Risk Indicators              |
+------------------------------+
| Shared Device        +30     |
| Shared IP             +20    |
| Connected Account     +30    |
+------------------------------+
| TOTAL                 80     |
+------------------------------+
```

The investigator then opens the network:

```text
Account A
   |
   +---- Device X ---- Account B
   |                     |
   |                     +---- Transaction B
   |
   +---- IP X -------- Account C
```

This gives the investigator contextual evidence for further investigation.

---

# Frontend Screens

## Dashboard

The dashboard provides:

- Total transactions
- Flagged transactions
- High-risk accounts
- Suspicious devices
- Recent suspicious activity
- Example investigation scenarios

## Transaction Investigation

Displays:

- Transaction details
- Account
- Customer
- Merchant
- Risk score
- Risk level
- Risk indicators
- Connected entities

## Graph Explorer

Displays the relationship network between:

- Customers
- Accounts
- Transactions
- Devices
- IP addresses
- Merchants

The graph explorer allows the user to visually understand how entities are connected.

---

# Screenshots

Screenshots will be added after the frontend implementation.

Expected screenshots:

```text
docs/screenshots/
├── dashboard.png
├── transaction-investigation.png
├── risk-analysis.png
└── graph-explorer.png
```

---

# Deployment

FraudLens is designed to be deployed using Render for the application layer and CognoDB Cloud for the graph database.

Architecture:

```text
                         Internet
                            |
               +------------+------------+
               |                         |
               v                         v
       React Frontend             FastAPI Backend
           Render                    Render
                                         |
                                       Bolt
                                         |
                                         v
                                  CognoDB Cloud
```

## Production Environment Variables

The backend deployment requires:

```text
COGNODB_URI
COGNODB_USERNAME
COGNODB_PASSWORD
```

These values are configured through Render's environment-variable settings.

Database credentials are never stored in the Git repository.

---

# Live Demo

Application:

```text
https://YOUR-RENDER-APP.onrender.com
```

API:

```text
https://YOUR-BACKEND-RENDER-APP.onrender.com
```

API Documentation:

```text
https://YOUR-BACKEND-RENDER-APP.onrender.com/docs
```

> Links will be updated after deployment.

---

# Screen Recording

A short screen recording demonstrates the main functionality of FraudLens.

The demonstration covers:

1. Opening the dashboard.
2. Selecting a suspicious transaction.
3. Viewing the risk assessment.
4. Viewing risk indicators.
5. Exploring connected entities.
6. Traversing the suspicious network.
7. Explaining how the graph relationships support the investigation.

Recording:

```text
LINK_TO_SCREEN_RECORDING
```

---

# Design Decisions

## Graph Database

CognoDB Cloud was selected because the primary problem involves discovering and traversing relationships between entities.

## Rule-Based Risk Engine

The MVP uses deterministic rules rather than machine learning.

This makes the result:

- Explainable
- Reproducible
- Easy to test
- Easy to demonstrate

The purpose of the project is primarily to demonstrate graph modeling, traversal, and application of graph data to a practical use case.

## Synthetic Data

The application uses synthetic data instead of real banking information.

This avoids exposing sensitive financial information while allowing realistic fraud scenarios to be demonstrated.

## Predefined Investigation Scenarios

Users do not need to create transactions manually.

The application provides seeded scenarios so that a reviewer can immediately investigate interesting cases.

---

# Limitations

FraudLens is a technical demonstration and not a production banking fraud detection platform.

The current implementation has several limitations:

- Synthetic rather than real banking data.
- Simplified rule-based risk scoring.
- No real-time transaction stream.
- No integration with a real bank.
- No production-grade investigator case-management workflow.
- No machine-learning fraud model.
- Limited fraud patterns compared with a production banking system.

The risk score should therefore be interpreted as an investigative signal rather than a definitive fraud classification.

---

# Future Improvements

## Machine Learning

Use historical investigation outcomes to build predictive fraud models.

## Real-Time Monitoring

Process transactions as they occur and automatically generate investigation alerts.

## Advanced Graph Analytics

Introduce graph algorithms for:

- Community detection
- Centrality analysis
- Path analysis
- Connected-component analysis
- Anomaly detection

## Investigator Case Management

Allow investigators to:

- Create cases
- Add transactions to cases
- Assign cases
- Add notes
- Track investigation status
- Record investigation outcomes

## Configurable Risk Rules

Allow administrators to configure:

```text
Shared device threshold
Shared IP threshold
Risk score weights
Suspicious merchant rules
Transaction thresholds
```

without modifying application code.

## Authentication and Authorization

Add:

- Investigator accounts
- Administrator accounts
- Role-based access control
- Audit logging

## Real-Time Graph Updates

Automatically update the graph when new transaction events arrive.

---

# Project Alignment

| Requirement | Implementation |
|---|---|
| Graph database | CognoDB Cloud |
| Practical use case | Retail banking fraud investigation |
| Graph modeling | Customers, accounts, transactions, devices, IPs and merchants |
| Typed relationships | `OWNS`, `MAKES`, `FROM_DEVICE`, `FROM_IP`, `TO`, etc. |
| Seed data | Automated synthetic seed script |
| Multi-hop traversal | Transaction → Account → Device → Account → Transaction |
| Relationship-heavy query | Suspicious network investigation |
| Parameterized Cypher | Neo4j Python Driver parameters |
| Database error handling | Backend and frontend error states |
| Web application | React frontend + FastAPI backend |
| Non-technical user | Investigation-oriented UI |
| Automated tests | pytest |
| Hosted deployment | Render |
| Graph database | CognoDB Cloud |
| Documentation | README + architecture/UML documentation |
| Demonstration | Hosted application + screen recording |

---

# Security Considerations

FraudLens does not store real banking credentials or financial information.

Database credentials are provided through environment variables:

```text
COGNODB_URI
COGNODB_USERNAME
COGNODB_PASSWORD
```

User-provided identifiers are passed to the graph database as parameters rather than concatenated into Cypher queries.

The application uses synthetic data for demonstration purposes.

---

# Repository

```text
https://github.com/YOUR_USERNAME/fraudlens
```

---


# Author

**Abdulwahab Adamson**

GitHub:

```text
https://github.com/Adamsonoladipupo
```

---

# Project Summary

FraudLens demonstrates how a graph database can be applied to retail banking fraud investigation.

The core idea is:

> **Fraud is not always visible in a transaction. It can become visible through the relationships surrounding that transaction.**

By representing customers, accounts, transactions, devices, IP addresses, and merchants as connected entities, FraudLens allows investigators to move beyond isolated transaction analysis and explore the underlying network of relationships.
