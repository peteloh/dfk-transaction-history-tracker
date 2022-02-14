from pypika import Query, Table, Field
import sqlite3

DATABASE_FILE = './dfk_transaction_tracker.db'

HERO_AUCTION_SUCCESS_TABLE_NAME = 'hero_auction_success'
TABLE_TRACK_TABLE_NAME = 'table_track'

TABLES_NAMES = [
    HERO_AUCTION_SUCCESS_TABLE_NAME,
    TABLE_TRACK_TABLE_NAME
]

create_table_track_table_sql = f"""
CREATE TABLE IF NOT EXISTS {TABLE_TRACK_TABLE_NAME} (
    tableName     TEXT PRIMARY KEY,
    lastBlock     INTEGER,
    timestamp     DATETIME
);
"""

create_hero_auction_success_table_sql = f"""
CREATE TABLE IF NOT EXISTS {HERO_AUCTION_SUCCESS_TABLE_NAME} (
    auctionId     INTEGER PRIMARY KEY,
    blockNumber   INTEGER NOT NULL,
    tokenId       INTEGER NOT NULL,
    totalPrice    TEXT NOT NULL,
    txHash        TEXT NOT NULL,
    winner        TEXT NOT NULL,
    owner         TEXT
);
"""

hero_auction_success_table = Table(HERO_AUCTION_SUCCESS_TABLE_NAME)
insert_auction_success_table = \
    Query.into(hero_auction_success_table).columns(
        'auctionId', 
        'blockNumber',
        'tokenId',
        'totalPrice',
        'txHash',
        'winner'
    )

def connect_db(db_file):
    db = None
    try:
        db = sqlite3.connect(DATABASE_FILE)
    except sqlite3.Error as e:        
        print(e)
    return db

def execute_query(connection, query, print_error=False):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        return True
    except sqlite3.Error as e:
        if print_error:
            print(f"The error '{e}' occurred")
        return False

def delete_record(tb_name, where="", db=None):
    to_close = False
    if db is None:
        db = connect_db(DATABASE_FILE)
        to_close = True
    
    if where != "":
        where = " where " + where
    sql = f"delete from {tb_name}" + where
    result = execute_query(db, sql)

    if to_close:
        db.close()

    return result

def drop_table(tb_name, db=None):
    to_close = False
    if db is None:
        db = connect_db(DATABASE_FILE)
        to_close = True

    sql = f"drop table {tb_name}"
    result = execute_query(db, sql)

    if to_close:
        db.close()

    return result

def select_table(tb_name, where=None, db=None, is_print=False):
    to_close = False
    if db is None:
        db = connect_db(DATABASE_FILE)
        to_close = True

    cur = db.cursor()
    sql =   f"select * from {tb_name}" if where is None else \
            f"select * from {tb_name} where {where};"
    
    result = None
    try:
        result = cur.execute(sql)
    
        if is_print:
            for r in result:
                print(r)
        result = list(result)
    finally:
        if to_close:
            db.close()

    return result

def insert_auction_success_record(record, args):
    db = args['db']
    q = insert_auction_success_table \
        .insert(
            record['auctionId'],
            record['blockNumber'],
            record['tokenId'],
            record['totalPrice'],
            record['transactionHash'],
            record['winner']
        )
    result = execute_query(db, q.get_sql())
    return result

def insert_or_update_table_track(db, tb_name, block_num):
    sql = f"""
        INSERT INTO {TABLE_TRACK_TABLE_NAME} (tableName, lastBlock, timestamp) 
        VALUES ('{tb_name}', {block_num}, datetime('now'))
        ON CONFLICT(tableName) DO
        UPDATE SET lastBlock={block_num}, timestamp=datetime('now')
    """
    execute_query(db, sql)
