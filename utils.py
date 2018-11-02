# -*- coding: utf-8 -*-
import config
import urllib2
import json
import sqlite3
from time import sleep

commands = "!time, !uptime,  !время, !цитата, !команды, !boxAdd <цитата>, !шерстинки, !рулетка"
end = {
    1: "шерстинка",
    2: "шерстинки",
    3: "шерстинки",
    4: "шерстинки",
    5: "шерстинок",
    6: "шерстинок",
    7: "шерстинок",
    8: "шерстинок",
    9: "шерстинок",
    0: "шерстинок",}

def mess(sock, message):
    sock.send("PRIVMSG #{} :{}\r\n".format(config.CHAN, message))

def ban(sock, user):
    mess(sock, ".ban {}".format(user))


def timeout(sock, user, seconds = 1):
    mess(sock, ".timeout {}".format(user, seconds))


#req = request
#res = response
def fillOplist():
    while True:
        try:
            url = "http://tmi.twitch.tv/group/user/{}/chatters".format(config.CHAN)
            req = urllib2.Request(url, headers={"accept":"*/*"})
            res = urllib2.urlopen(req).read()
            if res.find("502 gateway") == -1:
                config.oplist.clear()
                data = json.loads(res)
                for p in data["chatters"]["moderators"]:
                    config.oplist[p] = "mod"
                for p in data["chatters"]["global_mods"]:
                    config.oplist[p] = "global_mod"
                for p in data["chatters"]["admins"]:
                    config.oplist[p] = "admin"
                for p in data["chatters"]["staff"]:
                    config.oplist[p] = "staff"
        except:
            print("Something went wrong...Wait")
        sleep(5)


def moneyplus():
    while True:
        try:
            url = "http://tmi.twitch.tv/group/user/{}/chatters".format(config.CHAN)
            req = urllib2.Request(url, headers={"accept":"*/*"})
            res = urllib2.urlopen(req).read()
            if res.find("502 gateway") == -1:
                data = json.loads(res)
                conn = sqlite3.connect("money.sqlite")
                cursor = conn.cursor()
                for p in data["chatters"]["moderators"]:
                    try:
                        cursor.execute("select money from money where name='{}'".format(p))
                        f = cursor.fetchone()
                        fp = f[0] + 1
                        cursor.execute("update money set money={} where name='{}'".format(fp, p))
                        cursor.execute("select timer from money where name='{}'".format(p))
                        f = cursor.fetchone()
                        if f[0] != 0:
                            fp = f[0] - 1
                            cursor.execute("update money set timer={} where name='{}'".format(fp, p))
                        cursor.execute("select watch_time from money where name='{}'".format(p))
                        f = cursor.fetchone()
                        fp = f[0] + 1
                        cursor.execute("update money set watch_time={} where name='{}'".format(fp, p))
                        conn.commit()
                    except:
                        cursor.execute("insert into money values ('{}', 0) ".format(p))
                        cursor.execute("insert into money values ('{}', 0, 0, 1) ".format(p))
                        conn.commit()
                for p in data["chatters"]["viewers"]:
                    try:
                        cursor.execute("select money from money where name='{}'".format(p))
                        f = cursor.fetchone()
                        fp = f[0] + 1
                        cursor.execute("update money set money={} where name='{}'".format(fp, p))
                        cursor.execute("select timer from money where name='{}'".format(p))
                        f = cursor.fetchone()
                        if f[0] != 0:
                            fp = f[0] - 1
                            cursor.execute("update money set timer={} where name='{}'".format(fp, p))
                        cursor.execute("select watch_time from money where name='{}'".format(p))
                        f = cursor.fetchone()
                        fp = f[0] + 1
                        cursor.execute("update money set watch_time={} where name='{}'".format(fp, p))
                        conn.commit()
                    except:
                        cursor.execute("insert into money values ('{}', 0, 0, 1) ".format(p))
                        conn.commit()
                conn.close()
            sleep(60)
        except:
            print("Something went wrong in money...Wait")

def isOp(user):
    return user in config.oplist


def stime(s):
    url = "https://decapi.me/twitch/uptime?channel={}".format(config.CHAN)
    req = urllib2.Request(url, headers={"accept": "*/*"})
    res = urllib2.urlopen(req).read()
    if res.endswith(" is offline"):
        mess(s, "В ожидании начала стрима ResidentSleeper")
    else:
        res = res.replace(" hours, ", ":")
        res = res.replace(" hour, ", ":")
        res = res.replace(" minutes, ", ":")
        res = res.replace(" minute, ", ":")
        res = res.replace(" seconds", "")
        res = res.replace(" second", "")
        time = ""
        for i in res.split(":"):
            if len(i) != 2:
                i = "0"+i
            time = time + i + ":"
        mess(s, "Мы наслаждаемся обществом Саши уже {} <3".format(time[:-1]))


def cm_list(s):
    while True:
        mess(s, "Список команд: {}".format(commands))
        sleep(1200)

def donate(s):
    while True:
        sleep(2050)
        mess(s, "Если хотите, чтобы Джинджер была еще краше, пушистее и милее, то можете помочь Саше прокормить её по ссылочке ;) http://www.donationalerts.ru/r/sasha_neff")

def roulette_msg(s):
    while True:
        conn = sqlite3.connect("money.sqlite")
        cursor = conn.cursor()
        cursor.execute("select score from games where game='roulette'")
        f = cursor.fetchone()
        mess(s, "Призовой фонд составляет {} {}!".format(f[0], end[f[0] % 10]))
        sleep(550)
        conn.close()