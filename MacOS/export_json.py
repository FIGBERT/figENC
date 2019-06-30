import json

#Data to export. The initial keys are used to select the data groups.
data = {}
#Configuring the script - filepath, data, etc.
filename = input("File path for exported json data: ")
data_header = input("Data to convert to json format: ")
data_info = data[data_header]
#Outputting the dictionary in json format
with open(filename, 'w') as file_export:
    json.dump(data_info, file_export, indent=4, sort_keys=True)