import paho.mqtt.client as mqtt
import os, datetime
import pandas as pd
import joblib
import numpy as np

topicSubIrradiation = "topics/station1/irradiation/raw"
topicSubPower = "topics/station1/power/raw"
topicSubTemperature = "topics/station1/temperature/raw"

topicPubIrradiation = "topics/station1/irradiation/processed"
topicPubPower = "topics/station1/power/processed"
topicPubTemperature = "topics/station1/temperature/processed"
format_date = "%Y:%m:%dT%H:%M:%S"
clientMQTT = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)


listTemperature = []
listPower = []
listIrradiation = []
model = joblib.load('/home/model/isolation_forest_model.pkl')


def subscribe(client: mqtt):
    # Se recibimos mensaxe cargamos o modelo de anomalias e publicamos
    def on_message(clientMQTT, userdata, msx):
        #data = msx.kpayload.decode().replace(" ","")
        topic = msx.topic
        data = msx.payload.decode()
        fecha = data.split(",")[0]

        if topic == topicSubIrradiation:
            irradiacion = float(data.split(",")[1])
            listIrradiation.append((fecha,irradiacion))
        elif topic == topicSubPower:
            power = float(data.split(",")[1])
            listPower.append((fecha,power))
        elif topic == topicSubTemperature:
            temperature = float(data.split(",")[1])
            listTemperature.append((fecha,temperature))

        if listTemperature and listPower and listIrradiation:
            # Compruebas si recibiste todos los datos e realizas a deteccion de anomalias
            if (fecha == listTemperature[-1][0]) and (fecha == listPower[-1][0]) and(fecha == listIrradiation[-1][0]):
                x = np.array([[listTemperature[-1][1], listPower[-1][1], listIrradiation[-1][1]]])
                res = model.predict(x)
                print("Anomalo dato (temp: " + str(listTemperature[-1][1]) + ", potencia: " + str(listPower[-1][1]) + ", irradiacion: " + str(listIrradiation[-1][1]) + ") = " + str(res))
                if res[0] == -1:
                    msxI = str(fecha) + ",-1"
                    msxP = str(fecha) + ",-1"
                    msxT = str(fecha) + ",-1"
                else:
                    msxI = str(fecha) + "," + str(listIrradiation[-1][1])
                    msxP = str(fecha) + "," + str(listPower[-1][1])
                    msxT = str(fecha) + "," + str(listTemperature[-1][1])
                clientMQTT.publish(topicPubIrradiation, msxI)
                clientMQTT.publish(topicPubPower, msxP)
                clientMQTT.publish(topicPubTemperature, msxT)
            

            
    clientMQTT.subscribe(topicSubIrradiation)
    clientMQTT.subscribe(topicSubPower)
    clientMQTT.subscribe(topicSubTemperature)
    clientMQTT.on_message = on_message


if __name__ == '__main__':
    clientMQTT.connect('172.18.0.99', 1883)
    subscribe(clientMQTT)
    clientMQTT.loop_forever()
