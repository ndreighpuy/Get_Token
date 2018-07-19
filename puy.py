# -*- coding: utf-8 -*-

#  「 From Helloworld+Eater/ Edited by Puy 」 "
#The Beginning of this Bot Comes from Helloworld, I'm just Reworked This!
#Of Course Special Thanks To HelloWorld, And the Friends Around Me!
#ID : yapuy

from PUY.linepy import *
from PUY.akad.ttypes import Message
from PUY.akad.ttypes import ContentType as Type
from time import sleep
from datetime import datetime, timedelta
from googletrans import Translator
from humanfriendly import format_timespan, format_size, format_number, format_length
import time, random, sys, json, codecs, subprocess, threading, glob, re, string, os, requests, six, ast, pytz, urllib, urllib3, urllib.parse, traceback, atexit

#puy = LINE() 
#puy = LINE("PUT YOUR TOKEN HERE")    # UNTUK LOGIN TOKEN #
puy = LINE('')      # UNTUK LOGIN MAIL LINE #
puyMid = puy.profile.mid
puyProfile = puy.getProfile()
puySettings = puy.getSettings()
puyPoll = OEPoll(puy)
botStart = time.time()

msg_dict = {}

Owner = ["uac8e3eaf1eb2a55770bf10c3b2357c33","u33ba9a93d30c1be155df24f5d4e3f583"]
Admin =["uac8e3eaf1eb2a55770bf10c3b2357c33","u33ba9a93d30c1be155df24f5d4e3f583"]

settings = {
    "autoJoin": True,
    "autoLeave": False,
    "Inroom": True,
    "Outroom": True,
    "timeRestart": "18000",
    "changeGroupPicture": [],
    "limit": 50,
    "limits": 50,
    "wordban": [],
    "keyCommand": "",
    "myProfile": {
        "displayName": "",
        "coverId": "",
        "pictureStatus": "",
        "statusMessage": ""
    },
    "prefix": False
}

read = {
    "ROM": {},
    "readPoint": {},
    "readMember": {},
    "readTime": {}
}

try:
    with open("Log_data.json","r",encoding="utf_8_sig") as f:
        msg_dict = json.loads(f.read())
except:
    print("PUY")

adminOpen = codecs.open("Admin.json","r","utf-8")
ownerOpen = codecs.open("Owner.json","r","utf-8")

settings["myProfile"]["displayName"] = puyProfile.displayName
settings["myProfile"]["statusMessage"] = puyProfile.statusMessage
settings["myProfile"]["pictureStatus"] = puyProfile.pictureStatus
coverId = puy.getProfileDetail()["result"]["objectId"]
settings["myProfile"]["coverId"] = coverId

def restartBot():
    print ("[ INFO ] BOT RESTART")
    python = sys.executable
    os.execl(python, python, *sys.argv)

def autoRestart():
    if time.time() - botStart > int(settings["timeRestart"]):
        time.sleep(5)
        restartBot()
        
def sendMentionFooter(to, text="", mids=[]):
    arrData = ""
    arr = []
    mention = "@Meka Finee "
    if mids == []:
        raise Exception("Invalid mids")
    if "@!" in text:
        if text.count("@!") != len(mids):
            raise Exception("Invalid mids")
        texts = text.split("@!")
        textx = ""
        for mid in mids:
            textx += str(texts[mids.index(mid)])
            slen = len(textx)
            elen = len(textx) + 15
            arrData = {'S':str(slen), 'E':str(elen - 4), 'M':mid}
            arr.append(arrData)
            textx += mention
        textx += str(texts[len(mids)])
    else:
        textx = ""
        slen = len(textx)
        elen = len(textx) + 15
        arrData = {'S':str(slen), 'E':str(elen - 4), 'M':mids[0]}
        arr.append(arrData)
        textx += mention + str(text)
    puy.sendMessage(to, textx, {'AGENT_NAME':'@Muh.khadaffy on Instagram', 'AGENT_LINK': 'https://www.instagram.com/muh.khadaffy', 'AGENT_ICON': "http://dl.profile.line-cdn.net/" + puy.getProfile().picturePath, 'MENTION': str('{"MENTIONEES":' + json.dumps(arr) + '}')}, 0)    
    #'AGENT_LINK': 'line://ti/p/~{}'.format(puy.getProfile().userid),
    
def sendMessageWithFooter(to, text, name, url, iconlink):
        contentMetadata = {
            'AGENT_NAME': name,
            'AGENT_LINK': url,
            'AGENT_ICON': iconlink
        }
        return puy.sendMessage(to, text, contentMetadata, 0)
    
def cTime_to_datetime(unixtime):
    return datetime.fromtimestamp(int(str(unixtime)[:len(str(unixtime))-3]))
def dt_to_str(dt):
    return dt.strftime('%H:%M:%S')

def delete_log():
    ndt = datetime.now()
    for data in msg_dict:
        if (datetime.utcnow() - cTime_to_datetime(msg_dict[data]["createdTime"])) > timedelta(1):
            if "path" in msg_dict[data]:
                puy.deleteFile(msg_dict[data]["path"])
            del msg_dict[data]
            
def sendMention(to, text="", mids=[]):
    arrData = ""
    arr = []
    mention = "@zeroxyuuki "
    if mids == []:
        raise Exception("Invalid mids")
    if "@!" in text:
        if text.count("@!") != len(mids):
            raise Exception("Invalid mids")
        texts = text.split("@!")
        textx = ""
        for mid in mids:
            textx += str(texts[mids.index(mid)])
            slen = len(textx)
            elen = len(textx) + 15
            arrData = {'S':str(slen), 'E':str(elen - 4), 'M':mid}
            arr.append(arrData)
            textx += mention
        textx += str(texts[len(mids)])
    else:
        textx = ""
        slen = len(textx)
        elen = len(textx) + 15
        arrData = {'S':str(slen), 'E':str(elen - 4), 'M':mids[0]}
        arr.append(arrData)
        textx += mention + str(text)
    puy.sendMessage(to, textx, {'MENTION': str('{"MENTIONEES":' + json.dumps(arr) + '}')}, 0)

def command(text):
    pesan = text.lower()
    if settings["prefix"] == True:
        if pesan.startswith(settings["keyCommand"]):
            cmd = pesan.replace(settings["keyCommand"],"")
        else:
            cmd = "Undefined command"
    else:
        cmd = text.lower()
    return cmd
    
def helpmessage():
    if settings['prefix'] == True:
        key = settings['keyCommand']
    else:
        key = ''
    helpMessage =   "\n  「 PUY  」     " + "\n" + \
                    " " + key + "1) Token/Tokengen" + "\n" + \
                    " " + key + "2) Keluar" + "\n\n" + \
                    " " + key + " 「 CEKSIDER  」" + "\n" + \
                    " " + key + "3) Cekpembaca On/Off - [For SetRead]" + "\n" + \
                    " " + key + "4) Cekpembaca reset - [For Reset reader point]" + "\n" + \
                    " " + key + "5) Cekpembaca - [For CheckRead]" + "\n" + \
                    " " + key + "6) SetPrefix:" + "\n" + \
                    " " + key + "7) Logout" + "\n" + \
                    " " + key + "8) Perbarui" + "\n" + \
                    "  「Use " + key + " For the Prefix」" + "\n" + \
                    " 「 From Helloworld / Edited by Puy 」"
    return helpMessage
                    
def puyBot(op):
    try:
        if op.type == 0:
            print ("[ 0 ] END OF OPERATION")
            return

        if op.type == 5:
            print ("[ 5 ] NOTIFIED ADD CONTACT")
            if settings["autoAdd"] == True:
                puy.findAndAddContactsByMid(op.param2)
                sendMessageWithFooter(op.param1, "Thx for add")

        if op.type == 13:
            print ("[ 13 ] Invite Into Group")
            if cvMid in op.param3:
                if settings["autoJoin"] == True:
                    puy.acceptGroupInvitation(op.param1)
                dan = puy.getContact(op.param2)
                tgb = puy.getGroup(op.param1)
                sendMention(op.param1, "[ INVITE MEMBER NOTIFY ]".format(str(tgb.name)),[op.param2])
                puy.sendImageWithURL(op.param1, "http://dl.profile.line-cdn.net{}".format(dan.picturePath))
                puy.sendContact(op.param1, op.param2)

        if op.type == 19:
            print ("[ 19 ] NOTIFIED KICKOUT FROM GROUP")
            group = puy.getGroup(op.param1)
            contact = puy.getContact(op.param2)
            victim = puy.getContact(op.param3)
            dap = "   Group Name : {}".format(str(group.name))
            dapp = "\n   Executor : {}".format(str(contact.displayName))
            dappp = "\n   Victim : {}".format(str(victim.displayName))
            puy.sendMessage(op.param1, "「 Notify Kickout From Group 」\n\nPelaku Kick : {}\nK{}".format(str(contact.displayName),"orban Kick : {}".format(str(victim.displayName))))
            puy.sendContact(op.param1, op.param2)
            puy.sendContact(op.param1, op.param3)
            print (dap)                
                
        if op.type in [22, 24]:
            print ("[ 22 And 24 ] NOTIFIED INVITE INTO ROOM & NOTIFIED LEAVE ROOM")
            if settings["autoLeave"] == True:
                sendMention(op.param2, "@! hmm?")
                puy.leaveRoom(op.param1)
                                
        if op.type == 26:
            try:
                print ("[ 26 ] PUBLIC")
                msg = op.message
                text = msg.text
                msg_id = msg.id
                receiver = msg.to
                sender = msg._from
                prefix = settings["keyCommand"].title()
                if settings["prefix"] == False:
                    prefix = ''
                if msg.toType == 0 or msg.toType == 1 or msg.toType == 2:
                    if msg.toType == 0:
                        if sender != puy.profile.mid:
                            to = sender
                        else:
                            to = receiver
                    elif msg.toType == 1:
                        to = receiver
                    elif msg.toType == 2:
                        to = receiver
                    if msg.contentType == 0:
                        if text is None:
                            return
                        else:
                            cmd = command(text)
                            if cmd == "help":
                                helpMessage = helpmessage()
                                puy.sendMessage(to, str(helpMessage),{'AGENT_ICON':'http://dl.profile.line-cdn.net/0hkY3juiptNHYOExk5wsdLITJWOht5PTI-diUpGX8RPhZ0IydzMSV_FC0VaxV0I3JyMCZ4Ei8VOEQh','AGENT_LINK':'https://line.me/ti/p/~yapuy','AGENT_NAME':'Help Message'})
                            
                            if cmd == "#help":
                                helpMessage = helpmessage()
                                puy.sendMessage(to, str(helpMessage),{'AGENT_ICON':'http://dl.profile.line-cdn.net/0hkY3juiptNHYOExk5wsdLITJWOht5PTI-diUpGX8RPhZ0IydzMSV_FC0VaxV0I3JyMCZ4Ei8VOEQh','AGENT_LINK':'https://line.me/ti/p/~yapuy','AGENT_NAME':'Help Message'})
                            
                            elif cmd == "tokengen":
                                sendMentionFooter(to, "「 TOKEN TIPE  」\n1* DESKTOPWIN\n2* WIN10\n3* DESKTOPMAC\n4* IOSPAD\n5* CHROME\n\n*Usage : Type #login with Token Type\n\n*Example : #login chrome\n\n[ From BotEater / Edited by Puy ]\n@! - Selamat Mencoba.", [sender])
                            elif cmd == "token":
                                sendMentionFooter(to, "「 TOKEN TIPE  」\n1* DESKTOPWIN\n2* WIN10\n3* DESKTOPMAC\n4* IOSPAD\n5* CHROME\n\n*Usage : Type #login with Token Type\n\n*Example : #login chrome\n\n[ From BotEater / Edited by Puy ]\n@! - Selamat Mencoba.", [sender])
                                
                            elif cmd == "sp":
                                start = time.time()
                                puy.sendMessage(to, "Counting...")
                                speed = time.time() - start
                                ping = speed * 1000
                                puy.sendMessage(to, "The result is {} ms".format(str(speedtest(ping))))                                
                                
                            elif cmd == "speed":
                              if msg._from in Owner:
                                start = time.time()
                                puy.sendMessage(to, "...")
                                elapsed_time = time.time() - start
                                puy.sendMessage(to, "{}".format(str(elapsed_time)))
                                
                            elif cmd.startswith(".speed"):
                                get_profile_time_start = time.time()
                                get_profile = puy.getProfile()
                                get_profile_time = time.time() - get_profile_time_start
                                get_group_time_start = time.time()
                                get_group = puy.getGroupIdsJoined()
                                get_group_time = time.time() - get_group_time_start
                                get_contact_time_start = time.time()
                                #get_contact = puy.getContact(clientMid)
                                get_contact_time = time.time() - get_contact_time_start
                                #puy.sendMessage("u3b07c57b6239e5216aa4c7a02687c86d", '.')
                                puy.sendMessage(to, "Time :\n%.6f" % (get_group_time/3))                                
                                
                            elif cmd == "perbarui":
                              if sender in Owner:
                                tz = pytz.timezone("Asia/Jakarta")
                                timeNow = datetime.now(tz=tz)
                                day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
                                hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
                                bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
                                hr = timeNow.strftime("%A")
                                bln = timeNow.strftime("%m")
                                for i in range(len(day)):
                                    if hr == day[i]: hasil = hari[i]
                                for k in range(0, len(bulan)):
                                    if bln == str(k): bln = bulan[k-1]
                                Timed = hasil + ", " + timeNow.strftime('%d') + " - " + bln + " - " + timeNow.strftime('%Y') + "\nJam : [ " + timeNow.strftime('%H:%M:%S') + " ]"
                                #if msg.to not in read['readPoint']:
                                    #dap.sendMessage(msg.to, "「 NOTIFIED BOT SPEED 」\n\n" + Timed)
                                #sendMention(to, "@! \nPUY berhasil diperbarui.\n\nPada :\n" + Timed, [sender])
                                puy.sendMessage(to, "PUY berhasil diperbarui.\n\nPada :\n" + Timed)
                                restartBot()
                              else:
                                  puy.sendMessage("Permission Denied")

                            elif cmd.startswith("about puy"):
                                try:
                                    arr = []
                                    Ownerz = "uac8e3eaf1eb2a55770bf10c3b2357c33"
                                    creator = puy.getContact(Ownerz)
                                    contact = puy.getContact(puyMid)
                                    grouplist = puy.getGroupIdsJoined()
                                    contactlist = puy.getAllContactIds()
                                    blockedlist = puy.getBlockedContactIds()
                                    #ret_ = "「 HELPER  」"
                                    #ret_ += "\n  Name : {}".format(contact.displayName)
                                    #ret_ += "\n  Group : {}".format(str(len(grouplist)))
                                    #ret_ += "\n  Friend : {}".format(str(len(contactlist)))
                                    #ret_ += "\n  Blocked : {}".format(str(len(blockedlist)))
                                    #ret_ += "\n  [ About Selfbot ]"
                                    #ret_ += "\n  Version : Premium"
                                    #ret_ += "\n  Creator : {}".format(creator.displayName)
                                    #ret_ += "\n  Creator : @!".format(Owner)
                                    #puy.sendMessage(to, str(ret_))
                                    sendMention(to, "「 About Puy 」\n\nThe Beginning of this Bot Comes from Helloworld, I'm just Reworked This!\n\nOf Course Special Thanks To HelloWorld, And the Friends Around Me!", [Ownerz])
                                except Exception as e:
                                    puy.sendMessage(msg.to, str(e))                                 
                                  
                            elif cmd == "me":
                                contact = puy.getContact(sender)
                                sendMentionFooter(to, "At here @!", [sender])
                                puy.sendContact(to, sender)                                
                                puy.sendImageWithURL(to,"http://dl.profile.line-cdn.net/{}".format(contact.pictureStatus))                                                        
                                
                            elif cmd == "autojoin on":
                              if msg._from in Owner:
                                settings["autoJoin"] = True
                                sendMention(to, "[ Notified Auto Join ]\nBerhasil mengaktifkan Auto Join @!", [sender])
                            elif cmd == "autojoin off":
                              if msg._from in Owner:
                                settings["autoJoin"] = False
                                sendMention(to, "[ Notified Auto Join ]\nBerhasil menonaktifkan Auto Join @!", [sender])   
                            elif cmd == "autoleave on":
                                settings["autoLeave"] = True
                                sendMention(to, "[ Notified Auto Leave ]\nBerhasil mengaktifkan Auto leave @!", [sender])
                            elif cmd == "autoleave off":
                              if msg._from in Owner:
                                settings["autoLeave"] = False
                                sendMention(to, "[ Notified Auto Leave ]\nBerhasil menonaktifkan Auto leave @!", [sender])
                            elif cmd == "status":
                                try:
                                    ret_ = "\n   [ BOT STATUS ]\n"
                                    if settings["autoJoin"] == True: ret_ += "\n   [ ON ] Auto Join"
                                    else: ret_ += "\n   [ OFF ] Auto Join"
                                    if settings["autoLeave"] == True: ret_ += "\n   [ ON ] Auto Leave Room"
                                    else: ret_ += "\n   [ OFF ] Auto Leave Room"
                                    ret_ += ""
                                    sendMessageWithFooter(to, str(ret_))
                                except Exception as e:
                                    sendMessageWithFooter(to, str(e))
              ## LURKING ##                      
                            elif text.lower() == 'cekpembaca on':
                                tz = pytz.timezone("Asia/Jakarta")
                                timeNow = datetime.now(tz=tz)
                                day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
                                hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
                                bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
                                hr = timeNow.strftime("%A")
                                bln = timeNow.strftime("%m")
                                for i in range(len(day)):
                                    if hr == day[i]: hasil = hari[i]
                                for k in range(0, len(bulan)):
                                    if bln == str(k): bln = bulan[k-1]
                                readTime = hasil + ", " + timeNow.strftime('%d') + " - " + bln + " - " + timeNow.strftime('%Y') + "\nJam : [ " + timeNow.strftime('%H:%M:%S') + " ]"
                                if msg.to in read['readPoint']:
                                        try:
                                            del read['readPoint'][msg.to]
                                            del read['readMember'][msg.to]
                                            del read['readTime'][msg.to]
                                        except:
                                            pass
                                        read['readPoint'][msg.to] = msg.id
                                        read['readMember'][msg.to] = ""
                                        read['readTime'][msg.to] = datetime.now().strftime('%H:%M:%S')
                                        read['ROM'][msg.to] = {}
                                        with open('read.json', 'w') as fp:
                                            json.dump(read, fp, sort_keys=True, indent=4)                                                                                                                                                                                                                                                                                                                                                           
                                            #sendMention(to, "@!\n「 Ceksider Diaktifkan 」\nWaktu :\n" + readTime, [sender])
                                            puy.sendMessage(to, "「 Ceksider Diaktifkan 」\n\nWaktu :\n" + readTime)
                                else:
                                    try:
                                        del read['readPoint'][msg.to]
                                        del read['readMember'][msg.to]
                                        del read['readTime'][msg.to]
                                    except:
                                        pass
                                    read['readPoint'][msg.to] = msg.id
                                    read['readMember'][msg.to] = ""
                                    read['readTime'][msg.to] = datetime.now().strftime('%H:%M:%S')
                                    read['ROM'][msg.to] = {}
                                    with open('read.json', 'w') as fp:
                                        json.dump(read, fp, sort_keys=True, indent=4)
                                        #sendMention(to, "@!\n「 Ceksider Diaktifkan 」\n" + readTime, [sender])
                                        puy.sendMessage(to, "「 Ceksider Diaktifkan 」\n\n" + readTime)
                            
                            elif text.lower() == 'cekpembaca off':
                                tz = pytz.timezone("Asia/Jakarta")
                                timeNow = datetime.now(tz=tz)
                                day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
                                hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
                                bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
                                hr = timeNow.strftime("%A")
                                bln = timeNow.strftime("%m")
                                for i in range(len(day)):
                                    if hr == day[i]: hasil = hari[i]
                                for k in range(0, len(bulan)):
                                    if bln == str(k): bln = bulan[k-1]
                                readTime = hasil + ", " + timeNow.strftime('%d') + " - " + bln + " - " + timeNow.strftime('%Y') + "\nJam : [ " + timeNow.strftime('%H:%M:%S') + " ]"
                                if msg.to not in read['readPoint']:
                                    #sendMention(to, "「 Ceksider telah dimatikan  」\n@!\nWaktu :\n" + readTime, [sender])
                                    puy.sendMessage(to, "「 Ceksider telah dimatikan  」\n\nWaktu :\n" + readTime)
                                else:
                                    try:
                                        del read['readPoint'][msg.to]
                                        del read['readMember'][msg.to]
                                        del read['readTime'][msg.to]
                                    except:
                                          pass
                                    #sendMention(to, "「 Ceksider telah dimatikan  」\n@!\n" + readTime, [sender])
                                    puy.sendMessage(to, "「 Ceksider telah dimatikan  」\n\n" + readTime)
        
                            elif text.lower() == 'cekpembaca reset':
                                tz = pytz.timezone("Asia/Jakarta")
                                timeNow = datetime.now(tz=tz)
                                day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
                                hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
                                bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
                                hr = timeNow.strftime("%A")
                                bln = timeNow.strftime("%m")
                                for i in range(len(day)):
                                    if hr == day[i]: hasil = hari[i]
                                for k in range(0, len(bulan)):
                                    if bln == str(k): bln = bulan[k-1]
                                readTime = hasil + ", " + timeNow.strftime('%d') + " - " + bln + " - " + timeNow.strftime('%Y') + "\nJam : [ " + timeNow.strftime('%H:%M:%S') + " ]"
                                if msg.to in read["readPoint"]:
                                    try:
                                        del read["readPoint"][msg.to]
                                        del read["readMember"][msg.to]
                                        del read["readTime"][msg.to]
                                    except:
                                        pass
                                    #sendMention(to, "「 Mengulangi riwayat pembaca 」 :\n@!\n" + readTime, [sender])
                                    puy.sendMessage(to, "「 Ceksider telah direset 」\n\n" + readTime)
                                else:
                                    #sendMention(to, "「 Ceksider belum diaktifkan 」\n@!", [sender])
                                    puy.sendMessage(to, "「 Ceksider telah direset 」\n\n" + readTime)

                            elif text.lower() == 'cekpembaca':
                                tz = pytz.timezone("Asia/Jakarta")
                                timeNow = datetime.now(tz=tz)
                                day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
                                hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
                                bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
                                hr = timeNow.strftime("%A")
                                bln = timeNow.strftime("%m")
                                for i in range(len(day)):
                                    if hr == day[i]: hasil = hari[i]
                                for k in range(0, len(bulan)):
                                    if bln == str(k): bln = bulan[k-1]
                                readTime = hasil + ", " + timeNow.strftime('%d') + " - " + bln + " - " + timeNow.strftime('%Y') + "\nJam : [ " + timeNow.strftime('%H:%M:%S') + " ]"
                                if receiver in read['readPoint']:
                                    if read["ROM"][receiver].items() == []:
                                        puy.sendMessage(receiver,"   「 Daftar Pembaca 」\nNone")
                                    else:
                                        chiya = []
                                        for rom in read["ROM"][receiver].items():
                                            chiya.append(rom[1])
                                        cmem = puy.getContacts(chiya) 
                                        zx = ""
                                        zxc = ""
                                        zx2 = []
                                        xpesan = '「 Daftar Pembaca 」\n\n'
                                    for x in range(len(cmem)):
                                        xname = str(cmem[x].displayName)
                                        pesan = ''
                                        pesan2 = pesan+"@c\n"
                                        xlen = str(len(zxc)+len(xpesan))
                                        xlen2 = str(len(zxc)+len(pesan2)+len(xpesan)-1)
                                        zx = {'S':xlen, 'E':xlen2, 'M':cmem[x].mid}
                                        zx2.append(zx)
                                        zxc += pesan2
                                    text = xpesan+ zxc + "\n\n" + readTime
                                    try:
                                        puy.sendMessage(receiver, text, contentMetadata={'MENTION':str('{"MENTIONEES":'+json.dumps(zx2).replace(' ','')+'}')}, contentType=0)
                                    except Exception as error:
                                        print (error)
                                    pass
                                else:
                                    puy.sendMessage(receiver,"*Cekpembaca belum diaktifkan\nKetik 「 cekpembaca on 」 untuk mengaktifkan.")

                            elif cmd.startswith("keluar"):
                                puy.sendMessage(to, "Gbye")
                                puy.getGroupIdsJoined()
                                puy.leaveGroup(to)

                            elif cmd.startswith("getnumb "):
                                query = cmd.replace("getnumb ","")
                                puy1 = requests.get("https://www.calcatraz.com/calculator/api?c={}".format(urllib.parse.quote(query)))
                                data=puy1.text
                                data=json.loads(data)
                                puy.sendMessage(msg.to, query + " = " + str(data))                                
                                
                            elif cmd.startswith("motivate"):
                                puy1 = requests.get("https://talaikis.com/api/quotes/random")
                                data=puy1.text
                                data=json.loads(data)                                                                   
                                puy.sendMessage(to,str(data["quote"]))                                
                                
                            elif cmd.startswith("bitcoin"):
                                puy1 = requests.get("https://xeonwz.herokuapp.com/bitcoin.api")
                                data=puy1.text
                                data=json.loads(data)
                                hasilnya = "[ Bitcoin ]\n" 
                                hasilnya += "\n~Price : " +str(data["btc"])
                                hasilnya += "\n~Expensive : " +str(data["high"])
                                hasilnya += "\n~Cheap : " +str(data["low"])
                                puy.sendMessage(msg.to, str(hasilnya))
                                
                            elif cmd.startswith("urban "):
                                sep = cmd.split(" ")
                                judul = cmd.replace(sep[0] + " ","")
                                url = "http://api.urbandictionary.com/v0/define?term="+str(judul)
                                with requests.session() as s:
                                    s.headers["User-Agent"] = random.choice(settings["userAgent"])
                                    puy1 = s.get(url)
                                    data = puy1.text
                                    data = json.loads(data)
                                    y = "Result Urban :"
                                    y += "\nTags: "+ data["tags"][0]
                                    y += ","+ data["tags"][1]
                                    y += ","+ data["tags"][2]
                                    y += ","+ data["tags"][3]
                                    y += ","+ data["tags"][4]
                                    y += ","+ data["tags"][5]
                                    y += ","+ data["tags"][6]
                                    y += ","+ data["tags"][7]
                                    y += "\n\n~Author : "+str(data["list"][0]["author"])
                                    y += "\n~Word : "+str(data["list"][0]["word"])
                                    y += "\n~Link : "+str(data["list"][0]["permalink"])
                                    y += "\n~Definition : "+str(data["list"][0]["definition"])
                                    y += "\n~Example : "+str(data["list"][0]["example"])
                                    puy.sendMessage(to, str(y))                                
                                
                            elif cmd.startswith("suggestion "):
                                query = cmd.replace("suggestion ","")
                                puy1 = requests.get("http://api.ntcorp.us/se/v1/?q={}".format(urllib.parse.quote(query)))
                                data=puy1.text
                                data=json.loads(data)
                                no = 0
                                ret_ = "[ Suggestion ]\n"                                                                                                                       
                                anu = data["result"]["suggestions"]
                                for s in anu:
                                    hmm = s
                                    no += 1
                                    ret_ += "\n" + str(no) + ". " + "{}".format(str(hmm))
                                puy.sendMessage(msg.to, str(ret_))                              
                                
                            elif cmd.startswith("bcroadcast: "):
                              if msg._from in Owner:
                                sep = text.split(" ")
                                pesan = text.replace(sep[0] + " ","")
                                saya = puy.getGroupIdsJoined()
                                for group in saya:
                                   sendMessageWithFooter(group,"" + str(pesan))
                                         
                        if text.lower() == 'login win10':
                            req = requests.get('https://api.eaterbots.com/WIN10')
                            a = req.text
                            b = json.loads(a)
                            tknop= codecs.open("tkn.json","r","utf-8")
                            tkn = json.load(tknop)
                            tkn['{}'.format(msg._from)] = []
                            tkn['{}'.format(msg._from)].append({
                                'qr': b['result'][0]['linkqr'],
                                'tkn': b['result'][0]['linktkn']
                                })
                            qrz = b['result'][0]['linkqr']
                            puy.sendMessage(to, 'Buka Link dibawah dan Tekan Login\n\n{}\n\nKetik win10 done jika sudah'.format(qrz))                            
                            with open('tkn.json', 'w') as outfile:
                                json.dump(tkn, outfile)
                        if text.lower() == 'win10 done':
                            tknop= codecs.open("tkn.json","r","utf-8")
                            tkn = json.load(tknop)
                            a = tkn['{}'.format(msg._from)][0]['tkn']
                            req = requests.get(url = '{}'.format(a))
                            b = req.text
                            puy1 = dap.getContact(sender).displayName
                            puy2 = dap.getGroup(msg.to).name
                            puy3 = dap.getContact(sender).mid
                            sendMention(to,'「 TOKEN RESULT 」\nUntuk : @!\nDari Grup : '+puy2+'\nMid Kamu : '+puy3+'\n\n-「 TOKEN 」  : \n{}\n\n- UA : Line/8.3.2\n- LA : WIN10 8.8.3 NADYA-TJ x64\n\n*「 From BotEater / Edited By PUY 」'.format(b), [sender])
                            
                        if text.lower() == 'login chrome':
                            req = requests.get('https://api.eaterbots.com/CHROMEOS')
                            a = req.text
                            b = json.loads(a)
                            tknop= codecs.open("tkn.json","r","utf-8")
                            tkn = json.load(tknop)
                            tkn['{}'.format(msg._from)] = []
                            tkn['{}'.format(msg._from)].append({
                                'qr': b['result'][0]['linkqr'],
                                'tkn': b['result'][0]['linktkn']
                                })
                            qrz = b['result'][0]['linkqr']
                            dap.sendMessage(to, 'Buka Link dibawah dan Tekan Login\n\n{}\n\nKetik chrome done jika sudah'.format(qrz))                            
                            with open('tkn.json', 'w') as outfile:
                                json.dump(tkn, outfile)
                        if text.lower() == 'chrome done':
                            tknop= codecs.open("tkn.json","r","utf-8")
                            tkn = json.load(tknop)
                            a = tkn['{}'.format(msg._from)][0]['tkn']
                            req = requests.get(url = '{}'.format(a))
                            b = req.text
                            puy1 = dap.getContact(sender).displayName
                            puy2 = dap.getGroup(msg.to).name
                            puy3 = dap.getContact(sender).mid
                            sendMention(to,'「 CHROME 」\nUntuk : @!\nDari Grup : '+puy2+'\nMid Kamu : '+puy3+'\n\n-「 TOKEN 」  : \n{}\n\n- UA : Line/8.3.2\n- LA : CHROMEOS 8.8.3 PUY x64\n\n*「 From NadyaTJ & BotEater / Edited By PUY 」'.format(b), [sender])
                                
                        if text.lower() == 'login iospad':
                            req = requests.get('https://api.eaterbots.com/IOSIPAD')
                            a = req.text
                            b = json.loads(a)
                            tknop= codecs.open("tkn.json","r","utf-8")
                            tkn = json.load(tknop)
                            tkn['{}'.format(msg._from)] = []
                            tkn['{}'.format(msg._from)].append({
                                'qr': b['result'][0]['linkqr'],
                                'tkn': b['result'][0]['linktkn']
                                })
                            qrz = b['result'][0]['linkqr']
                            dap.sendMessage(to, 'Buka Link dibawah dan Tekan Login\n\n{}\n\nKetik iospad done jika sudah'.format(qrz))                            
                            with open('tkn.json', 'w') as outfile:
                                json.dump(tkn, outfile)
                        if text.lower() == 'iospad done':
                            tknop= codecs.open("tkn.json","r","utf-8")
                            tkn = json.load(tknop)
                            a = tkn['{}'.format(msg._from)][0]['tkn']
                            req = requests.get(url = '{}'.format(a))
                            b = req.text
                            puy1 = dap.getContact(sender).displayName
                            puy2 = dap.getGroup(msg.to).name
                            puy3 = dap.getContact(sender).mid
                            sendMention(to,'「 IOSPAD 」\nUntuk : @!\nDari Grup : '+ab+'\nMid Kamu : '+ac+'\n\n-「 TOKEN 」  : \n{}\n\n- UA : Line/8.3.2\n- LA : IOSPAD 8.8.3 PUY x64\n\n*「 From BotEater / Edited By PUY 」'.format(b), [sender])
                                
                        if text.lower() == 'login desktopwin':
                            req = requests.get('https://api.eaterbots.com/DESKTOPWIN')
                            a = req.text
                            b = json.loads(a)
                            tknop= codecs.open("tkn.json","r","utf-8")
                            tkn = json.load(tknop)
                            tkn['{}'.format(msg._from)] = []
                            tkn['{}'.format(msg._from)].append({
                                'qr': b['result'][0]['linkqr'],
                                'tkn': b['result'][0]['linktkn']
                                })
                            qrz = b['result'][0]['linkqr']
                            dap.sendMessage(to, 'Buka Link dibawah dan Tekan Login\n\n{}\n\nKetik desktopwin done jika sudah'.format(qrz))                            
                            with open('tkn.json', 'w') as outfile:
                                json.dump(tkn, outfile)
                        if text.lower() == 'desktopwin done':
                            tknop= codecs.open("tkn.json","r","utf-8")
                            tkn = json.load(tknop)
                            a = tkn['{}'.format(msg._from)][0]['tkn']
                            req = requests.get(url = '{}'.format(a))
                            b = req.text
                            puy1 = dap.getContact(sender).displayName
                            puy2 = dap.getGroup(msg.to).name
                            puy3 = dap.getContact(sender).mid
                            sendMention(to,'「 DESKTOPWIN 」\nUntuk : @!\nDari Grup : '+puy2+'\nMid Kamu : '+puy3+'\n\n-「 TOKEN 」  : \n{}\n\n- UA : DESKTOPWIN 8.8.3 PUY x64\n\n*「 From BotEater / Edited By PUY 」'.format(b), [sender])
                            
                        if text.lower() == 'login desktopmac':
                            req = requests.get('https://api.eaterbots.com/DESKTOPMAC')
                            a = req.text
                            b = json.loads(a)
                            tknop= codecs.open("tkn.json","r","utf-8")
                            tkn = json.load(tknop)
                            tkn['{}'.format(msg._from)] = []
                            tkn['{}'.format(msg._from)].append({
                                'qr': b['result'][0]['linkqr'],
                                'tkn': b['result'][0]['linktkn']
                                })
                            qrz = b['result'][0]['linkqr']
                            dap.sendMessage(to, 'Buka Link dibawah dan Tekan Login\n\n{}\n\nKetik desktopmac done jika sudah'.format(qrz))
                            with open('tkn.json', 'w') as outfile:
                                json.dump(tkn, outfile)
                        if text.lower() == 'desktopmac done':
                            tknop= codecs.open("tkn.json","r","utf-8")
                            tkn = json.load(tknop)
                            a = tkn['{}'.format(msg._from)][0]['tkn']
                            req = requests.get(url = '{}'.format(a))
                            b = req.text
                            puy1 = dap.getContact(sender).displayName
                            puy2 = dap.getGroup(msg.to).name
                            puy3 = dap.getContact(sender).mid
                            sendMention(to,'「 DESKTOPMAC 」\nUntuk : @!\nDari Grup : '+puy2+'\nMid Kamu : '+puy3+'\n\n-「 TOKEN 」  : \n{}\n\n- UA : Line/8.3.2\n- LA : DESKTOPMAC 8.8.3 PUY x64\n\n*「 From BotEater / Edited By PUY 」'.format(b), [sender])
                                
        ## PREFIX ##          
                        elif cmd.startswith("setprefix:"):
                          if msg._from in Owner:
                            sep = text.split(" ")
                            key = text.replace(sep[0] + " ","")
                            if " " in key:
                                puy.sendMessage(to, "\nTanpa spasi.\n")
                            else:
                                settings["keyCommand"] = str(key).lower()
                                sendMessageWithFooter(to, "text [ {} ]".format(str(key).lower()))        
                        if text.lower() == "myprefix":
                            puy.sendMessage(to, "Prefix diterapkan menjadi [ {} ]\n".format(str(settings["keyCommand"])))
                        elif text.lower() == "prefix":
                            puy.sendMessage(to, "Prefix saat ini [ {} ]".format(str(settings["keyCommand"])))
                        elif text.lower() == "prefix on":
                            settings["prefix"] = True
                            puy.sendMessage(to, "[ Notified Prefix Key ]\nBerhasil mengaktifkan Prefix")
                        elif text.lower() == "prefix off":
                            settings["prefix"] = False
                            puy.sendMessage(to, "[ Notified Prefix Key ]\nBerhasil menonaktifkan Prefix")
                            
                        elif cmd.startswith("imageart "):
                            try:                                   
                                search = cmd.replace("imageart ","")
                                puy1 = requests.get("https://xeonwz.herokuapp.com/images/deviantart.api?q={}".format(search))
                                data = puy1.text
                                data = json.loads(data)
                                if data["content"] != []:
                                    items = data["content"]
                                    path = random.choice(items)
                                    a = items.index(path)
                                    b = len(items)
                                    puy.sendImageWithURL(to, str(path))
                                    puy.sendMessage(to,"Art #%s from #%s." %(str(a),str(b)))
                                    log.info("Art #%s from #%s." %(str(a),str(b)))
                            except Exception as error:
                                logError(error)
                                traceback.print_tb(error.__traceback__)
                    if msg.contentType == 0:
                        if text is None:
                            return
                        if "/ti/g/" in msg.text.lower():
                            if settings["autoJoinTicket"] == True:
                                link_re = re.compile('(?:line\:\/|line\.me\/R)\/ti\/g\/([a-zA-Z0-9_-]+)?')
                                links = link_re.findall(text)
                                n_links = []
                                for l in links:
                                    if l not in n_links:
                                        n_links.append(l)
                                for ticket_id in n_links:
                                    group = puy.findGroupByTicket(ticket_id)
                                    puy.acceptGroupInvitationByTicket(group.id,ticket_id)
                                    puy.sendMessage(to, "Berhasil masuk ke group %s" % str(group.name))                                             
                        if 'MENTION' in msg.contentMetadata.keys()!= None:
                            names = re.findall(r'@(\w+)', text)
                            mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                            mentionees = mention['MENTIONEES']
                            lists = []
                            for mention in mentionees:
                                if puyMid in mention["M"]:
                                    if settings["autoRespon"] == True:
                                        sendMention(sender, " @!, don't tag", [sender])
                                    break
            except Exception as error:
                logError(error)
                traceback.print_tb(error.__traceback__)                            
                            
        if op.type == 26:
            try:
                print ("[ 26 ] RECIEVE MESSAGE")
                msg = op.message
                text = msg.text
                msg_id = msg.id
                receiver = msg.to
                sender = msg._from
                if msg.toType == 0 or msg.toType == 1 or msg.toType == 2:
                    if msg.toType == 0:
                    #if text =='mute':
                        if sender != puy.profile.mid:
                            to = sender
                        else:
                            to = receiver
                    elif msg.toType == 1:
                        to = receiver
                    elif msg.toType == 2:
                        to = receiver
                    #if settings["autoRead"] == True:
                        #puy.sendChatChecked(to, msg_id)
                    if to in read["readPoint"]:
                        if sender not in read["ROM"][to]:
                            read["ROM"][to][sender] = True
                    
## INI KALAU MAU DI HAPUS SILAHKAN ## 
                    elif msg.contentType == 16:
                        if settings["checkPost"] == True:
                            try:
                                ret_ = "\n  [ Details Post ]  "
                                if msg.contentMetadata["serviceType"] == "GB":
                                    contact = puy.getContact(sender)
                                    auth = "\n  Author : {}".format(str(contact.displayName))
                                else:
                                    auth = "\n  Author : {}".format(str(msg.contentMetadata["serviceName"]))
                                purl = "\n  URL : {}".format(str(msg.contentMetadata["postEndUrl"]).replace("line://","https://line.me/R/"))
                                ret_ += auth
                                ret_ += purl
                                if "mediaOid" in msg.contentMetadata:
                                    object_ = msg.contentMetadata["mediaOid"].replace("svc=myhome|sid=h|","")
                                    if msg.contentMetadata["mediaType"] == "V":
                                        if msg.contentMetadata["serviceType"] == "GB":
                                            ourl = "\n  Object URL : https://obs-us.line-apps.com/myhome/h/download.nhn?tid=612w&{}".format(str(msg.contentMetadata["mediaOid"]))
                                            murl = "\n  Media URL : https://obs-us.line-apps.com/myhome/h/download.nhn?{}".format(str(msg.contentMetadata["mediaOid"]))
                                        else:
                                            ourl = "\n  Object URL : https://obs-us.line-apps.com/myhome/h/download.nhn?tid=612w&{}".format(str(object_))
                                            murl = "\n  Media URL : https://obs-us.line-apps.com/myhome/h/download.nhn?{}".format(str(object_))
                                        ret_ += murl
                                    else:
                                        if msg.contentMetadata["serviceType"] == "GB":
                                            ourl = "\n  Object URL : https://obs-us.line-apps.com/myhome/h/download.nhn?tid=612w&{}".format(str(msg.contentMetadata["mediaOid"]))
                                        else:
                                            ourl = "\n  Object URL : https://obs-us.line-apps.com/myhome/h/download.nhn?tid=612w&{}".format(str(object_))
                                    ret_ += ourl
                                if "text" in msg.contentMetadata:
                                    text = "\n  the contents of writing : {}".format(str(msg.contentMetadata["text"]))
                                    ret_ += text
                                ret_ += "\n"
                                puy.sendMessage(to, str(ret_))
                            except:
                                puy.sendMessage(to, "\nInvalid post\n")
            except Exception as error:
                logError(error)
                traceback.print_tb(error.__traceback__)
                            
        if op.type == 55:
            print ("[ 55 ] NOTIFIED READ MESSAGE")
            try:
                if op.param1 in read['readPoint']:
                    if op.param2 in read['readMember'][op.param1]:
                        pass
                    else:
                        read['readMember'][op.param1] += op.param2
                    read['ROM'][op.param1][op.param2] = op.param2
                else:
                   pass
            except Exception as error:
                logError(error)
                traceback.print_tb(error.__traceback__)
    except Exception as error:
        logError(error)
        traceback.print_tb(error.__traceback__)

while True:
    try:
        delete_log()
        ops = puyPoll.singleTrace(count=50)
        if ops is not None:
            for op in ops:
                puyBot(op)
                puyPoll.setRevision(op.revision)
    except Exception as error:
        logError(error)
        
def atend():
    print("Saving")
    with open("Log_data.json","w",encoding='utf8') as f:
        json.dump(msg_dict, f, ensure_ascii=False, indent=4,separators=(',', ': '))
    print("BYE")
atexit.register(atend)
