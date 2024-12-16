import psycopg2
import datetime
import json
import os

def get_all_tables(cursor):
    try:
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'postgres';
        """)
        tables = cursor.fetchall()
        return [table[0] for table in tables]
    except Exception as e:
        print(f"Error getting tables: {e}")
        return []

def get_primary_keys(cursor, table_name):
    try:
        cursor.execute(f"""
            SELECT kcu.column_name
            FROM information_schema.table_constraints tco
            JOIN information_schema.key_column_usage kcu
            ON kcu.constraint_name = tco.constraint_name
            WHERE tco.constraint_type = 'PRIMARY KEY' AND tco.table_name = '{table_name}';
        """)
        primary_keys = cursor.fetchall()
        return [pk[0] for pk in primary_keys]
    except Exception as e:
        print(f"Error getting primary keys for {table_name}: {e}")
        return []
    
def get_column_names(cursor, table_name):
    try:
        cursor.execute(f"""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = '{table_name}';
        """)
        columns = cursor.fetchall()
        return [column[0] for column in columns]
    except Exception as e:
        print(f"Error getting column names for {table_name}: {e}")
        return []

import datetime

def get_all_data(cursor, table_name, cnfk):
    try:
        cursor.execute(f"SELECT * FROM {table_name};")
        data = cursor.fetchall()
        column_names = [description[0] for description in cursor.description]
        cnfk_index = column_names.index(cnfk)
        rearranged_column_names = [column_names[cnfk_index]] + [
            column_names[i] for i in range(len(column_names)) if i != cnfk_index
        ]
        filtered_data = []
        for row in data:
            new_row = (row[cnfk_index],) + tuple(
                item.strftime('%H:%M:%S') if isinstance(item, datetime.time) else item
                for i, item in enumerate(row) if i != cnfk_index
            )
            filtered_data.append(new_row)
        return rearranged_column_names, filtered_data
    except Exception as e:
        print(f"Error getting data from {table_name}: {e}")
        return [], []
    
def create_json_from_tuples(tuples_array, file_path, column_names):
    data_list = [
        {column_names[i]: value for i, value in enumerate(tup)}
        for tup in tuples_array
    ]
    with open(file_path, 'w') as json_file:
        json.dump(data_list, json_file, indent=4)

def main():
    conn = None
    try:
        conn = psycopg2.connect(host='localhost', database='newairport', user='postgres', password='admin')
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return
    
    if conn is not None:
        cursor = conn.cursor()
        tables = get_all_tables(cursor)
        print("Tables in the database:", tables)
        if tables:
            try:
                os.makedirs('./dumps', exist_ok=True)
            except Exception as e:
                pass
            for table_name in tables:
                columns = get_column_names(cursor, table_name)
                primary_key = get_primary_keys(cursor, table_name)
                columns, data = get_all_data(cursor, table_name, primary_key[0])
                print(f"Data from {table_name}:", columns, data)
                create_json_from_tuples(data, f'dumps/{table_name}.json', columns)
        conn.close()

if __name__ == "__main__":
    main()
