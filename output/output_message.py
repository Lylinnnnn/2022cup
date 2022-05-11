# -*- coding:utf-8 -*-


def sort_by_key(d):
    return sorted(d.items(), key=lambda k: k[0])

def change():
    classes=[b'cz',b'jz',b'xz',b'xsy',b'z',b'kxt',b'fbm',b'sp',b'gzyl',b'pzyl',b'nn',b'yys',b'pg',b'l',b'xj',b'mht']
    changes=['CA001','CA002','CA003','CA004','CB001','CB002','CB003','CB004','CC001','CC002','CC003','CC004','CD001','CD002','CD003','CD004']
    return classes,changes

def output_info(name,num):
    keys,values=change()
    dictionary = dict(zip(keys, values))
    ans_str='目标ID:'+dictionary[name]+' '+'数量:'+str(num)
    return ans_str

def output_state(num):
    state = ["空闲", "识别中", "待转动", "结束"]
    return state[num]

def create_file(str):
    desktop_path = './ANS'
    full_path = desktop_path + '/ans.txt'
    file = open(full_path, 'w')
    file.write(str)
    pass

def change_list2dict(list):
    name_list=list
    my_dict = {}
    for i in name_list:
        if i in my_dict:
            my_dict[i] += 1
        else:
            my_dict[i] = 1
    return my_dict

def dict2str(dic):
    classes = [b'cz', b'jz', b'xz', b'xsy', b'z', b'kxt', b'fbm', b'sp', b'gzyl', b'pzyl', b'nn', b'yys', b'pg', b'l',b'xj', b'mht']
    changes = ['CA001', 'CA002', 'CA003', 'CA004', 'CB001', 'CB002', 'CB003', 'CB004', 'CC001', 'CC002', 'CC003','CC004', 'CD001', 'CD002', 'CD003', 'CD004']
    for i,thing in enumerate(classes):
        if dic. __contains__(thing):
            dic[changes[i]] = dic[thing]
            del dic[thing]
    ans_str='START\r'
    dic = dict(sort_by_key(dic))
    for item in dic.items():
        (name,num)=item
        # "START\rGoal_ID=CA002;Num=3\rGoal_ID=CA003;Num=3\rEND"
        ans_str=ans_str+'Goal_ID='+name+';'+'Num='+str(num)+'\r'
    ans_str+='END'
    ans_len = len(ans_str.encode())
    ans = bytes(ans_str, 'UTF-8')
    ans_len = '{:08x}'.format(ans_len)
    hexstring = ans.hex()
    return ans_str,ans_len,hexstring