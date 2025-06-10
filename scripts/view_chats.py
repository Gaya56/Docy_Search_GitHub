#!/usr/bin/env python3
"""Simple database viewer"""
import sqlite3

def main():
    try:
        conn = sqlite3.connect('docy_search.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM chat_history ORDER BY timestamp DESC')
        records = cursor.fetchall()
        
        print('📊 DOCY SEARCH DATABASE')
        print('=' * 40)
        print(f'Total Chat Records: {len(records)}\n')
        
        for i, record in enumerate(records, 1):
            print(f'[{i}] {record["timestamp"][:19]}')
            print(f'Model: {record["model_used"]}')
            print(f'User: {record["prompt"][:80]}...')
            print(f'Bot: {record["response"][:80]}...')
            print('-' * 40)
        
        conn.close()
    except Exception as e:
        print(f'Error: {e}')

if __name__ == '__main__':
    main()
