"""
InnoSphere Database Connector & Utility Layer
Provides connection pooling, context management, and query helpers.
"""

import os
from contextlib import contextmanager
import mysql.connector
from mysql.connector import pooling
from config import Config

# Initialize MySQL connection pool for high concurrency
db_pool = None

try:
    db_pool = mysql.connector.pooling.MySQLConnectionPool(
        pool_name="innosphere_pool",
        pool_size=10,
        pool_reset_session=True,
        host=Config.DB_HOST,
        port=Config.DB_PORT,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        database=Config.DB_NAME,
        autocommit=False
    )
except Exception as e:
    # Fallback to direct connection if pooling is not supported
    db_pool = None


def get_db_connection():
    """
    Returns an active database connection from the pool or directly.
    """
    if db_pool:
        return db_pool.get_connection()
    return mysql.connector.connect(
        host=Config.DB_HOST,
        port=Config.DB_PORT,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        database=Config.DB_NAME,
        autocommit=False
    )


@contextmanager
def get_db(commit=False):
    """
    Context manager for database transactions.
    Automatically closes connections and handles commit/rollback.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        yield cursor, conn
        if commit:
            conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()


def query_all(sql, params=None):
    """
    Executes a SELECT query and returns all matching rows as a list of dicts.
    """
    with get_db() as (cursor, conn):
        cursor.execute(sql, params or ())
        return cursor.fetchall()


def query_one(sql, params=None):
    """
    Executes a SELECT query and returns a single row or None.
    """
    with get_db() as (cursor, conn):
        cursor.execute(sql, params or ())
        return cursor.fetchone()


def execute_dml(sql, params=None):
    """
    Executes an INSERT, UPDATE, or DELETE statement.
    Returns (lastrowid, rowcount).
    """
    with get_db(commit=True) as (cursor, conn):
        cursor.execute(sql, params or ())
        return cursor.lastrowid, cursor.rowcount
