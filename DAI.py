import time
import random
import requests
import pandas as pd
import DAN
import paho.mqtt.client as mqtt
from occupancy_prediction import predict_occupancy as predict


ServerURL = 'http://120.108.111.234:9999'  # with non-secure connection
# ServerURL = 'https://DomainName' #with SSL connection
Reg_addr = None  # if None, Reg_addr = MAC address

DAN.profile['dm_name'] = 'sw_esp32' #新建iottalk裝置名稱
DAN.profile['df_list'] = ['sw_esp32_temp', 'sw_esp32_humi', 'sw_esp32_lux', 'sw_esp32_co2', 'sw_esp32_Occupancy']    #新建iottalk裝置Device_Feature名稱
DAN.profile['d_name'] = 'sw_esp32'  #這個裝置的名稱

DAN.device_registration_with_retry(ServerURL, Reg_addr)
# DAN.deregister()  #if you want to deregister this device, uncomment this line
# exit()            #if you want to deregister this device, uncomment this line


DAN.ControlChannel
det_humi = 0
det_temp = 0
det_Occupancy = 0
det_lux = 0
det_co2= 0



control_message = False


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # 將訂閱主題寫在on_connet中
    # 如果我們失去連線或重新連線時
    # 地端程式將會重新訂閱
 
    client.subscribe("pub/sw_esp32") #MQTT的Topic訂閱

# 當接收到從伺服器發送的訊息時要進行的動作


def on_message(client, userdata, msg):
    global det_Occupancy, det_temp, det_humi, det_lux, det_co2, control_message

    # 轉換編碼utf-8才看得懂中文

    message = msg.payload.decode('utf-8')
    print(msg.topic,message, type(message))

    #這個部分為以溫溼度為例子切出字串

    det_temp, det_humi, det_lux, det_co2 = map(float,message.split(','))
    # print(det_temp, det_humi, det_lux, det_co2)
    data = [det_temp, det_humi, det_lux, det_co2]
    det_Occupancy = float(predict(data))
    print(det_Occupancy)
    
    control_message = True


# 連線設定
# 初始化地端程式
client = mqtt.Client()

# 設定連線的動作
client.on_connect = on_connect

# 設定接收訊息的動作
client.on_message = on_message
print("client:", client.on_message)

# 設定登入帳號密碼
client.username_pw_set("test", "test")

# 設定連線資訊(IP, Port, 連線時間)
client.connect("120.108.111.227", 1883, 60)

# 開始連線，執行設定的動作和處理重新連線問題
# 也可以手動使用其他loop函式來進行連接

while True:
    if DAN.state == "RESUME":
        try:
            client.loop_start()
            if (control_message == True):
                # det_Occupancy, det_temp, det_humi, det_lux, det_co2
                # ['sw_esp32_temp', 'sw_esp32_humi', 'sw_esp32_lux', 'sw_esp32_co2', 'sw_esp32_Occupancy']    #新建iottalk裝置Device_Feature名稱

                DAN.push('sw_esp32_Occupancy', det_Occupancy)
                DAN.push('sw_esp32_temp', det_temp)
                DAN.push('sw_esp32_humi', det_humi)
                DAN.push('sw_esp32_lux', det_lux)
                DAN.push('sw_esp32_co2', det_co2)
                print('success')
                control_message = False
                print(control_message)
            # ==================================

            # # Pull data from an output device feature "Dummy_Control"
            # ODF_data = DAN.pull('Dummy_Control')
            # if ODF_data != None:
            #     print(ODF_data[0])

        except Exception as e:
            print(e)
            if str(e).find('mac_addr not found:') != -1:
                print('Reg_addr is not found. Try to re-register...')
                DAN.device_registration_with_retry(ServerURL, Reg_addr)
            else:
                print('Connection failed due to unknow reasons.')
                time.sleep(1)
    else:
        client.loop_stop()
