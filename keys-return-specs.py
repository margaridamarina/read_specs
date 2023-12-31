import csv
import json

def get_keys(spec):
    list_keys = []
    unwanted_keys = ['type', 'name', 'sample', 'required', 'condition', 'avoid_retry', 'emit_event']
    for step in spec.get("steps", []):
        if step.get("type") == "parser":
            for field in step.get("fields", []):
                if field.get("type") == "ListField":
                    keys = [key for key in field.keys() if key not in unwanted_keys and field[key] is not None] 
                    list_keys.append(keys)
    return list_keys

def list_of_keys_to_string(keys_list):
    sorted_keys = ['+'.join(sorted(keys)) for keys in keys_list]
    return '+'.join(sorted(sorted_keys))

def get_list_of_keys(csv_filename):
    list_of_keys = []
    with open(csv_filename, newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)  

        for row_number, row in enumerate(csvreader, start=2):  
            if row[4]:
                spec_str = row[4]
                spec_dict = json.loads(spec_str)
                keys = get_keys(spec_dict)
                list_of_keys.append((row[0], row[2], keys))  # Adiciona também o número do crawler e o projeto

    return list_of_keys

if __name__ == '__main__':
    data = get_list_of_keys("query_result.csv")
    
    key_to_row_mapping = {}  
    with open("query_result.csv", newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)  

        for row_number, row in enumerate(csvreader, start=2):  
            if row[4]:
                spec_str = row[4]
                spec_dict = json.loads(spec_str)
                keys = get_keys(spec_dict)
                key_string = list_of_keys_to_string(keys)
                key_to_row_mapping[key_string] = (row[0], row[2], row_number)  # Mapeia a lista de chaves para o número da linha, o número do crawler e o nome do projeto
    
    unique_list_of_keys = list(set(list_of_keys_to_string(keys) for _, _, keys in data))
    for unique_key in unique_list_of_keys:
        print(f"Lista de Chaves: {unique_key}")
        crawler_number, project_name, row_number = key_to_row_mapping.get(unique_key, (None, None, None))
        if row_number:
            print(f"Numero do Crawler: {crawler_number}")
            print(f"Projeto: {project_name}")
            print(f"Linha do CSV: {row_number}" + "\n")
