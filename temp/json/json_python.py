import json


json_data = '{"name": "Ivan", "age": 30, "is_student": false}'

parsed_data = json.loads(json_data)
print(parsed_data)


with open("json_example.json", "r", encoding="utf-8") as file:
    data = json.load(file)
    print(data)
