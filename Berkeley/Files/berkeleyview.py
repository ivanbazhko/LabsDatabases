import bsddb3
import os

def print_all_records(db_path):
    try:
        db = bsddb3.btopen(db_path, 'r')
    except Exception as e:
        print(f"Error opening database: {e}")
        return

    try:
        for key in db.keys():
            value = db[key]
            key = key.decode("utf-8")
            value = value.decode("utf-8")
            print(f"Key: {key}, Value: {value}")
            # print(key)
            # print(value)
    except Exception as e:
        print(f"Error reading records: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    print('========================================')
    for filename in os.listdir('./databases'):
        print(filename)
        print_all_records(f'./databases/{filename}')
        print('========================================')
