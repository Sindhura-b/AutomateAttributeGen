import pandas as pd
import glob
import re
import csv


# root_dir needs a trailing slash (i.e. /root/dir/)

def get_calibration_list(path):
    list_out = []
    for filename in glob.iglob(path, recursive=True):
        print(filename)
        pattern1 = re.compile(r'([\w]+)[ ]+([\w]+)[ ]+=[ ]+(\{([^{]+)\}|\w+)')
        pattern2 = re.compile(r'(/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/)')
        with open(filename, 'r') as f:
            contents = f.read()
            separate_statements = contents.split(';')
            for separate_statement in separate_statements:

                matches1 = pattern1.finditer(separate_statement)
                matches2 = pattern2.finditer(separate_statement)

                list1 = []
                there = False
                for match1 in matches1:
                    # print(match1.group(2))
                    value = match1.group(3)
                    list1 = [match1.group(1), match1.group(2), " ".join(value.split())]

                for match2 in matches2:
                    comments = match2.group(1)
                    comments = comments.replace('/* Object: ', '')
                    comments = comments.replace('*/', '')
                    #comments = comments.replace('\n  ', '')
                    there = True
                    list1.append(" ".join(comments.split()))
                    list1.append('Engine Thermal Management TRB')

                if there == False and len(list1) != 0:
                    list1.append('')
                    list1.append('Engine Thermal Management TRB')

                list_out.append(list1)
                list_out = [x for x in list_out if x != []]
    return list_out


list_new = []
list_old = []
list_final = []
path_new = r'C:\Users\sindh\Documents\software\VECR_valve_new\**\vec?k???.txt'
path_old = r'C:\Users\sindh\Documents\software\VECR_valve_old\**\vec?k???.txt'
list_new = get_calibration_list(path_new)
list_old = get_calibration_list(path_old)
print(list_old)
print(len(list_old[0]))
print(list_new)

added_datatype_columns_new = [line[0] for line in list_new if line]
added_name_columns_new = [line[1] for line in list_new if line]
added_value_columns_new = [line[2] for line in list_new if line]
added_description_columns_new = [line[3] for line in list_new if line]

added_datatype_columns_old = [line[0] for line in list_old if line]
added_name_columns_old = [line[1] for line in list_old if line]
added_value_columns_old = [line[2] for line in list_old if line]
added_description_columns_old = [line[3] for line in list_old if line]

for list_elem in list_new:
    if not (any([list_elem[1] == item for item in added_name_columns_old])):
        status = 'Add'
        list3 = [status] + list_elem
        list_final.append(list3)

for list_elem in list_old:
    if any([list_elem[1] == item for item in added_name_columns_new]):
        index = added_name_columns_new.index(list_elem[1])
        if not (list_elem[0] == added_datatype_columns_new[index] and
                list_elem[2] == added_value_columns_new[index] and
                list_elem[3] == added_description_columns_new[index]):
            status = 'modify'
            list3 = [status] + list_elem
            list_final.append(list3)
    else:
        status = 'delete'
        list3 = [status] + list_elem
        list_final.append(list3)

with open('innovators.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    columns_names = [["Status", 'Data type', 'Calibration', "Value", "Description", "Calibration TRB"]]
    writer.writerows(columns_names)
    writer.writerows(list_final)
