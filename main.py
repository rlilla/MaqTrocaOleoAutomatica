import eel
from paho.mqtt import client as mqtt_client
import threading
import json

#Servidor MQTT
broker = "broker.mqtt-dashboard.com"

#Inicializa o caminho da pasta onde estao os arquivos da pagina web
eel.init('web')

#Criar a instancia do cliente MQTT
client = mqtt_client.Client("smartLub-Python")

#Conecta ao broker
client.connect(broker, 1883)

#Variaveis globais
global valAtual
global x
x=0
valAtual = ""

#Funcao para publicar os comandos MQTT
@eel.expose
def publicaComandos(valor):
    client.publish("smartlub/mqtt/comandos", json.dumps(valor))

#Funcao para publicar os parametros
@eel.expose
def publicaParametros(valor):
    client.publish("smartlub/mqtt/parametros", json.dumps(valor))

#Funcao para criar o callback de quando recebe mensagens
@eel.expose
def conectar():
    client.on_message = on_message

#Funcao para enviar o valor atual para o Javascript
@eel.expose
def valorAtual():
    global valAtual
    if valAtual:
        valAtualDict = json.loads(valAtual)
        return valAtualDict

#Funcao callback para quando recebe mensagens MQTT
def on_message(client, userdata, msg):
    global valAtual
    global x
    valAtual=str(msg.payload.decode())

#Subscreve ao topico para receber valores atuais do ESP32
client.subscribe("smartlub/mqtt/atual")

#Loop MQTT
def loopMQTT():
    client.loop_forever()

#Criacao de Thread para que MQTT rode em paralelo com o servidor web
th=threading.Thread(target=loopMQTT)
th.start()

#Inicia o servidor web e mostra a pagina HTML
eel.start('MQTT.html')