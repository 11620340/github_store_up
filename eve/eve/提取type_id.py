import pandas as pd
import requests


type_id_list = []


def get_type_id():
    global type_id_list
    i = 1
    while True:
        if i < 50:
            # 获取type_id
            type_id_str = requests.get(f"https://ali-esi.evepc.163.com/latest/universe/types/?datasource=serenity&page={i}").text
            type_id_str = type_id_str.replace("[", "")
            type_id_str = type_id_str.replace("]", "")
            # 字符串转换为列表
            type_id_list = type_id_list + type_id_str.split(",")
            print(f"第{i}页完成")
            i += 1
        else:
            break


def write_txt():
    # 写入txt
    f = open('type_id.txt', 'w')
    f.write(str(type_id_list))
    f.close()



def excle():
    # 写入excle
    df = pd.DataFrame(type_id_list, columns=['type_id'])
    df.to_excel('type.xlsx', index=False)


def main():
    get_type_id()
    # write_txt()
    excle()
    print(f"type id写入完成，共{len(type_id_list)}个id")


if __name__ == "__main__":
    main()