import paho.mqtt.client as mqtt
import os, datetime
import pandas as pd
import time
import numpy

topicPubIrradiation = "topics/station1/irradiation/raw"
topicPubTemperature = "topics/station1/temperature/raw"
topicPubPower = "topics/station1/power/raw"
format_date = "%Y:%m:%dT%H:%M:%S"
clientMQTT = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)


if __name__ == '__main__':
    df = pd.read_csv("/home/probaEmision.csv")
    clientMQTT.connect('172.18.0.99', 1883)
    for index, row in df.iterrows():
        # Publica Irradiacion
        msx = df.iloc[index][['DATE_TIME', 'IRRADIATION', 'DC_POWER', 'MODULE_TEMPERATURE']].values.reshape(-1,4)[0]
        msxIrr = msx[0] + "," + str(msx[1])
        msxPwr = msx[0] + ',' + str(msx[2])
        msxTmp = msx[0] + ',' + str(msx[3])
        print(msx)
        clientMQTT.publish(topicPubIrradiation, str(msxIrr))
        clientMQTT.publish(topicPubPower, str(msxPwr))
        clientMQTT.publish(topicPubTemperature, str(msxTmp))

        time.sleep(1)
