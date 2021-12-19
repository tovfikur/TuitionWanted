from time import sleep
import serial
from curses import ascii
import socket
import threading

'''Run this file in your shell, the aim for this script is to try and allow you to
    send, read and delete messages from python, after playing around with this for a while i have
    realised that the most importain thing is good signal strength at the modem. For a full list of
    fuctions that a GSM modem is capable of google Haynes AT+ commands

    I have put the sleep function into many of the functions found within this script as it give the modem time
    to receive all the messages from the Mobile Network Operators servers'''

##set serial
ser = serial.Serial()

##Set port connection to USB port GSM modem
ser.port = '/dev/ttyUSB0'

## set older phones to a baudrate of 9600 and new phones and 3G modems to 115200
##ser.baudrate = 9600
ser.baudrate = 115200
ser.timeout = 1
ser.open()
ser.write('AT+CMGF=1\r\n'.encode())
##following line of code sets the prefered message storage area to modem memory
ser.write('AT+CPMS="ME","SM","ME"\r\n'.encode())


## Important understand the difference between PDU and text mode, in PDU istructions are sent to the port as numbers eg: 0,1,2,3,4 and in TEXT mode as text eg: "ALL", "REC READ" etc
## following line sets port into text mode, all instructions have to be sent to port as text not number
##Important positive responses from the modem are always returned as OK

##you may want to set a sleep timer between sending texts of a few seconds to help the system process

def sendsms(number, text):
    ser.write('AT+CMGF=1\r\n'.encode())
    sleep(2)
    ser.write(('AT+CMGS="%s"\r\n' % number).encode())
    sleep(2)
    ser.write(('%s' % text).encode())
    sleep(2)
    ser.write(ascii.ctrl('z').encode())
    print("Text: %s  \nhas been sent to: %s" % (text, number))


def read_all_sms():
    ser.write('AT+CMGF=1\r\n'.encode())
    sleep(5)
    ser.write('AT+CMGL="ALL"\r\n'.encode())
    sleep(15)
    a = ser.readlines()
    z = []
    y = []
    for x in a:
        if x.startswith('+CMGL:'):
            r = a.index(x)
            t = r + 1
            z.append(r)
            z.append(t)
    for x in z:
        y.append(a[x])

    ## following line changes modem back to PDU mode
    ser.write('AT+CMGF=0\r\n'.encode())
    return y


def read_unread_sms():
    ser.write('AT+CMGF=1\r\n')
    sleep(5)
    ser.write('AT+CMGL="REC UNREAD"\r\n')
    sleep(15)
    a = ser.readlines()
    z = []
    y = []
    for x in a:
        if x.startswith('+CMGL:'):
            r = a.index(x)
            t = r + 1
            z.append(r)
            z.append(t)
    for x in z:
        y.append(a[x])

    ##Following line changed modem back to PDU mode
    ser.write('AT+CMGF=0\r\n')
    return y


def read_read_sms():
    ##returns all unread sms's on your sim card
    ser.write('AT+CMGS=1\r\n')
    ser.read(100)
    ser.write('AT+CMGL="REC READ"\r\n')
    ser.read(1)
    a = ser.readlines()
    for x in a:
        print(x)


def delete_all_sms():
    ##this changes modem back into PDU mode and deletes all texts then changes modem back into text mode
    ser.write('AT+CMGF=0\r\n')
    sleep(5)
    ser.write('AT+CMGD=0,4\r\n')
    sleep(5)
    ser.write('AT+CMGF=1\r\n')


def delete_read_sms():
    ##this changes modem back into PDU mode and deletes read texts then changes modem back into text mode
    ser.write('AT+CMGF=0\r\n')
    sleep(5)
    ser.write('AT+CMGD=0,1\r\n')
    sleep(5)
    ser.write('AT+CMGF=1\r\n')


##this is an attempt to run ussd commands from the gsm modem

def check_ussd_support():
    ##if return from this is "OK" this phone line supports USSD, find out the network operators codes
    ser.write(b'AT+CMGF=0\r\n')
    ser.write(b'AT+CUSD=?\r\n')
    ser.write(b'AT+CMGF=1\r\n')


##This function is an attempt to get your sim airtime balance using USSD mode
def get_balance():
    ##first set the modem to PDU mode, then pass the USSD command(CUSD)=1, USSD code eg:*141# (check your mobile operators USSD numbers)
    ## Error may read +CUSD: 0,"The service you requested is currently not available.",15
    ## default value for <dcs> is 15 NOT 1
    ser.write(b'AT+CMGF=0\r\n')
    ser.write(b'AT+CUSD=1,*123#,15\r\n')
    ser.read(1)
    a = ser.readlines()
    print(a)
    ser.write(b'AT+CMGF=1\r\n')


def ussd_sms_check():
    ##first set the modem to PDU mode, then pass the USSD command(CUSD)=1, USSD code eg:*141# (check your mobile operators USSD numbers)
    ser.write(b'AT+CMGF=0\r\n')
    ser.write(b'AT+CUSD=1,*123#,15\r\n')
    ser.read(100)
    a = ser.readlines()
    print(a)
    ser.write(b'AT+CMGF=1\r\n')


def re_send():
    sendsms(input('Type number : '), input('Type massage : '))
    re_send()


bind_ip = '127.0.0.1'
bind_port = 9994

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind_ip, bind_port))
server.listen(5)  # max backlog of connections

print('Listening on {}:{}'.format(bind_ip, bind_port))


def handle_client_connection(client_socket):
    request = client_socket.recv(1024)
    print(str(request).split("'")[1].split('::'))
    tr = str(request).split("'")[1].split('::')[1]
    print('\n'.join(tr.split('\\n')))
    sendsms(str(request).split("'")[1].split('::')[0], str('\n'.join(tr.split('\\n'))))
    client_socket.send(b'ACK!')
    client_socket.close()

while True:
    client_sock, address = server.accept()
    print('Accepted connection from {}:{}'.format(address[0], address[1]))
    client_handler = threading.Thread(
        target=handle_client_connection,
        args=(client_sock,)  # without comma you'd get a... TypeError: handle_client_connection() argument after * must be a sequence, not _socketobject
    )
    client_handler.start()
