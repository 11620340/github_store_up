import requests
import re
import  pandas
import time

categories = requests.get('https://ali-esi.evepc.163.com/latest/universe/categories/?datasource=serenity').text
categories = categories.replace("[", "")
categories = categories.replace("]", "")
categories = categories.split(",")
#
#
item_category_information_list = []


for i in categories:
    id_name_dict = {}
    item_category_information = requests.get(f'https://ali-esi.evepc.163.com/latest/universe/categories/{i}/?datasource=serenity&language=zh').text
    item_category_information = item_category_information.encode().decode("unicode_escape")
    item_category_information_id = re.findall(r'category_id":(.*?),"groups', item_category_information)
    item_category_information_name = re.findall(r'name":"(.*?)","published', item_category_information)
    id_name_dict['ID'] = item_category_information_id[0]
    id_name_dict['name'] = item_category_information_name[0]
    item_category_information_list.append(id_name_dict)


    print(f"{i} done")

print(item_category_information_list)
df = pandas.DataFrame(item_category_information_list)
df.to_excel('item_type.xlsx', index=False)
print(df)


# f = open('item.txt', 'w')
# f.write(str(item_category_information_list))
# f.close()