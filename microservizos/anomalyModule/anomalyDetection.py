from pymongo import MongoClient
import paho.mqtt.client as mqtt
import os, datetime
import pandas as pd

topicSub = "topics/station1/irradiation/raw"
topicPub = "topics/station1/irradiation/processed"
format_date = "%Y:%m:%dT%H:%M:%S"
clientMQTT = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)


def subscribe(client: mqtt):
    # Se recibimos mensaxe pasamos o modelo de anomalias e publicamos
    def on_message(clientMQTT, userdata, msx):
        #data = msx.payload.decode().replace(" ","")
        data = msx.payload.decode()
        fecha = data.split(",")[0]
        irradiacion = float(data.split(",")[1])
        clientMQTT.publish(topicPub, df.to_string())
        with open('model/isolation_forest_model.pkl', 'rb') as file:
            dt_object = datetime.strptime(datetime_string, "%Y-%m-%d %H:%M:%S")
            hora = dt_object.hour
            mes = dt_object.month
            X = pd.DataFrame({
                'Mes': [mes],
                'Hora': [hora],
                'G(i)': [irradiacion]
            })
            model = pickle.load(file)
            Y = model.predict(X)
            print("dato: " + str(irradiacion) + "  anomalia: " + str(Y))
    
    clientMQTT.subscribe(topicSub)
    clientMQTT.on_message = on_message


if __name__ == '__main__':
    clientMQTT.connect('172.18.0.99', 1883)
    subscribe(client)
    clientMQTT.loop_forever()
