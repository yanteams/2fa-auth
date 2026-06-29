from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import psycopg2
from psycopg2.extras import RealDictCursor
import config
from datetime import datetime

app = FastAPI(title="2FA API")

# Enable CORS for Extension
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db_connection():
    try:
        # We can use DATABASE_URL or the DB_* variables
        conn = psycopg2.connect(
            host=config.DB_HOST,
            database=config.DB_NAME,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            port=config.DB_PORT
        )
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        raise e

class AccountCreate(BaseModel):
    name: str
    secret_key: str
    key_type: str = "TOTP"
    username: Optional[str] = None
    password: Optional[str] = None

class AccountUpdate(BaseModel):
    name: Optional[str] = None
    secret_key: Optional[str] = None
    key_type: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None

@app.get("/api/accounts")
def get_accounts():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute("SELECT * FROM twofa_accounts ORDER BY created_at DESC")
        accounts = cursor.fetchall()
        return accounts
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@app.post("/api/accounts")
def add_account(account: AccountCreate):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cleaned_key = account.secret_key.replace(" ", "").replace("-", "").replace(":", "")
        cursor.execute("""
            INSERT INTO twofa_accounts (name, secret_key, key_type, username, password, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING *
        """, (account.name.strip(), cleaned_key, account.key_type, account.username, account.password, datetime.now(), datetime.now()))
        new_account = cursor.fetchone()
        conn.commit()
        return new_account
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@app.put("/api/accounts/{account_id}")
def update_account(account_id: int, account: AccountUpdate):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        update_fields = []
        params = []
        
        if account.name is not None:
            update_fields.append("name = %s")
            params.append(account.name.strip())
        if account.username is not None:
            update_fields.append("username = %s")
            params.append(account.username)
        if account.password is not None:
            update_fields.append("password = %s")
            params.append(account.password)
        if account.secret_key is not None:
            update_fields.append("secret_key = %s")
            params.append(account.secret_key.replace(" ", "").replace("-", "").replace(":", ""))
        if account.key_type is not None:
            update_fields.append("key_type = %s")
            params.append(account.key_type)
            
        if not update_fields:
            return {"message": "No fields to update"}
            
        update_fields.append("updated_at = %s")
        params.append(datetime.now())
        
        params.append(account_id)
        
        query = f"UPDATE twofa_accounts SET {', '.join(update_fields)} WHERE id = %s RETURNING *"
        cursor.execute(query, tuple(params))
        updated_account = cursor.fetchone()
        if not updated_account:
            raise HTTPException(status_code=404, detail="Account not found")
        conn.commit()
        return updated_account
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@app.delete("/api/accounts/{account_id}")
def delete_account(account_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM twofa_accounts WHERE id = %s RETURNING id", (account_id,))
        deleted = cursor.fetchone()
        if not deleted:
            raise HTTPException(status_code=404, detail="Account not found")
        conn.commit()
        return {"message": "Deleted successfully"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()
