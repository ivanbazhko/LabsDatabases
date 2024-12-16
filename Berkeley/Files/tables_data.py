import bsddb3
import os
import json

def get_db_len(db_path):
    try:
        db = bsddb3.btopen(db_path, 'r')
    except Exception as e:
        print(f"Error opening database: {e}")
        return 0
    count = 0
    try:
        for key in db.keys():
            count += 1
    except Exception as e:
        print(f"Error reading records: {e}")
    finally:
        db.close()
    return count

def get_len_mod_name(dbname):
    return get_db_len(f'./databases/{dbname}.db')

def transform_string(input_string):
    data = json.loads(input_string)
    return tuple(data.values())

def get_records(dbname):
    try:
        db = bsddb3.btopen(f'./databases/{dbname}.db', 'r')
    except Exception as e:
        print(f"Error opening database: {e}")
        return
    ids = []
    records = []
    try:
        for key in db.keys():
            value = db[key]
            key = key.decode("utf-8")
            value = value.decode("utf-8")
            ids.append(key)
            records.append(transform_string(value))
    except Exception as e:
        print(f"Error reading records: {e}")
    finally:
        db.close()
    return ids, records

def unite_arrays(keys, values):
    if len(keys) != len(values):
        raise ValueError("Both arrays must have the same length.")
    combined_dict = dict(zip(keys, values))
    combined_string = json.dumps(combined_dict)
    return combined_string

def add_new_record(dbname, data, oid = -1):
    global maxkey
    try:
        db = bsddb3.btopen(f'./databases/{dbname}.db', 'c')
    except Exception as e:
        print(f"Error opening database: {e}")
        return
    maxkey = 0
    nid = 0
    try:
        for key in db.keys():
            ikey = int(key)
            if ikey > maxkey:
                maxkey = ikey
    except Exception as e:
        print(f"Error reading records: {e}")
    if int(oid) > 0:
        maxkey = int(oid) - 1
    try:
        key = f'{maxkey + 1}'.encode("utf-8")
        nid = f'{maxkey + 1}'
        value = data.encode("utf-8")
        db[key] = value
    except Exception as e:
        print(f"Error adding record: {e}")
    finally:
        db.close()
    return nid

def delete_record(dbname, orkey):
    k = None
    try:
        db = bsddb3.btopen(f'./databases/{dbname}.db', 'c')
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
        del db[k]
    except Exception as e:
        print(f"Error editing record: {e}")
    finally:
        db.close()

def edit_record(dbname, data, orkey):
    k = None
    try:
        db = bsddb3.btopen(f'./databases/{dbname}.db', 'c')
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

def extract_elements(data, index):
    return [t[index] for t in data]

def process_json_data(dbname, json_string, orids):
    err = 0
    # Create the databases directory if it doesn't exist
    os.makedirs('./databases', exist_ok=True)

    try:
        # Load the JSON data from the string
        json_data = json.loads(json_string)
        
        # Check if the loaded data is a list
        if isinstance(json_data, list):
            # Create a database for all entries
            db = bsddb3.db.DB()
            db.open(f'./databases/{dbname}.db', None, bsddb3.db.DB_BTREE, bsddb3.db.DB_CREATE)
            
            for item in json_data:
                if isinstance(item, dict):
                    # Use the first value as the key
                    for it in orids:
                        if str(it) == str(list(item.values())[0]):
                            continue
                    key = f'{list(item.values())[0]}'.encode('utf-8')
                    value_data = {k: item[k] for k in item if k != list(item.keys())[0]}
                    value_structure = json.dumps(value_data).encode("utf-8")
                    
                    # Insert the key-value pair into the database
                    try:
                        db.put(key, value_structure)
                    except Exception as e:
                        err = 1
                        print(f"Error inserting into database for key {key.decode('utf-8')}: {e}")
                else:
                    print("Item is not a dictionary:", item)
            db.close()
        else:
            err = 1
            print("Provided data is not a list:", json_data)
    
    except json.JSONDecodeError:
        print("Invalid JSON data provided.")
        err = 1

    return err

