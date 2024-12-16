import os
import json
import bsddb3

def process_json_files(directory):
    for filename in os.listdir(directory):
        base = os.path.splitext(filename)[0]
        new_filename = f"./databases/{base}.db"
        print(f'{filename} -> {new_filename}')
        try:
            os.makedirs('./databases', exist_ok=True)
        except Exception as e:
            pass
        if filename.endswith('.json'):
            file_path = os.path.join(directory, filename)
            db = bsddb3.db.DB()
            db.open(new_filename, None, bsddb3.db.DB_BTREE, bsddb3.db.DB_CREATE)
            try:
                with open(file_path, 'r') as json_file:
                    data = json.load(json_file)
                    if isinstance(data, list):
                        for item in data:
                            if isinstance(item, dict):
                                key = f'{list(item.values())[0]}'.encode('utf-8')
                                value_data = {k: item[k] for k in item if k != list(item.keys())[0]}
                                value_structure = json.dumps(value_data).encode("utf-8")
                                print(key, value_structure)
                                db.put(key, value_structure)
                            else:
                                print("Item is not a dictionary:", item)
                    else:
                        print(f"Data in {filename} is not a list: {data}")
            except Exception as e:
                print(f"Error processing file {filename}: {e}")
            db.close()

directory_path = './dumps'
process_json_files(directory_path)
