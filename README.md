# Cryptocurrency Price Alert API

This API allows users to track cryptocurrencies, set price alerts, and receive notifications via email or other methods when the price or percentage change reaches a specified threshold. The API pulls live cryptocurrency market data using external services like CoinGecko and stores user preferences and alert details in a SQL database.

## Features:
- Retrieve cryptocurrency details (e.g., Bitcoin, Ethereum).
- Set price alerts for specific cryptocurrencies.
- Get notifications when thresholds are crossed.
- Store users and their alert configurations in a database.

---

## Table of Contents
1. [Setting Up the Project](#setting-up-the-project)
   - [Database Setup](#database-setup)
   - [Install Dependencies](#install-dependencies)
2. [Running the API](#running-the-api)
3. [Interacting with the API Using Postman](#interacting-with-the-api-using-postman)
4. [Example API Requests and Responses](#example-api-requests-and-responses)

---

## Setting Up the Project

### 1. Database Setup
This project uses **MySQL** as the database. Ensure MySQL is installed on your system. You need to create a database and configure your environment with the necessary credentials.

1. Install MySQL (if not already installed) and start the MySQL server.
2. Create a new database:
    ```sql
    CREATE DATABASE hodlup_api;
    ```

3. Configure your `.env` file:
    Create a `.env` file in the root of the project with the following details. Replace the placeholders with the actual SQL connection informations provided in the lytespace submission. 
    ```env
    DB_USER=your_mysql_username
    DB_PASS=your_mysql_password
    DB_HOST=localhost
    DB_NAME=hodlup_api
    ```

### 2. Install Dependencies

1. Make sure Python 3.x is installed on your system.
2. Create a virtual environment (optional but recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On macOS/Linux
    venv\Scripts\activate     # On Windows
    ```

3. Install the required dependencies using `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```

**Example `requirements.txt`**:
```txt
requests 
sqlalchemy
mysql-connector-python
python-dotenv
PyMySQL
fastapi 
uvicorn # this is the ASGI server that FastAPI uses
```

---

## Running the API

Once the database is set up and the dependencies are installed, you can run the API server using Uvicorn.

1. Apply database migrations:
    ```bash
    python main.py  # Ensure that your database tables are created when the app starts
    ```

2. Run the FastAPI app using Uvicorn:
    ```bash
    uvicorn main:app --reload
    ```

The app should now be running at `http://127.0.0.1:8000`.

---

## Interacting with the API Using Postman

You can use **Postman** to interact with the API. Here are some instructions to help you get started:

### Step 1: Open Postman
If you haven't installed Postman, you can download it [here](https://www.postman.com/downloads/).

### Step 2: Create a New Request

#### 1. **GET All Cryptocurrencies**
- **URL**: `http://127.0.0.1:8000/cryptocurrencies/`
- **Method**: `GET`
- **Description**: Retrieves all cryptocurrency records from the database.

#### 2. **GET Cryptocurrency by ID**
- **URL**: `http://127.0.0.1:8000/cryptocurrencies/{crypto_id}`
- **Method**: `GET`
- **Description**: Retrieves a specific cryptocurrency by its ID.

#### 3. POST Add New Cryptocurrency
- **URL:** `http://127.0.0.1:8000/cryptocurrencies/`
- **Method:** `POST`
  -(For VS Code: select body > raw >JSON (from the toggle bar in the right side) and write down the test there and send the request)
- **Description:** Adds a new cryptocurrency to the database.


### 4. Update a Cryptocurrency

- **Method**: `PUT`
- **URL**: `http://127.0.0.1:8000/cryptocurrencies/{crypto_id}` (replace `{crypto_id}` with an actual ID)
- **Body**: Go to the "Body" tab, select "raw" and "JSON", and enter the updated cryptocurrency data. For example:
  ```json
  {
    "name": "Updated Crypto Name",
    "market_cap": 10000000.0,
    "hourly_price": 500.0,
    "hourly_percentage": 2.5
  }
  ```
- **Click**: `Send`

### 5. Delete a Cryptocurrency

- **Method**: `DELETE`
- **URL**: `http://127.0.0.1:8000/cryptocurrencies/{crypto_id}` (replace `{crypto_id}` with an actual ID)
- **Click**: `Send`


---

## Example API Requests and Responses

### 1. **GET All Cryptocurrencies**

**Request**:
```bash
GET http://127.0.0.1:8000/cryptocurrencies/
```

**Response**:
```json
[
    {
        "id": 1,
        "name": "Bitcoin",
        "market_cap": 600000000000.0,
        "hourly_price": 30000.0,
        "time_updated": "2024-10-10T21:07:58",
        "hourly_percentage": 1.5
    },
    {
        "id": 2,
        "name": "Ethereum",
        "market_cap": 250000000000.0,
        "hourly_price": 1800.0,
        "time_updated": "2024-10-10T21:07:58",
        "hourly_percentage": -2.3
    },
    {
        "id": 3,
        "name": "Cardano",
        "market_cap": 50000000000.0,
        "hourly_price": 0.5,
        "time_updated": "2024-10-10T21:07:58",
        "hourly_percentage": 0.8
    },
    {
        "id": 10,
        "name": "Ripple",
        "market_cap": 25000000000.0,
        "hourly_price": 0.45,
        "time_updated": "2024-10-17T00:54:42",
        "hourly_percentage": 1.2
    },
    {
        "id": 11,
        "name": "Bitcoin",
        "market_cap": 1000000000000.0,
        "hourly_price": 50000.0,
        "time_updated": "2024-10-17T17:40:18",
        "hourly_percentage": 2.5
    },
    {
        "id": 12,
        "name": "Litecoin",
        "market_cap": 1000000000.0,
        "hourly_price": 200.0,
        "time_updated": "2024-10-17T14:50:00",
        "hourly_percentage": 1.75
    },
    {
        "id": 13,
        "name": "TestCoin",
        "market_cap": 500000000.0,
        "hourly_price": 100.0,
        "time_updated": "2024-10-17T14:56:27",
        "hourly_percentage": 0.75
    }
]
```

### 2. **GET Cryptocurrency by ID**

**Request**:
```bash
GET http://127.0.0.1:8000/cryptocurrencies/1
```

**Response**:
```json
{
    "id": 1,
    "name": "Bitcoin",
    "market_cap": 600000000000.0,
    "hourly_price": 30000.0,
    "time_updated": "2024-10-10T21:07:58",
    "hourly_percentage": 1.5
}
```
### 3. **POST Add New Cryptocurrency**
Request:
```bash
POST http://localhost:8000/cryptocurrencies/
```
Body (JSON):
```bash
{
    "name": "TestCoin",
    "market_cap": 500000000.00,
    "hourly_price": 100.00,
    "hourly_percentage": 0.75
}
```
Response:
```bash
{
    "id": 13,
    "name": "TestCoin",
    "market_cap": 500000000.0,
    "hourly_price": 100.0,
    "hourly_percentage": 0.75,
    "time_updated": "2024-10-17T14:56:27"
}
```

### 4. **PUT Update a Cryptocurrency**

**Request**:
```bash
PUT http://localhost:8000/cryptocurrencies/1
```
**Body** (JSON):
```json
{
    "name": "Updated Crypto Name",
    "market_cap": 10000000.0,
    "hourly_price": 500.0,
    "hourly_percentage": 2.5
}
```
**Response**:
```json
{
    "id": 1,
    "name": "Updated Crypto Name",
    "market_cap": 10000000.0,
    "hourly_price": 500.0,
    "hourly_percentage": 2.5,
    "time_updated": "2024-10-17T12:34:56.789Z"
}
```

### 5. **DELETE a Cryptocurrency**

**Request**:
```bash
DELETE http://localhost:8000/cryptocurrencies/1
```
**Response**:
```json
{
    "detail": "Cryptocurrency deleted successfully"
}
```
