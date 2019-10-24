# -*- coding: utf8 -*-
from wifi import Cell, Scheme
from time import time
import time
from os.path import dirname, join
from flask import Flask, render_template
from flask import request
import socket               # Import socket module
import os,sys, threading, logging
import minimalmodbus
minimalmodbus.CLOSE_PORT_AFTER_EACH_CALL=True
import serial.tools.list_ports
import MySQLdb
import HC2,serialdecode
import json
import hashlib
#####################################################################################################
## Infor: 22/04/2017 Phạm An Nhàn Modbus Daikin V1.1                                          #######
## Status có thể trả về theo 2 hàm : TCP hoặc GET                                             #######
## TCP: port 10002: nội dung upload_daikin                                                    #######
## Get ta có thể GEt IP:8080/getinfor                                                         #######
## Chương trình được bảo mật bằng mã Serial của Raspberry nên mọi sự copy đều có thể gây lỗi   ######
#####################################################################################################
bientruyen=0
modbus_mod="rtu"
modbus_boudrate=9600
modbus_timeout=0.2
modbus_address=1
co_tinhieu_HC2=0
dangtuyenmodbus=0
dangtruyenmodbus_HC2=0
daikin_address = 2
############
## Bien cho ma hoa
##################
ma_serial=0     #Số đã mã hóa để so sánh
so_serial=1  #Số thực chất của Raspberry
dungmaserial=0
mahoa2="dsds"

############
## Bien cho Wifi
##################
ssid=""
wpa_password=""
wifi_ip_address="192.168.99.130"
wifi_ip_gateway="192.168.99.1"
infor_wifi_found=""
############
## Bien cho Wire NEtword
##################
ip_address="192.168.99.130"
ip_subnet="255.255.255.0"
ip_gateway="192.168.99.1"
############
## Bien cho HC2
##################
ip_HC2="192.168.99.10"
HC2_user="admin"
HC2_password="admin"
HC2_global1="Daikin"
HC2_global2="daikin"

time_begin=0
time_end=0
status_lock=-1

exit_popup_daikin=0
###########################
## GLobal Daikin ##########
###########################
daikinconnect=0
Daikin_last={
    "Zone1":{
        "Name":"P.Khach",
        "Using":0,
        "Status":0,
        "Temp":29,
        "Setpoint":20,
        "FanD":0,
        "FanVolume":0,
        "ForcudOFF":1
    },
    "Zone2": {
        "Name":"P.Khach",
        "Using":0,
        "Status": 0,
        "Temp": 29,
        "Setpoint": 20,
        "FanD": 0,
        "FanVolume": 0,
        "ForcudOFF": 1
    },
    "Zone3": {
        "Name":"P.Khach",
        "Using":0,
        "Status": 0,
        "Temp": 29,
        "Setpoint": 20,
        "FanD": 0,
        "FanVolume": 0,
        "ForcudOFF": 1
    },
    "Zone4": {
        "Name":"P.Khach",
        "Using":0,
        "Status": 0,
        "Temp": 56,
        "Setpoint": 20,
        "FanD": 0,
        "FanVolume": 0,
        "ForcudOFF": 1
    },
    "Zone5": {
        "Name":"P.Khach",
        "Using":1,
        "Status": 0,
        "Temp": 29,
        "Setpoint": 20,
        "FanD": 0,
        "FanVolume": 0,
        "ForcudOFF": 1
    },
    "Zone6": {
        "Name":"P.Khach",
        "Using":0,
        "Status": 0,
        "Temp": 29,
        "Setpoint": 20,
        "FanD": 0,
        "FanVolume": 0,
        "ForcudOFF": 1
    },
    "Zone7": {
        "Name":"P.Khach",
        "Using":0,
        "Status": 0,
        "Temp": 29,
        "Setpoint": 20,
        "FanD": 0,
        "FanVolume": 0,
        "ForcudOFF": 1
    },
    "Zone8": {
        "Name":"P.Khach",
        "Using":0,
        "Status": 0,
        "Temp": 29,
        "Setpoint": 20,
        "FanD": 0,
        "FanVolume": 0,
        "ForcudOFF": 1
    },
    "Zone9": {
        "Name":"P.Khach",
        "Using":0,
        "Status": 0,
        "Temp": 29,
        "Setpoint": 20,
        "FanD": 0,
        "FanVolume": 0,
        "ForcudOFF": 1
    },
    "Zone10": {
        "Name":"P.Khach",
        "Using":0,
        "Status": 0,
        "Temp": 29,
        "Setpoint": 20,
        "FanD": 0,
        "FanVolume": 0,
        "ForcudOFF": 1
    },
    "Zone11": {
        "Name":"P.Khach",
        "Using":0,
        "Status": 0,
        "Temp": 29,
        "Setpoint": 20,
        "FanD": 0,
        "FanVolume": 0,
        "ForcudOFF": 1
    },
    "Zone12": {
        "Name":"P.Khach",
        "Using":0,
        "Status": 0,
        "Temp": 29,
        "Setpoint": 20,
        "FanD": 0,
        "FanVolume": 0,
        "ForcudOFF": 1
    },
    "Zone13": {
        "Name":"P.Khach",
        "Using":0,
        "Status": 0,
        "Temp": 29,
        "Setpoint": 20,
        "FanD": 0,
        "FanVolume": 0,
        "ForcudOFF": 1
    },
    "Zone14": {
        "Name":"P.Khach",
        "Using":0,
        "Status": 0,
        "Temp": 29,
        "Setpoint": 20,
        "FanD": 0,
        "FanVolume": 0,
        "ForcudOFF": 1
    },
    "Zone15": {
        "Name":"P.Khach",
        "Using":0,
        "Status": 0,
        "Temp": 29,
        "Setpoint": 20,
        "FanD": 0,
        "FanVolume": 0,
        "ForcudOFF": 1
    },
    "Zone16": {
        "Name":"P.Khach",
        "Using":0,
        "Status": 0,
        "Temp": 29,
        "Setpoint": 20,
        "FanD": 0,
        "FanVolume": 0,
        "ForcudOFF": 1
    }
}
Daikin1={
    "Zone1":{
            "Name":"P.Khach",
            "Using":0,
            "Status":0,
            "Temp":29,
            "Setpoint":20,
            "FanD":0,
            "FanVolume":0,
            "ForcudOFF":1,
            "Mode":0
    },
    "Zone2": {
        "Name":"P.Khach",
        "Using":0,
        "Status": 0,
        "Temp": 29,
        "Setpoint": 20,
        "FanD": 0,
        "FanVolume": 0,
        "ForcudOFF": 1,
        "Mode": 0
    },
    "Zone3": {
        "Name":"P.Khach",
        "Using":0,
        "Status": 0,
        "Temp": 29,
        "Setpoint": 20,
        "FanD": 0,
        "FanVolume": 0,
        "ForcudOFF": 1,
        "Mode": 0
    },
    "Zone4": {
        "Name":"P.Khach",
        "Using":0,
        "Status": 0,
        "Temp": 56,
        "Setpoint": 20,
        "FanD": 0,
        "FanVolume": 0,
        "ForcudOFF": 1,
        "Mode": 0
    },
    "Zone5": {
        "Name":"P.Khach",
        "Using":0,
        "Status": 0,
        "Temp": 29,
        "Setpoint": 20,
        "FanD": 0,
        "FanVolume": 0,
        "ForcudOFF": 1,
        "Mode": 0
    },
    "Zone6": {
        "Name":"P.Khach",
        "Using":0,
        "Status": 0,
        "Temp": 29,
        "Setpoint": 20,
        "FanD": 0,
        "FanVolume": 0,
        "ForcudOFF": 1,
        "Mode": 0
    },
    "Zone7": {
        "Name":"P.Khach",
        "Using":0,
        "Status": 0,
        "Temp": 29,
        "Setpoint": 20,
        "FanD": 0,
        "FanVolume": 0,
        "ForcudOFF": 1,
        "Mode": 0
    },
    "Zone8": {
        "Name":"P.Khach",
        "Using":0,
        "Status": 0,
        "Temp": 29,
        "Setpoint": 20,
        "FanD": 0,
        "FanVolume": 0,
        "ForcudOFF": 1,
        "Mode": 0
    },
    "Zone9": {
        "Name":"P.Khach",
        "Using":0,
        "Status": 0,
        "Temp": 29,
        "Setpoint": 20,
        "FanD": 0,
        "FanVolume": 0,
        "ForcudOFF": 1,
        "Mode": 0
    },
    "Zone10": {
        "Name":"P.Khach",
        "Using":0,
        "Status": 0,
        "Temp": 29,
        "Setpoint": 20,
        "FanD": 0,
        "FanVolume": 0,
        "ForcudOFF": 1,
        "Mode": 0
    },
    "Zone11": {
        "Name":"P.Khach",
        "Using":0,
        "Status": 0,
        "Temp": 29,
        "Setpoint": 20,
        "FanD": 0,
        "FanVolume": 0,
        "ForcudOFF": 1,
        "Mode": 0
    },
    "Zone12": {
        "Name":"P.Khach",
        "Using":0,
        "Status": 0,
        "Temp": 29,
        "Setpoint": 20,
        "FanD": 0,
        "FanVolume": 0,
        "ForcudOFF": 1,
        "Mode": 0
    },
    "Zone13": {
        "Name":"P.Khach",
        "Using":0,
        "Status": 0,
        "Temp": 29,
        "Setpoint": 20,
        "FanD": 0,
        "FanVolume": 0,
        "ForcudOFF": 1,
        "Mode": 0
    },
    "Zone14": {
        "Name":"P.Khach",
        "Using":0,
        "Status": 0,
        "Temp": 29,
        "Setpoint": 20,
        "FanD": 0,
        "FanVolume": 0,
        "ForcudOFF": 1,
        "Mode": 0
    },
    "Zone15": {
        "Name":"P.Khach",
        "Using":0,
        "Status": 0,
        "Temp": 29,
        "Setpoint": 20,
        "FanD": 0,
        "FanVolume": 0,
        "ForcudOFF": 1,
        "Mode": 0
    },
    "Zone16": {
        "Name":"P.Khach",
        "Using":0,
        "Status": 0,
        "Temp": 29,
        "Setpoint": 20,
        "FanD": 0,
        "FanVolume": 0,
        "ForcudOFF": 1,
        "Mode": 0
    }
}


TRANSLATIONS = {
    'mode' : { #42002 Bit 0->4
        'FAN': 0,
        'COOKING': 2,
        'HEATING': 1,
        'AUTO': 3,
        'Setpoint': 6,
        'Sry': 7
    },
    'Setpoin':30,#42003
    'power' : { #42001 bit 0
        "OFF": 0,
        "ON": 1
    },
    'FANdirec' : { #42001 bit 8->10
        'P0': 0,
        'P1': 1,
        'P2': 2,
        'P3': 3,
        'P4': 4,
        'STOP': 6,
        'SWING': 7
    },
    'FANVOLUME' : { #42001 bit 12->14
        'LOW': 1,
        'MID': 3,
        'HIGH': 5
    }
}




################################################

db_update_network= "UPDATE Daikin SET mode = '%s' boudrate = '%d' slave_address='%d' timeout='%f'".format('rtu',modbus_boudrate,modbus_address,modbus_timeout)
db_update_modbus= "UPDATE Daikin SET mode = '%s' boudrate = '%d' slave_address='%d' timeout='%f'".format('rtu',modbus_boudrate,modbus_address,modbus_timeout)
############################################
## Server TCP ##############################
#############################################


class server(threading.Thread):
    global Daikin1
    global co_tinhieu_HC2
    def __init__(self):
        threading.Thread.__init__(self)
        self.PORTNO1=10002
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.s.bind(("0.0.0.0",self.PORTNO1))
        self.CONNECTION_LIST=[]
        self.RECV_BUFFER=4096
    def run(self):
        global bientruyen
        self.s.listen(5)
        _payload=""
        #MyPaintApp().run()
        while(1):
            try:
                bientruyen=bientruyen+1
                c,addr = self.s.accept()
                #print(addr)
                #print(c)
                try:
                    data=bytes.decode(c.recv(1024))
                    #print(data)
                    if "Reboot" in data:
                        os.system("sudo reboot")
                        _payload=b'Ket noi thanh cong !'
                    elif "upload_daikin":
                        _payload=Daikin1
                except:
                    data=""
                c.send(_payload)
                c.close()
            except:
                logging.warning('loi Port 10002')
                print ("loi port 10002")
########################################
## Ham Chuyen Doi Int to CharArray
#########################################
def int_to_chararray(value):
    try:
        value=int(value)
        return [(value >> (4 * i)) & 0x0f for i in range(3, -1, -1)]
    except:
        logging.warning('Chuyen doi int to array loi')
        return 0
def chararray_to_int(value0,value1,value2,value3):
    try:
        value0 = int(value0)
        value1 = int(value1)
        value2 = int(value2)
        value3 = int(value3)
        return (value3&0x000f) | (value2<<(4)&0x00f0) | (value1<<(8)&0x0f00) | (value0<<(12)&0xf000)
    except:
        logging.warning('Chuyen doi loi')
        return 0
#########################################################
############ KiVy
##################################################################

###########################
## Class Setting Ip Pgae
###########################

###############################
### Class control Daikin
##################################
## MAIN SCREEN ####################
###################################
#################################################################################################################
## Modbus ####################################################################################################
###############################################################################################################
class modbus(threading.Thread):
    global Daikin1,daikinconnect,co_tinhieu_HC2
    def __init__(self,Port,Slave_address,baudrate,timout):
        threading.Thread.__init__(self)
        print(Port, Slave_address, minimalmodbus.MODE_RTU)
        self.instrument = minimalmodbus.Instrument(Port, 1)
        minimalmodbus.CLOSE_PORT_AFTER_EACH_CALL = True
        print(baudrate)
        self.instrument.serial.baudrate = 9600 #baudrate
        self.instrument.serial.timeout = 1.2 #timout
        self.instrument.debug = False
        self.instrument.precalculate_read_size = True
        self.instrument.serial.bytesize = 8
        self.instrument.serial.parity = serial.PARITY_EVEN
        self.instrument.serial.stopbits = 1
        #self.instrument.debug = False
        #self.instrument.precalculate_read_size = True

    def run(self):
        _bientang=0
        print("Begin")
        global daikinconnect,dangtruyenmodbus_HC2,dangtuyenmodbus
        global co_tinhieu_HC2
        _reatime=0
        while (daikinconnect==0):
            daikinconnect = self.get_DTA_Ready()
            daikinconnect=1
            time.sleep(1)
        time.sleep(1)
        self.get_status_all()
        global bientruyen
        print("Ready")
        while(1):
            try:
                _bientang=_bientang+1
                time.sleep(0.1)
                if co_tinhieu_HC2==1:
                    time.sleep(1)
                    co_tinhieu_HC2=0
                    #get_input()
                    truyen_ve_HC()
                    _bientang = 1
                if _bientang % 200 == 0:
                    #while dangtuyenmodbus!=0:
                       # time.sleep(0.1)
                    tam = 0
                    while dangtuyenmodbus != 0:
                        tam = tam + 1
                        if tam > 100:
                            break
                        time.sleep(0.05)
                    get_input()
                if _bientang % 600 ==0:
                    truyen_ve_HC()
                    _bientang = 1
            except:
                logging.warning('Lpi Main')
                print("Loi Main")

    #######################
    ## Set Status HOlding Register

    ######################
    def set_status_forcusstatus_fandir_fanvolume(self, zone, status=503,forcus=503,fandir=503,fanvolume=503,SHC2=0):
        global co_tinhieu_HC2
        zone_new=zone
        _reset=0
        _status_old =0
        _for_cus_old=0
        _fan_dir_old=0
        _fanvolume_old=0
        try:
            zone = 2000 + 48 + (zone - 1) * 3
            print(zone,_status_old,_for_cus_old,_fan_dir_old,_fanvolume_old)
            infor = self.instrument.read_register(zone,  numberOfDecimals=0,functioncode=3)
            print "SET STATUS ",infor
            old_fanvolume,old_fandir,old_forcus,old_status =int_to_chararray(infor)
            print "DOC VE ",old_fanvolume,old_fandir,old_forcus,old_status
            if old_status!=Daikin1["Zone{}".format(zone_new)]["Status"]:
                _reset=1
                _status_old=Daikin1["Zone{}".format(zone_new)]["Status"]
            elif status==503:
                status=old_status
                _status_old=old_status
            if old_fandir != Daikin1["Zone{}".format(zone_new)]["FanD"]:
                _reset = 1
                _fan_dir_old = Daikin1["Zone{}".format(zone_new)]["FanD"]
            elif fandir==503:
                fandir=old_fandir
                _fan_dir_old=old_fandir
            if old_fanvolume != Daikin1["Zone{}".format(zone_new)]["FanVolume"]:
                _reset = 1
                _fanvolume_old = Daikin1["Zone{}".format(zone_new)]["FanVolume"]
            elif fanvolume==503:
                fanvolume=old_fanvolume
                _fanvolume_old=old_fanvolume
            if _reset==1:
                _datasend1 = chararray_to_int(_fanvolume_old, _fan_dir_old, 6, _status_old)
                self.instrument.write_register(zone, _datasend1, numberOfDecimals=0, functioncode=16)
                time.sleep(1)
            _datasend = chararray_to_int(fanvolume, fandir, 6, status)
            print(zone,_datasend)
	    Daikin1["Zone{}".format(zone_new)]["Status"]=status
            self.instrument.write_register(zone,_datasend ,numberOfDecimals=0, functioncode=16)
            print("OK SET STATUS")
        except:
            logging.warning('SET status')
            print ("loi set status")
        #if SHC2==1:
        co_tinhieu_HC2=1
    def set_tempset(self, zone, temp,SHC2=0):
        global co_tinhieu_HC2
        zone_new=zone
        try:
            zone = 2002+ 48 + (zone - 1) * 3
            #infor = self.instrument.read_register(zone, numberOfDecimals=0, functioncode=3)
            #infor=infor/10
            #if infor != Daikin1["Zone{}".format(zone_new)]["Setpoint"]:
            #    self.instrument.write_register(zone, Daikin1["Zone{}".format(zone_new)]["Setpoint"], functioncode=16)
            #    time.sleep(1)
            #print "Nhiet do",infor,temp
	    Daikin1["Zone{}".format(zone_new)]["Setpoint"]=temp/10
            self.instrument.write_register(zone, temp, functioncode=16)
        except:
            logging.warning('SET temp')
            print ("loi set nhiet do")
        #if SHC2==1:
        co_tinhieu_HC2=1
    def set_mode_filterreset_statusopera(self, zone, mode=503, filterreset=503, statusopera=503,SHC2=0):
        global co_tinhieu_HC2
        zone_new=zone
        _reset=0
        _mode_out=0
        try:
            #old_mode, old_filterreset, old_statusopera, old_none = self.get_mode_filter(zone)
            zone = 2001 + 48 + (zone - 1) * 3
            infor = self.instrument.read_register(zone,  numberOfDecimals=0,functioncode=3)
            old_none,old_statusopera,old_filterreset,old_mode =int_to_chararray(infor)
            if old_mode!=Daikin1["Zone{}".format(zone_new)]["Mode"]:
                _reset = 1
                _mode_out = Daikin1["Zone{}".format(zone_new)]["Mode"]
            elif mode == 503:
                mode = old_mode
                _mode_out=old_mode
            if filterreset == 503:
                filterreset = old_filterreset
            if statusopera == 503:
                statusopera = old_statusopera
            if _reset==1:
                _datasend1 = chararray_to_int(old_none, statusopera, filterreset, _mode_out)
                self.instrument.write_register(zone, _datasend1, numberOfDecimals=0, functioncode=16)
                time.sleep(0.5)
            _datasend=chararray_to_int(old_none,statusopera,filterreset,mode)
            self.instrument.write_register(zone, _datasend, numberOfDecimals=0,functioncode=16)
            print("OK SET MODE")
        except:
            logging.warning('SET MODE')
            print ("loi set mode")
        #if SHC2==1:
        co_tinhieu_HC2=1

    ################
    ## Get status INPUT
    ##############
    def get_status_forcusstatus_fandir_fanvolume(self, zone):
        try:
            zone1 = 2000 + 96 + (zone - 1) * 6
            infor=int(self.instrument.read_register(zone1, numberOfDecimals=0,functioncode=4))
            bien3=0
            bien4=0
            Daikin1["Zone{}".format(zone)]["FanVolume"],Daikin1["Zone{}".format(zone)]["FanD"],bien3,bien4=int_to_chararray(infor)
            Daikin1["Zone{}".format(zone)]["ForcudOFF"]=(bien4&0x04)>>2
            Daikin1["Zone{}".format(zone)]["Status"]=bien4&0x01
            return("OK")
        except:
            logging.warning('GET status')
            print ("loi get status")
            return ("error")
    def get_mode_filter(self, zone):
        try:
            zone_new = zone
            zone = 2001 + 96 + (zone - 1) * 6
            bien1,bien2,bien3=0,0,0
            infor=int(self.instrument.read_register(zone, numberOfDecimals=0,functioncode=4))
            bien1,bien2,bien3,Daikin1["Zone{}".format(zone_new)]["Mode"]=int_to_chararray(infor)
            return("OK")
        except:
            logging.warning('GET mode')
            print ("loi get mode")
            return ("error")
    def get_temproom(self,zone):
        try:
            zone_new=zone
            zone = 2004 + 96 + (zone - 1) * 6
            infor =self.instrument.read_register(zone,  numberOfDecimals=0,functioncode=4)
            Daikin1["Zone{}".format(zone_new)]["Temp"]=infor/10
            return("OK")
            #return(infor)
        except:
            logging.warning('GET temproom')
            print ("loi get temp")
            return ("error")
    def get_tempset(self,zone):
        try:
            zone_new = zone
            zone = 2002 + 96 +  (zone - 1) * 6
            infor =self.instrument.read_register(zone,functioncode=4)
            Daikin1["Zone{}".format(zone_new)]["Setpoint"] = infor/10
            return("OK")
        except:
            logging.warning('GET Tempset')
            print ("loi get tempset")
            return ("error")
#############################
## GET INFORMATION
##################################
    def get_status_all(self):
        try:
            _status_all=int(self.instrument.read_register(2, functioncode=4,signed=True))
            print (int(_status_all))
            i=5
            while i < 12:
                Daikin1["Zone{}".format(i)]["Using"] = (_status_all>>(i-1))&0x0001
                i += 1
        except:
            logging.warning('GET ALL STATUS')
            print ("loi_STATUS ALL")
            return ("error")

    def get_DTA_Ready(self):
        try:
            _status_all = self.instrument.read_register(0, functioncode=4)
            print "GET READY",int(_status_all)
            return((int(_status_all) & 0x0001))
        except:
            logging.warning('GET READY')
            print ("loi_READY")
            return (0)
######################
###hAm ###################################
######################
def get_input():
    global co_tinhieu_HC2,Daikin1,dangtuyenmodbus
    dangtuyenmodbus=1
    try:
	TCP_HC21.get_status_all()
        for i in range(5, 12):
            if Daikin1["Zone{}".format(i)]["Using"]==1:
                if dangtuyenmodbus==2:
                    dangtuyenmodbus=0
                    return(0)
                TCP_HC21.get_status_forcusstatus_fandir_fanvolume(i)
                if dangtuyenmodbus==2:
                    dangtuyenmodbus=0
                    return(0)
                TCP_HC21.get_mode_filter(i)
                #if dangtuyenmodbus==2:
                    #dangtuyenmodbus=0
                    #return(0)
                #TCP_HC21.get_temproom(i)
                if dangtuyenmodbus==2:
                    dangtuyenmodbus=0
                    return(0)
                TCP_HC21.get_tempset(i)
    except:
        logging.warning('GET INPUT')
        print("Loi Get INPUT")
    dangtuyenmodbus=0
def truyen_ve_HC():
    try:
	#print(Daikin1)
        hc2.setvariable("Daikin", Daikin1)
    except:
        logging.warning(' Truyen ve HC2')
        print("Loi truyen ve HC")
def serial_ports():
    try:
        ports = list(serial.tools.list_ports.comports())
        for port_no, description, address in ports:
	    print(description)
            if 'USB' in description:
                return port_no
        return ("NO")
    except:
        logging.warning('GET SERIAL ')
        return("NO")
def recv(data):
    dulieu=data
    if "Reboot" in dulieu:
        os.system("reboot")

##################################
##  WED SERVER ###################
##################################

app = Flask(__name__)
@app.route('/')
def trang_chu():
    return render_template('index.html',global3=Daikin1,name_zone1=Daikin1["Zone1"]["Name"], name_zone2=Daikin1["Zone2"]["Name"], name_zone3=Daikin1["Zone3"]["Name"], name_zone4=Daikin1["Zone4"]["Name"],name_zone5=Daikin1["Zone5"]["Name"],name_zone6=Daikin1["Zone6"]["Name"],name_zone7=Daikin1["Zone7"]["Name"],name_zone8=Daikin1["Zone8"]["Name"],name_zone9=Daikin1["Zone9"]["Name"],name_zone10=Daikin1["Zone10"]["Name"],name_zone11=Daikin1["Zone11"]["Name"],name_zone12=Daikin1["Zone12"]["Name"],name_zone13=Daikin1["Zone13"]["Name"],name_zone14=Daikin1["Zone14"]["Name"],name_zone15=Daikin1["Zone15"]["Name"],name_zone16=Daikin1["Zone16"]["Name"],_Using_zone1=Daikin1["Zone1"]["Using"], _Using_zone2=Daikin1["Zone2"]["Using"], _Using_zone3=Daikin1["Zone3"]["Using"], _Using_zone4=Daikin1["Zone4"]["Using"],_Using_zone5=Daikin1["Zone5"]["Using"],_Using_zone6=Daikin1["Zone6"]["Using"],_Using_zone7=Daikin1["Zone7"]["Using"],_Using_zone8=Daikin1["Zone8"]["Using"],_Using_zone9=Daikin1["Zone9"]["Using"],_Using_zone10=Daikin1["Zone10"]["Using"],_Using_zone11=Daikin1["Zone11"]["Using"],_Using_zone12=Daikin1["Zone12"]["Using"],_Using_zone13=Daikin1["Zone13"]["Using"],_Using_zone14=Daikin1["Zone14"]["Using"],_Using_zone15=Daikin1["Zone15"]["Using"],_Using_zone16=Daikin1["Zone16"]["Using"])

@app.route('/setmodbus', methods=['POST', 'GET'])
def set_modbus():
    global modbus_boudrate,modbus_timeout,modbus_address
    if request.method == 'POST':
        print(modbus_timeout)
        modbus_boudrate=request.form['html_Boudrate']
        modbus_address=request.form['html_slave_address']
        modbus_timeout=request.form['html_timeout']
        print(modbus_timeout)
        update_database("UPDATE Daikin SET mode='{}',boudrate={},slave_address={},timeout={}".format('rtu',modbus_boudrate,modbus_address,modbus_timeout))
        return "OK dsds"
    else:
        return render_template('set_modbus.html')
##################3
## Ham SET STATIC IP CHO PI
############################
def write_netword():
    global ip_address, ip_gateway, ip_subnet, wifi_ip_gateway, wifi_ip_address
    f = open("/etc/dhcpcd.conf", "r+")
    d = f.readlines()
    f.seek(0)
    for i in d:
        if "nohook lookup-hostname" in i:
            f.write(i)
            break
        else:
            f.write(i)
    f.write("\n")
    f.write("interface eth0\n")
    f.write("\n")
    f.write("static ip_address={}/24\n".format(ip_address))
    f.write("static routers={}\n".format(ip_gateway))
    f.write("static domain_nam_servers=8.8.8.8\n")
    f.write("\n")
    f.write("interface wlan0\n")
    f.write("\r\n")
    f.write("static ip_address={}/24\n".format(wifi_ip_address))
    f.write("static routers={}\n".format(wifi_ip_gateway))
    f.write("static domain_nam_servers=8.8.8.8\n")
    f.truncate()
    f.close()
###########################
## Ham lưu Wifi cho raspberry kết nối
#############################
def write_wifi():
    global ssid,wpa_password
    f = open("/etc/wpa_supplicant/wpa_supplicant.conf", "r+")
    d = f.readlines()
    f.seek(0)
    for i in d:
        if "network={" in i:
            f.write(i)
            break
        else:
            f.write(i)
    f.write("ssid=\"{}\"\n".format(ssid))
    f.write("scan_ssid=1\n")
    f.write("psk=\"{}\"\n".format(wpa_password))
    f.write("}\r\n")
    f.truncate()
    f.close()

@app.route('/setip', methods=['POST', 'GET'])
def set_ip():
    global ip_address,ip_gateway,ip_subnet,wifi_ip_gateway,wifi_ip_address
    if request.method == 'POST':
        if request.headers['Content-Type'] == 'application/json':
            return ("JSON Message:  Not Accept") #" + json.dumps(request.json + "
        ip_address_new,ip_subnet_new,ip_gateway_new=request.form['html_ip'],request.form['html_subnet'],request.form['html_gateway']
        if len(ip_address_new) < 7:
            print("Khong gia tri IP")
            return "Dia chi IP ngan"
        elif len(ip_gateway_new) < 7:
            print ("Khong gia tri Gateway")
            return "Dia chi gateway ngan"
        elif ip_address_new==wifi_ip_address:
            print("Trung Ip voi mnag Wifi")
            return "Error IP trung voi mang VLAN"
        else:
            ip_address,ip_subnet,ip_gateway=ip_address_new,ip_subnet_new,ip_gateway_new
            update_database("UPDATE infor_network SET ip='{}',gateway= '{}',subnet= '{}'".format(ip_address,ip_gateway,ip_subnet))
            write_netword()
        #os.system('sudo ifconfig eth0 down')
        #os.system('sudo ifconfig eth0 {}'.format(ip_address))
        #os.system('sudo ifconfig eth0 up')
            return "OK"
    else:
        return render_template('set_ip.html', ip=ip_address,gateway=ip_gateway,subnet=ip_subnet)
@app.route('/setmaso', methods=['POST', 'GET'])
def set_maso():
    global so_serial,ma_serial
    if request.method == 'POST':
        ma_tam = request.form['html_code']
        if len(ma_tam) < 20:
            print("Sai ma")
            return "NOT OK"
        else:
            ma_serial = ma_tam
            update_database("UPDATE Serial_Raspberry SET So_Serial='{}'".format(ma_serial))
            return "OK"
    else:
        return render_template('set_maso.html', uuid=so_serial,macode=ma_serial)

@app.route('/setwifi', methods=['POST', 'GET'])
def set_wifi():
    global ip_address,ip_gateway,ip_subnet,wpa_password,ssid,wifi_ip_address,wifi_ip_gateway,infor_wifi_found
    if request.method == 'POST':
        if request.headers['Content-Type'] == 'application/json':
            return ("JSON Message:  Not Accept") #" + json.dumps(request.json + "
        ssid_new,wpa_password_new,wifi_ip_address_new,wifi_ip_gateway_new=request.form['html_ssid'],request.form['html_wpa_password'],request.form['html_ip_wifi'],request.form['html_gateway_wifi']
        if wifi_ip_address_new==ip_address:
            print ("Dia chi trung IP voi Wire")
            return "Error IP trung voi mmang LAN"
        else:
            ssid,wpa_password,wifi_ip_address,wifi_ip_gateway=ssid_new,wpa_password_new,wifi_ip_address_new,wifi_ip_gateway_new
            update_database("UPDATE infor_network_wifi SET wifi_name='{}',wifi_password='{}',ip='{}',gateway= '{}'".format(ssid,wpa_password,wifi_ip_address,wifi_ip_gateway))
            write_netword()
            write_wifi()
            #os.system('sudo ifconfig eth0 down')
            #os.system('sudo ifconfig eth0 {}'.format(ip_address))
            #os.system('sudo ifconfig eth0 up')
            return "OK"
    else:
        infor_wifi_found = ssid_discovered()
        return render_template('set_wifi.html', ssid=ssid,wpa_pass=wpa_password,ip_wifi=wifi_ip_address,gateway_wifi=wifi_ip_gateway,infor_wifi_found=infor_wifi_found)

@app.route('/setHC2', methods=['POST', 'GET'])
def set_HC2():
    global ip_HC2,HC2_password,HC2_user,HC2_global1,HC2_global2
    if request.method == 'POST':
        if request.headers['Content-Type'] == 'application/json':
            return "JSON Message: " + json.dumps(request.json + " Not Accept")
        content = request.json
        ip_HC2,HC2_user,HC2_password,HC2_global1,HC2_global2=request.form['html_ipHC2'],request.form['html_user'],request.form['html_password'],request.form['html_global1'],request.form['html_global2']
        update_database("UPDATE HC2 SET ipHC2='{}',userHC2='{}',passwordHC2='{}',bien1_HC2= '{}',bien_HC2= '{}'".format(ip_HC2,HC2_user,HC2_password,HC2_global2,HC2_global1))
        return "OK"
    else:
        return render_template('set_HC2.html',ip=ip_HC2,userHC=HC2_user,PassHC2=HC2_password,glo1=HC2_global1,glo2=HC2_global2)
@app.route('/setZoneName', methods=['POST', 'GET'])
def set_ZoneName():
    global Daikin1
    if request.method == 'POST':
        Daikin1["Zone1"]["Name"], Daikin1["Zone2"]["Name"], Daikin1["Zone3"]["Name"], Daikin1["Zone4"]["Name"], Daikin1["Zone5"]["Name"], Daikin1["Zone6"]["Name"], Daikin1["Zone7"]["Name"], Daikin1["Zone8"]["Name"], Daikin1["Zone9"]["Name"], Daikin1["Zone10"]["Name"], Daikin1["Zone11"]["Name"], Daikin1["Zone12"]["Name"], Daikin1["Zone13"]["Name"], Daikin1["Zone14"]["Name"], Daikin1["Zone15"]["Name"], Daikin1["Zone16"]["Name"] = request.form['html_nameZone1'], request.form['html_nameZone2'], request.form['html_nameZone3'], request.form['html_nameZone4'], request.form['html_nameZone5'], request.form['html_nameZone6'], request.form['html_nameZone7'], request.form['html_nameZone8'], request.form['html_nameZone9'], request.form['html_nameZone10'], request.form['html_nameZone11'], request.form['html_nameZone12'], request.form['html_nameZone13'], request.form['html_nameZone14'], request.form['html_nameZone15'], request.form['html_nameZone16']
        update_database("UPDATE Name_Zone SET Zone1='{}',Zone2='{}',Zone3='{}',Zone4= '{}',Zone5= '{}',Zone6= '{}',Zone7= '{}',Zone8= '{}',Zone9= '{}',Zone10= '{}',Zone11= '{}',Zone12= '{}',Zone13= '{}',Zone14= '{}',Zone15= '{}',Zone16= '{}'".format(Daikin1["Zone1"]["Name"], Daikin1["Zone2"]["Name"], Daikin1["Zone3"]["Name"], Daikin1["Zone4"]["Name"], Daikin1["Zone5"]["Name"], Daikin1["Zone6"]["Name"], Daikin1["Zone7"]["Name"], Daikin1["Zone8"]["Name"], Daikin1["Zone9"]["Name"], Daikin1["Zone10"]["Name"], Daikin1["Zone11"]["Name"], Daikin1["Zone12"]["Name"], Daikin1["Zone13"]["Name"], Daikin1["Zone14"]["Name"], Daikin1["Zone15"]["Name"], Daikin1["Zone16"]["Name"]))
        return "OK"
    else:
        return render_template('set_ZoneName.html', name_zone1=Daikin1["Zone1"]["Name"], name_zone2=Daikin1["Zone2"]["Name"], name_zone3=Daikin1["Zone3"]["Name"], name_zone4=Daikin1["Zone4"]["Name"],name_zone5=Daikin1["Zone5"]["Name"],name_zone6=Daikin1["Zone6"]["Name"],name_zone7=Daikin1["Zone7"]["Name"],name_zone8=Daikin1["Zone8"]["Name"],name_zone9=Daikin1["Zone9"]["Name"],name_zone10=Daikin1["Zone10"]["Name"],name_zone11=Daikin1["Zone11"]["Name"],name_zone12=Daikin1["Zone12"]["Name"],name_zone13=Daikin1["Zone13"]["Name"],name_zone14=Daikin1["Zone14"]["Name"],name_zone15=Daikin1["Zone15"]["Name"],name_zone16=Daikin1["Zone16"]["Name"])

#####################################################
###### Thay doi ma Serial Lock ######################
#####################################################
@app.route('/setmaserial', methods=['POST', 'GET'])
def set_maserial():
    global ma_serial
    if request.method == 'POST':
        kien = json.loads(request.data)
        print(kien["maserial"])
        ma_serial = kien["maserial"]
        update_database("UPDATE Serial_Raspberry SET So_Serial='{}'".format(ma_serial))
        return "OK"
    else:
        return "Ma OK"
#################################
###### API HC2
#################################
@app.route('/getinfor', methods=['GET'])
def get_infor():
    data = json.dumps(Daikin1)
    return data
@app.route('/api/setup/temp', methods=['POST'])
def api_set_temp():
    global dangtuyenmodbus,dangtruyenmodbus_HC2,dungmaserial
    dangtruyenmodbus_HC2=1
    #co_tinhieu_HC2 = 1
    try:
        tam=0
        while dangtuyenmodbus!=0:
            dangtuyenmodbus=2
            tam = tam+1
            if tam>100:
                break
            time.sleep(0.1)
        _trave=request.data
        kien=json.loads(request.data)
        print(kien["zone"])
        TCP_HC21.set_tempset(int(kien["zone"]),int(kien["status"]),1)
        logging.info('INFO: HC2 SET TEMP {}'.format(request.data))
        if dungmaserial==1:
            return "FUCK YOU"
        else:
            return "OK"
    except:
        print "Loi API settemp"
        return "Error"
@app.route('/api/setup/status', methods=['POST'])
def api_set_status():
    global dangtuyenmodbus,dangtruyenmodbus_HC2,dungmaserial
    try:
        dangtruyenmodbus_HC2=1
        #co_tinhieu_HC2 = 1
        tam=0
        while dangtuyenmodbus!=0:
            dangtuyenmodbus=2
            tam = tam+1
            if tam>100:
                break
            time.sleep(0.1)
        _trave=request.data
        kien = json.loads(request.data)
        bien=0
        TCP_HC21.set_status_forcusstatus_fandir_fanvolume(int(kien["zone"]),kien["status"],503,503,503,1)
        logging.info('INFO: HC2 SET STATUS {}'.format(request.data))
        if dungmaserial==1:
            return "FUCK YOU"
        else:
            return "OK"
    except:
        print "Loi API Statua"
        return "Error"
@app.route('/api/setup/fandir', methods=['POST'])
def api_set_fandir():
    global dangtuyenmodbus,dangtruyenmodbus_HC2,dungmaserial
    try:
        dangtruyenmodbus_HC2=1
        #co_tinhieu_HC2 = 1
        tam=0
        while dangtuyenmodbus!=0:
            dangtuyenmodbus=2
            tam = tam+1
            if tam>100:
                break
            time.sleep(0.1)
        _trave=request.data
        kien = json.loads(request.data)
        TCP_HC21.set_status_forcusstatus_fandir_fanvolume(int(kien["zone"]),503,503,int(kien["status"]),503,1)
        logging.info('INFO: HC2 SET FANDIR {}'.format(request.data))
        if dungmaserial==1:
            return "FUCK YOU"
        else:
            return "OK"
    except:
        print "Loi API Fan"
        return "Error"
@app.route('/api/setup/fanvolume', methods=['POST'])
def api_set_fanvolume():
    global dangtuyenmodbus,dangtruyenmodbus_HC2,dungmaserial
    try:
        dangtruyenmodbus_HC2=1
        #co_tinhieu_HC2 = 1
        tam=0
        while dangtuyenmodbus!=0:
            dangtuyenmodbus=2
            tam = tam+1
            if tam>100:
                break
            time.sleep(0.1)
        kien = json.loads(request.data)
        TCP_HC21.set_status_forcusstatus_fandir_fanvolume(int(kien["zone"]),503,503,503,int(kien["status"]),1)
        logging.info('INFO: HC2 SET FANVOLUME {}'.format(request.data))
        if dungmaserial==1:
            return "FUCK YOU"
        else:
            return "OK"
    except:
        print "Loi API Volume"
        return "Error"
@app.route('/api/setup/mode', methods=['POST'])
def api_set_mode():
    global dangtuyenmodbus,dungmaserial
    dangtruyenmodbus_HC2 = 1
    #co_tinhieu_HC2 = 1
    try:
        tam=0
        while dangtuyenmodbus!=0:
            dangtuyenmodbus=2
            tam = tam+1
            if tam>100:
                break
            time.sleep(0.1)
        kien = json.loads(request.data)
        TCP_HC21.set_mode_filterreset_statusopera(int(kien["zone"]),int(kien["status"]),503,503,1)
        logging.info('INFO: HC2 SET MODE {}'.format(request.data))
        if dungmaserial==1:
            return "FUCK YOU"
        else:
            return "OK"
    except:
        print "Loi API Mode"
        return "Error"
#######################################################
## DataBase  #########################################
######################################################

TABLES_CREATE = {}
TABLES_CREATE['Daikin'] = (
        """CREATE TABLE Daikin(
         mode  CHAR(20) NOT NULL,
         boudrate  INT,
         slave_address INT,  
         timeout FLOAT)""")
TABLES_CREATE['infor_network'] = (
        """CREATE TABLE infor_network(
         ip  CHAR(20) NOT NULL,
         gateway  CHAR(16),
         subnet  CHAR(16),
         wifi_name CHAR(30),  
         wifi_password CHAR(60))""")
TABLES_CREATE['infor_network_wifi'] = (
        """CREATE TABLE infor_network_wifi(
         ip  CHAR(20) NOT NULL,
         gateway  CHAR(16),
         subnet  CHAR(16),
         wifi_name CHAR(30),  
         wifi_password CHAR(60))""")
TABLES_CREATE['HC2'] = (
        """CREATE TABLE HC2(
         ipHC2  CHAR(20) NOT NULL,
         userHC2  CHAR(50),
         passwordHC2  CHAR(50),
         bien1_HC2 CHAR(16),
         bien_HC2 CHAR(16))""")
TABLES_CREATE['Name_Zone'] = (
        """CREATE TABLE Name_Zone(
         Zone1  CHAR(20) NOT NULL,
         Zone2  CHAR(20),
         Zone3  CHAR(20),
         Zone4  CHAR(20),
         Zone5  CHAR(20),
         Zone6  CHAR(20),
         Zone7  CHAR(20),
         Zone8  CHAR(20),
         Zone9  CHAR(20),
         Zone10  CHAR(20),
         Zone11  CHAR(20),
         Zone12  CHAR(20),
         Zone13  CHAR(20),
         Zone14  CHAR(20),
         Zone15  CHAR(20),
         Zone16  CHAR(20))""")
TABLES_CREATE['Serial_Raspberry'] = (
        """CREATE TABLE Serial_Raspberry(
         So_Serial  CHAR(50) NOT NULL)""")
TABLES_INSERT = {}
TABLES_INSERT['Daikin'] = (
        "INSERT INTO Daikin(mode,boudrate,slave_address,timeout) VALUES ('%s','%d','%d','%f')"%('rtu', modbus_boudrate, modbus_address, modbus_timeout))
TABLES_INSERT['infor_network'] = (
        "INSERT INTO infor_network(ip,gateway,subnet,wifi_name,wifi_password) VALUES ('%s','%s','%s','%s','%s')"%(ip_address, ip_gateway, ip_subnet, 'mHomeBH','123789456'))
TABLES_INSERT['infor_network_wifi'] = (
        "INSERT INTO infor_network_wifi(ip,gateway,subnet,wifi_name,wifi_password) VALUES ('%s','%s','%s','%s','%s')"%(wifi_ip_address, wifi_ip_gateway, ip_subnet, 'mHomeBH','123789456'))

TABLES_INSERT['HC2'] = (
        "INSERT INTO HC2(ipHC2,userHC2,passwordHC2,bien1_HC2,bien_HC2) VALUES ('%s','%s','%s','%s','%s')"%("192.168.99.10", "admin", "chotronniemvui", "Daikin1","Daikin2"))
TABLES_INSERT['Name_Zone'] = (
        "INSERT INTO Name_Zone(Zone1,Zone2,Zone3,Zone4,Zone5,Zone6,Zone7,Zone8,Zone9,Zone10,Zone11,Zone12,Zone13,Zone14,Zone15,Zone16) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%("None","None","None","None","None","None","None","None","None","None","None","None","None","None","None","None"))
TABLES_INSERT['Serial_Raspberry'] = (
        "INSERT INTO Serial_Raspberry(So_Serial) VALUES ('%s')"%("00000000aee33ffb"))

def load_database():
    global Daikin1,ma_serial,wifi_ip_gateway,wifi_ip_address,ssid,wpa_password
    global modbus_timeout,modbus_address,modbus_boudrate,ip_gateway,ip_address,ip_subnet,ip_HC2,HC2_user,HC2_password,HC2_global1,HC2_global2
    db = MySQLdb.connect("localhost", "root", "root", "Daikin")
    cursor = db.cursor()
    for name, ddl in TABLES_CREATE.iteritems():
        print(name)
        try:

            cursor.execute(ddl)
            db.commit()
            cursor.execute(TABLES_INSERT[name])
            db.commit()
            print("Creating table {}: ".format(name))
        except :
            db.rollback()
            sql = "SELECT * FROM {}".format(name)
            cursor.execute(sql)
            results = cursor.fetchall()
            variable_loadata=0
            for row in results:
                if name=="Daikin":
                    modbus_boudrate,modbus_address,modbus_timeout=int(row[1]),int(row[2]),row[3]
                elif name=="HC2":
                    ip_HC2, HC2_user, HC2_password,HC2_global1,HC2_global2 = row[0], row[1], row[2], row[3], row[4]
                elif name=="Name_Zone":
                    Daikin1["Zone1"]["Name"],Daikin1["Zone2"]["Name"],Daikin1["Zone3"]["Name"],Daikin1["Zone4"]["Name"],Daikin1["Zone5"]["Name"],Daikin1["Zone6"]["Name"],Daikin1["Zone7"]["Name"],Daikin1["Zone8"]["Name"],Daikin1["Zone9"]["Name"],Daikin1["Zone10"]["Name"],Daikin1["Zone11"]["Name"],Daikin1["Zone12"]["Name"],Daikin1["Zone13"]["Name"],Daikin1["Zone14"]["Name"],Daikin1["Zone15"]["Name"],Daikin1["Zone16"]["Name"] = row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15]
                    print (Daikin1["Zone1"]["Name"],Daikin1["Zone2"]["Name"],Daikin1["Zone3"]["Name"],Daikin1["Zone4"]["Name"],Daikin1["Zone5"]["Name"],Daikin1["Zone6"]["Name"],Daikin1["Zone7"]["Name"],Daikin1["Zone8"]["Name"],Daikin1["Zone9"]["Name"],Daikin1["Zone10"]["Name"],Daikin1["Zone11"]["Name"],Daikin1["Zone12"]["Name"],Daikin1["Zone13"]["Name"],Daikin1["Zone14"]["Name"],Daikin1["Zone15"]["Name"],Daikin1["Zone16"]["Name"])
                elif name=="Serial_Raspberry":
                    ma_serial = row[0]
                    print "Ma serial ",ma_serial
                elif name=="infor_network_wifi":

                    wifi_ip_address, wifi_ip_gateway, ssid, wpa_password = row[0], row[1], row[3], row[4]
                    print " WIFI " ,wifi_ip_address, wifi_ip_gateway, ssid, wpa_password
                else:
                    ip_address,ip_subnet,ip_gateway=row[0],row[2],row[1]
                variable_loadata=variable_loadata+1
            if variable_loadata==0:
                print("Inser table {}: ".format(name))
                cursor.execute(TABLES_INSERT[name])
                db.commit()
        db.commit()
    db.close()
def delete_db():
    db = MySQLdb.connect("localhost", "root", "root", "Daikin")
    cursor = db.cursor()
    for name, ddl in TABLES_CREATE.iteritems():
        try:
            print("Delete table {}: ".format(name))
            sql = "DROP TABLE {};".format(name)
            cursor.execute(sql)
            db.commit()
        except:
            logging.warning('Delete Database Error')
            print("already exists.")
            db.rollback()
    db.close()
def update_database(table):
    db = MySQLdb.connect("localhost", "root", "root", "Daikin")
    cursor = db.cursor()
    try:
        print(table)
        cursor.execute("SET SQL_SAFE_UPDATES = 0")
        cursor.execute(table)
        cursor.execute("SET SQL_SAFE_UPDATES = 1")
        db.commit()
        print(table)
    except:
        logging.warning('Update Database Error')
        print("already exists.")
        db.rollback()
    db.close()
###################################
## MAIN ##########################
####################################
def getserial():
    # Extract serial from cpuinfo file
    cpuserial = "0000000000000000"
    try:
        f = open('/proc/cpuinfo', 'r')
        for line in f:
            if line[0:6] == 'Serial':
                cpuserial = line[10:26]
        f.close()
    except:
        cpuserial = "ERROR000000000"
    return cpuserial
#####################################
def ssid_discovered():
    try:
    	Cells = Cell.all('wlan0')
    	wifi_info = ''
    	for current in range(len(Cells)):
        	wifi_info +=  Cells[current].ssid + "\n"
    	wifi_info+="!"
    	print wifi_info
    	return wifi_info
    except:
	print "wifi discovered error"
	return "wifi discovered error, pls check manual"
########################################
####################################
if __name__ == '__main__':
    with open('Daikin.log', 'w'):
        pass
    logging.basicConfig(filename='Daikin.log', level=logging.DEBUG)
    logging.debug('Daikin begin')
    bien = serial_ports()
    while bien=="NO":
        bien = serial_ports()
	print("Khong co Serial")
	time.sleep(10)
    #delete_db()
    load_database()
    so_serial=getserial()
    mahoa1=hashlib.md5(so_serial).hexdigest()
    mahoa2=hashlib.md5(mahoa1).hexdigest()
    logging.debug('Daikin begin')
    infor_wifi_found=ssid_discovered()
    print "NHAN",mahoa2
    print(so_serial,ma_serial)
    print(len(str(mahoa2)),len(str(ma_serial)))
    if str(ma_serial) == str(mahoa2):
        #print("dung serial")
        TCP_HC21 = modbus(serial_ports(),modbus_address,modbus_boudrate,modbus_timeout)
        TCP_HC21.start()
    else:
        #print("Sai Serial")
        TCP_HC21 = modbus(serial_ports(),123,9600,modbus_timeout)
        TCP_HC21.start()
        dungmaserial=1
    hc2 = HC2.hc2(HC2_user, HC2_password, ip_HC2)
    TCP_HC2 = server()
    TCP_HC2.start()
    #KivyCatalogApp().run()
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host='0.0.0.0',port=8080,debug=True,use_reloader=False)