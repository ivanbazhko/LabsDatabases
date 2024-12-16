import bsddb3
import os

maxkey = 1

def print_all_records(db_path):
    global maxkey
    try:
        db = bsddb3.btopen(db_path, 'r')
    except Exception as e:
        print(f"Error opening database: {e}")
        return
    try:
        for key in db.keys():
            value = db[key]
            key = key.decode("utf-8")
            ikey = int(key)
            value = value.decode("utf-8")
            print(f"Key: {key}, Value: {value}")
            if ikey > maxkey:
                maxkey = ikey
    except Exception as e:
        print(f"Error reading records: {e}")
    finally:
        db.close()

def edit_record(db_path, data, orkey):
    global maxkey
    k = None
    try:
        db = bsddb3.btopen(db_path, 'c')
    except Exception as e:
        print(f"Error opening database: {e}")
        return
    try:
        k = f'{orkey}'.encode("utf-8")
        value = db[k]
    except Exception as e:
        print(f"Record with key '{orkey}' does not exist.")
        return
    try:
        value = data.encode("utf-8")
        db[k] = value
    except Exception as e:
        print(f"Error editing record: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    user_input = input("Enter table name: ")
    if os.path.exists(f'./databases/{user_input}.db'):
        print_all_records(f'./databases/{user_input}.db')
        print('========================================')
        orig_key = input("Enter the key: ")
        new_data = input("Enter new data: ")
        edit_record(f'./databases/{user_input}.db', new_data, orig_key)
        print('========================================')
        print_all_records(f'./databases/{user_input}.db')
    else:
        print(f"The file ./databases/'{user_input}'.db does not exist.")
    
