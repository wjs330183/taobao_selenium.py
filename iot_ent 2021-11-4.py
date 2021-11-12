from paho.mqtt import client as ct
import time
import decimal
import http.client as hc
from urllib.parse import quote
import struct
import datetime
broker = 'iot.yingheli.com'
port = 18085
username = "iot-se"
passwd = "42GcER!!@tfP"

topic_speed_req = "wind/speed_request"
topic_speed_res = "wind/speed_respond"
topic_speed_direction_req = "wind/speed_direction_request"
topic_speed_direction_res = "wind/speed_direction_respond"
topic_power_req = "power_request"
topic_power_res = "power_respond"
# 带显示传感器
topic_power_v_req = "power/v_request"
topic_power_v_res = "power/v_respond"

hexstring_speed = b'\x01\x03\x00\x16\x00\x01\x65\xCE'
hexstring_speed_direction = b'\x01\x03\x00\x00\x00\x02\xC4\x0B'
hexstring_power = b'\x01\x03\x00\x00\x00\x06\xC5\xC8'
hexstring_power_v = b"\x01\x03\x00\x39\x00\x12\x15\xCA"

sleep = 60
decimal.getcontext().prec = 3

def hex2float(h):
    f = struct.unpack('!f', h)[0]
    return round(f,1)

def insertDB(data):
    fmt = '/acceptDataYl/{"SBID":"%s","DL_A":"%s","DL_B":"%s","DL_C":"%s","DY_A":"%s","DY_B":"%s","DY_C":"%s"}'
    c = hc.HTTPSConnection("s.zjamr.zj.gov.cn", 8083)
    url = fmt % tuple(data)
    url_encode = quote(url)
    c.request("GET", url_encode)
    r = c.getresponse()
    # print(r.status)

def process_message_power(message):
    if(len(message.payload) < 17):
        return
    id = message.payload[0:5].decode("utf-8")
    A_hex = message.payload[8:10]
    B_hex = message.payload[10:12]
    C_hex = message.payload[12:14]
    U_hex = message.payload[14:16]
    V_hex = message.payload[16:18]
    W_hex = message.payload[18:20]
    A_int = int.from_bytes(A_hex, "big")
    B_int = int.from_bytes(B_hex, "big")
    C_int = int.from_bytes(C_hex, "big")
    A = round(A_int * 0.1, 1)
    B = round(B_int * 0.1, 1)
    C = round(C_int * 0.1, 1)
    U = int.from_bytes(U_hex, "big")
    V = int.from_bytes(V_hex, "big")
    W = int.from_bytes(W_hex, "big")
    insertDB([id,A,B,C,U,V,W])
    print([A,B,C,U,V,W])
    print(message.payload)

def process_message_power_v(message):
    if(len(message.payload) < 40):
        return
    id = message.payload[0:5].decode("utf-8")
    U = hex2float(message.payload[8:12])
    V = hex2float(message.payload[12:16])
    W = hex2float(message.payload[16:20])
    A = hex2float(message.payload[32:36])
    B = hex2float(message.payload[36:40])
    C = hex2float(message.payload[40:44])
    insertDB([id,A,B,C,U,V,W])
    print([A,B,C,U,V,W])
    print(message.payload)    

def process_message_speed(message):
    if(len(message.payload) < 11):
        return
    id = message.payload[0:4].decode("utf-8")
    wind_speed_hex = message.payload[7:9]
    wind_speed_int = int.from_bytes(wind_speed_hex, "big")
    wind_speed = decimal.Decimal(wind_speed_int) / 10
    data = [0] * 7
    data[0] = id
    data[1] = wind_speed
    insertDB(data)
    # print(message.payload)
    # print(datetime.datetime.now())

def process_message_speed_direction(message):
    if(len(message.payload) < 11):
        return
    id = message.payload[0:4].decode("utf-8")
    wind_speed_hex = message.payload[7:9]
    wind_speed_int = int.from_bytes(wind_speed_hex, "big")
    wind_speed = decimal.Decimal(wind_speed_int) / 100
    wind_direction_hex = message.payload[9:11]
    wind_direction = int.from_bytes(wind_direction_hex, "big")
    data = [0] * 7
    data[0] = id
    data[1] = wind_speed
    data[2] = wind_direction
    # print(message.payload)
    # print(data)    
    insertDB(data)

def connect_mqtt():
    def on_conncet(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    client = ct.Client()
    client.username_pw_set(username, passwd)
    client.on_connect = on_conncet
    client.connect(broker, port)
    return client

def on_message_speed(client, userdata, message):
    process_message_speed(message)

def on_message_speed_direction(client, userdate, message):
    process_message_speed_direction(message)

def on_message_power(client, userdate, message):
    process_message_power(message)

def on_message_power_v(client, userdate, message):
    process_message_power_v(message)

try:
    client_res_speed = connect_mqtt()
    client_res_speed.subscribe(topic_speed_res)
    client_res_speed.on_message = on_message_speed
    client_res_speed.loop_start()

    client_res_speed_direction = connect_mqtt()
    client_res_speed_direction.subscribe(topic_speed_direction_res)
    client_res_speed_direction.on_message = on_message_speed_direction
    client_res_speed_direction.loop_start()

    client_res_power = connect_mqtt()
    client_res_power.subscribe(topic_power_res)
    client_res_power.on_message = on_message_power
    client_res_power.loop_start()

    client_res_power = connect_mqtt()
    client_res_power.subscribe(topic_power_v_res)
    client_res_power.on_message = on_message_power_v
    client_res_power.loop_start()

    client_req = connect_mqtt()
    while(True):
        client_req.publish(topic_speed_req, hexstring_speed)
        client_req.publish(topic_speed_direction_req, hexstring_speed_direction)
        client_req.publish(topic_power_req, hexstring_power)
        client_req.publish(topic_power_v_req, hexstring_power_v)

        time.sleep(sleep)
        print(datetime.datetime.now())
except:
    pass