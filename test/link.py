# -*- coding: UTF-8 -*-
import socket
import time
import os

def start_tcp_client(my_ip,my_port,target_ip, target_port,ans):
    id = bytes("YSZY001",'UTF-8').hex()
    # ans = "START\rGoal_ID=CA002;Num=3\rGoal_ID=CA003;Num=3\rEND"
    ans_len = len(ans.encode())
    ans = bytes(ans, 'UTF-8')
    ans_len = '{:08x}'.format(ans_len)
    hexstring = ans.hex()
    server_ip = target_ip
    servr_port = target_port
    tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_client.bind((my_ip,my_port))
    tcp_client.connect((server_ip, servr_port))
    print('sending..........')
    tcp_client.send(bytes.fromhex("00000000"+"00000007"+id))
    time.sleep(3)
    tcp_client.send(bytes.fromhex("00000001"+ans_len+hexstring))
    tcp_client.close()

start_tcp_client('169.254.63.99', 0, '169.254.63.99', 6666,
                     "START\rGoal_ID=CA002;Num=3\rGoal_ID=CA003;Num=3\rEND")
