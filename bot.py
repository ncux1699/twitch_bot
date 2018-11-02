# -*- coding: utf-8 -*-
import config
import utils
import socket
import re
import thread
import sqlite3
from time import sleep
from random import randint
"Это мой огородик, в нем уже 44 подсолнуха!"

def main():
    #try:
    s = socket.socket()
    s.connect((config.HOST, config.PORT))
    s.send("PASS {}\r\n".format(config.PASS).encode("utf-8"))
    s.send("NICK {}\r\n".format(config.NICK).encode("utf-8"))
    s.send("JOIN #{}\r\n".format(config.CHAN).encode("utf-8"))
    s.send("CAP REQ :twitch.tv/tags\r\n".encode("utf-8"))

    chat_message = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :0")
    whisper = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv WHISPER #\w+ :0")
    thread.start_new_thread(utils.fillOplist, ())
    thread.start_new_thread(utils.moneyplus, ())
    thread.start_new_thread(utils.cm_list, (s,))
    #thread.start_new_thread(utils.donate, (s,))
    #thread.start_new_thread(utils.roulette_msg, (s,))
    while True:
        response = s.recv(1024).decode("utf-8")

        if response == "PING :tmi.twitch.tv\r\n":
            s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
        else:

            try:
                server_message = chat_message.sub("", response)
            except:
                server_message = whisper.sub("", response)
                print(whisper)
            # print(response)
            try:
                message2 = server_message.split(" :", 1)
                message = message2[1]
            except:
                message = server_message
            print(message)

            username = re.search(r"\w+", message).group(0)
            if message.endswith("PRIVMSG #{} :!time\r\n".format(config.CHAN)) == 1 or message.endswith("PRIVMSG #{} :!время\r\n".decode("utf-8").format(config.CHAN)) == 1 or message.endswith("PRIVMSG #{} :!uptime\r\n".format(config.CHAN)) == 1:
                print(1)
                utils.stime(s)
            if message.endswith("PRIVMSG #{} :!message\r\n".format(config.CHAN)) == 1:
                print(2)
                utils.mess(s, "Если вам понравилось, подписывайтесь на youtube https://www.youtube.com/user/Neffedyourbrain и ВК https://vk.com/sashaneff".format(username))
            if message.startswith("{}!{}@{}.tmi.twitch.tv PRIVMSG #{} :!boxAdd ".format(username, username, username, config.CHAN)) == 1:  # and (message2[0].find("subscriber=1") or utils.isOp(username)):
                print(3)
                box = open("box.txt", "a")
                message = message.replace("{}!{}@{}.tmi.twitch.tv PRIVMSG #{} :!boxAdd ".format(username, username, username, config.CHAN),"")
                write = message.strip()
                box.write("\n" + write.encode("utf-8"))
                box.close()
                utils.mess(s, "Коробка пополнена!")
            if message.endswith("PRIVMSG #{} :!цитата\r\n".decode("utf-8").format(config.CHAN)) == 1:
                print(4)
                with open("box.txt") as box:
                    array = [line.strip() for line in box]
                r = randint(0, len(array) - 1)
                utils.mess(s, array[r])
            if message.endswith("PRIVMSG #{} :!команды\r\n".decode("utf-8").format(config.CHAN)) == 1:
                print(5)
                utils.mess(s, "Список команд: {}".format(utils.commands))
            if message.endswith("PRIVMSG #{} :!шерстинки\r\n".decode("utf-8").format(config.CHAN)) == 1:
                print(6)
                conn = sqlite3.connect("money.sqlite")
                cursor = conn.cursor()
                cursor.execute("select money from money where name='{}'".format(username))
                result = cursor.fetchone()
                try:
                    utils.mess(s, "/w {} У тебя {} {}!".format(username, result[0], utils.end[result[0]%10]))
                except:
                    utils.mess(s, "/w {} Прости, что-то опять сломалось BibleThump".format(username))
                conn.close()
            if message.startswith("ncux1699!ncux1699@ncux1699.tmi.twitch.tv PRIVMSG #{} :!награда ".decode("utf-8").format(config.CHAN)) == 1:
                print(7)
                conn = sqlite3.connect("money.sqlite")
                cursor = conn.cursor()
                winner = message.encode('utf-8').replace("{}!{}@{}.tmi.twitch.tv PRIVMSG #{} :!награда ".format("ncux1699", "ncux1699", "ncux1699",config.CHAN), "")
                cursor.execute("select money from money where name='{}'".format(winner.strip()))
                f = cursor.fetchone()
                print (f[0])
                f1 = f[0] + 100
                cursor.execute("update money set money={} where name='{}'".format(f1, winner.strip()))
                conn.commit()
                cursor.execute("select money from money where name='{}'".format(winner.strip()))
                f = cursor.fetchone()
                print (f[0])
                conn.close()
                utils.mess(s, "@{} выиграл 100 шерстинок!".format(winner))
            if message.endswith("PRIVMSG #{} :!рулетка\r\n".decode("utf-8").format(config.CHAN)) == 1:
                try:
                    print(8)
                    a = randint(1,20)
                    b = randint(1,20)
                    conn = sqlite3.connect("money.sqlite")
                    cursor = conn.cursor()
                    cursor.execute("select timer from money where name='{}'".format(username))
                    f = cursor.fetchone()
                    if f[0]==0:
                        cursor.execute("select money from money where name='{}'".format(username))
                        f = cursor.fetchone()
                        if f[0]>0:
                            cursor.execute("select score from games where game='roulette'")
                            f = cursor.fetchone()
                            if a == b:
                                cursor.execute("update games set score=20 where game='roulette'")
                                cursor.execute("select money from money where name='{}'".format(username))
                                fp = cursor.fetchone()
                                cursor.execute("update money set money={} where name='{}'".format(fp[0]+f[0], username))
                                conn.commit()
                                conn.close()
                                utils.mess(s, "@{}, поздравляю! Ты выиграл {} {}!".format(username, f[0], utils.end[f[0] % 10]))
                                utils.mess(s, "Призовой фонд сброшен до 20!")
                            else:
                                cursor.execute("update games set score={} where game='roulette'".format(f[0]+5))
                                cursor.execute("select money from money where name='{}'".format(username))
                                fp = cursor.fetchone()
                                cursor.execute("update money set money={} where name='{}'".format(fp[0]-5, username))
                                cursor.execute("update money set timer=1 where name='{}'".format(username))
                                conn.commit()
                                conn.close()
                                utils.mess(s, "/w {} не огорчайся, в следующий раз повезет. Призовой фонд увеличился и теперь составляет {} {}!".format(username, f[0]+5, utils.end[(f[0]+5) % 10]))
                                #utils.mess(s, "Призовой фонд увеличился и теперь составляет {} {}!".format(f[0] + 5, utils.end[(f[0] + 5) % 10]))
                        else:
                            utils.mess(s, "/w {} у тебя недостаточно шерстинок, приходи на стримы чаще, не огорчай Джинджер!".format(username))
                            cursor.execute("update money set timer=1 where name='{}'".format(username))
                            conn.close()
                    else:
                        utils.mess(s, "/w @{} не спамь, пробовать свою удачу можно только раз в минуту!".format(username))
                except:
                    utils.mess(s, "/w {} прости, что-то пошло не так, попробуй позже BibleThump".format(username))
            if message.endswith("PRIVMSG #{} :!топ\r\n".decode("utf-8").format(config.CHAN)) == 1:
                print(9)
                conn = sqlite3.connect("money.sqlite")
                cursor = conn.cursor()
                cursor.execute("select money from money order by money desc limit 10 offset 2")
                f = []
                for i in range(10):
                    c = cursor.fetchone()
                    f.append(c[0])
                cursor.execute("select name from money order by money desc limit 10 offset 2")
                name = []
                for i in range(10):
                    c = cursor.fetchone()
                    name.append(c[0])
                utils.mess(s, "Топ 10 хранителей шерстинок: 1 - {} ({}), 2 - {} ({}), 3 - {} ({}), 4 - {} ({}), 5 - {} ({}), 6 - {} ({}), 7 - {} ({}), 8 - {} ({}), 9 - {} ({}), 10 - {} ({}),".format(name[0], f[0], name[1], f[1], name[2], f[2], name[3], f[3], name[4], f[4], name[5], f[5], name[6], f[6], name[7], f[7], name[8], f[8], name[9], f[9]))
                conn.close()
            if message.endswith("ncux1699!ncux1699@ncux1699.tmi.twitch.tv PRIVMSG #{} :!roulette\r\n".format(config.CHAN)) == 1:
                conn = sqlite3.connect("money.sqlite")
                cursor = conn.cursor()
                cursor.execute("select score from games where game='roulette'")
                f = cursor.fetchone()
                utils.mess(s, "Призовой фонд составляет {} {}!".format(f[0], utils.end[f[0] % 10]))
                utils.mess(s, "Чтобы попытать свою удачу в ловле шерстинок напиши !рулетка")
                conn.close()


                    
    #except:
        #print("Fuck")


if __name__ == "__main__":
    main()
