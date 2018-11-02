# -*- coding: utf-8 -*-
import config

username = 'ncux1699'
message = 'ncux1699!ncux1699@ncux1699.tmi.twitch.tv PRIVMSG #sasha_neff :!награда sadandserious'
winner = message.replace("{}!{}@{}.tmi.twitch.tv PRIVMSG #{} :!награда ".format("ncux1699", "ncux1699", "ncux1699",config.CHAN), "")
print(winner)