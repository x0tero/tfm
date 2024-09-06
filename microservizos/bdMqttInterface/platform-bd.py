from pymongo import MongoClient
import paho.mqtt.client as mqtt
import os, datetime
import pandas as pd


topicSubIrr = "topics/forecast_input_date"
topicSubPwr = "topics/forecast_input_date"
topicSubTmp = "topics/forecast_input_date"
format_date = "%Y:%m:%dT%H:%M:%S"
clientMQTT = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client = MongoClient("mongodb://admin:1234@172.18.0.117:27017")


def subscribe(client: mqtt):
    def on_message(clientMQTT, userdata, msx):
        data = msx.payload.decode().replace(" ","")
        dataArray = data.split("-")
        print(dataArray)
        startDate = datetime.datetime.strptime(dataArray[0], format_date)
        endDate = datetime.datetime.strptime(dataArray[1], format_date)
        cursor = client["test"]['solar'].find({"datetime": {"$lt": endDate,"$gte": startDate}, "unit": 1})

        queryDates = []; querySolar = []; queryTemperature = []
        for document in cursor:
            queryDates.append(document['datetime'])
            querySolar.append(document['value'])
            queryTemperature.append(document['temp'])

        df = pd.DataFrame({'date': queryDates, 'radiation': querySolar, 'temperature': queryTemperature})
        df.to_csv('output.csv', index=False, header=False)
        data = open("./output.csv", 'r').read()
        clientMQTT.publish('topics/forecast_input', str(data))
    clientMQTT.subscribe(topic)
    clientMQTT.on_message = on_message


if __name__ == '__main__':
    clientMQTT.connect('172.18.0.99', 1883)
    subscribe(client)
    clientMQTT.loop_forever()
