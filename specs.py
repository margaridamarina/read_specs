import csv
import json

def get_keys(spec):
    list_keys = []
    unwanted_keys = ['type', 'name', 'json_path', 'sample', 'required', 'attribute', 'condition', 'avoid_retry', 'emit_event']
    for step in spec.get("steps", []):
        if step.get("type") == "parser":
            for field in step.get("fields", []):
                if field.get("type") == "ListField":
                    keys = [key for key in field.keys() if key not in unwanted_keys] 
                    list_keys.append(keys)
    return list_keys

def get_list_of_keys(csv_filename):
    list_of_keys = []
    with open(csv_filename, newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)  

        for row in csvreader:
            if row[4]:
                spec_str = row[4]
                spec_dict = json.loads(spec_str)
                keys = get_keys(spec_dict)
                list_of_keys.extend(keys)
    return list_of_keys

if __name__ == '__main__':
    data = get_list_of_keys("query_result.csv")
    sorted_list_keys = [sorted(x) for x in data]
    joined_list_keys = ['+'.join(x) for x in sorted_list_keys]
    unique_list_of_keys = [x.split('+') for x in list(set(joined_list_keys))]
    for unk_list_key in unique_list_of_keys:
        print(unk_list_key)
    