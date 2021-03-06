#!/usr/bin/python
# -*- coding: utf-8 -*-
# pylint: disable=invalid-name
"""Slots command"""
#---------------------------------------
# Libraries and references
#---------------------------------------
import codecs
import json
import os
import winsound
import ctypes
from array import *
#---------------------------------------
# [Required] Script information
#---------------------------------------
ScriptName = "Slots"
Website = "https://github.com/marianwulf"
Creator = "Marox"
Version = "1.0.1"
Description = "Slots command"
#---------------------------------------
# Versions
#---------------------------------------
""" Releases (open README.md for full release notes)
1.0.0 - Initial Release
1.0.1 - added allin
"""
#---------------------------------------
# Variables
#---------------------------------------
settingsFile = os.path.join(os.path.dirname(__file__), "settings.json")

#---------------------------------------
# Classes
#---------------------------------------
class Settings:
    """" Loads settings from file if file is found if not uses default values"""

    # The 'default' variable names need to match UI_Config
    def __init__(self, settingsFile=None):
        if settingsFile and os.path.isfile(settingsFile):
            with codecs.open(settingsFile, encoding='utf-8-sig', mode='r') as f:
                self.__dict__ = json.load(f, encoding='utf-8-sig')

        else: #set variables if no custom settings file is found
            self.OnlyLive = False
            self.Command = "!slots"
            self.Permission = "Everyone"
            self.PermissionInfo = ""
            self.Usage = "Stream Chat"
            self.UseCD = True
            self.Cooldown = 5
            self.OnCooldown = "$username the command is still on cooldown for $cooldown seconds!"
            self.UserCooldown = 10
            self.OnUserCooldown = "$username the command is still on user cooldown for $cooldown seconds!"
            self.CasterIgnoreCD = False
            self.NotEnoughResponse = "$username you don't have enough $currency to attempt this! You will need atleast $points $currency."
            self.PermissionResponse = "$username -> only $permission ($permissioninfo) and higher can use this command"
            self.Timeout = False
            self.TL = 60
            self.Min = 10
            self.Max = 100
            self.AcceptAllin = True
            self.MultiplierTwoApart = 2
            self.MultiplierTwoSidebySide = 4
            self.MultiplierJackpot = 20
            self.MultiplierEpicWin = 100
            self.Emotes = "Kappa,LUL,SeemsGood,DansGame,SeriousSloth,SMOrc"
            self.PremiumEmote = "GlitchLit"
            self.InfoResponse = "$username you have to set a value between $min and $max $currency that you want to bet. Or you dare to just go all in ;)"
            self.AllinResponse = "$username you went all in with a value of $points $currency. Good Luck!"
            self.LoseResponse = "$username you pulled the lever [ $slots ] and got nothing. You lost $points $currency!"
            self.TwoApartResponse = "$username you pulled the lever [ $slots ] and got 2 same emotes! You won $points $currency!"
            self.TwoSidebySideResponse = "$username you pulled the lever [ $slots ] and got 2 same emotes next to each other! You won $points $currency!"
            self.JackpotResponse = "$username you pulled the lever [ $slots ] and got the Jackpot! You won $points $currency!"
            self.EpicWinResponse = "$username you pulled the lever [ $slots ] and got the Epic Win! You won $points $currency!"

    # Reload settings on save through UI
    def ReloadSettings(self, data):
        """Reload settings on save through UI"""
        self.__dict__ = json.loads(data, encoding='utf-8-sig')
        return

    # Save settings to files (json and js)
    def SaveSettings(self, settingsFile):
        """Save settings to files (json and js)"""
        with codecs.open(settingsFile, encoding='utf-8-sig', mode='w+') as f:
            json.dump(self.__dict__, f, encoding='utf-8-sig')
        with codecs.open(settingsFile.replace("json", "js"), encoding='utf-8-sig', mode='w+') as f:
            f.write("var settings = {0};".format(json.dumps(self.__dict__, encoding='utf-8-sig', ensure_ascii=False)))
        return
#---------------------------------------
# [OPTIONAL] Settings functions
#---------------------------------------
def SetDefaults():
    """Set default settings function"""

    #play windows sound
    winsound.MessageBeep()

    #open messagebox with a security check
    MessageBox = ctypes.windll.user32.MessageBoxW
    returnValue = MessageBox(0, u"You are about to reset the settings, "
                                "are you sure you want to contine?"
                             , u"Reset settings file?", 4)

    #if user press "yes"
    if returnValue == 6:

        # Save defaults back to file
        Settings.SaveSettings(MySet, settingsFile)

        #show messagebox that it was complete
        MessageBox = ctypes.windll.user32.MessageBoxW
        returnValue = MessageBox(0, u"Settings successfully restored to default values"
                                 , u"Reset complete!", 0)

#---------------------------------------
# [Required] functions
#---------------------------------------
def Init():
    """data on Load, required function"""
    global MySet
    MySet = Settings(settingsFile)

def Execute(data):
    """Required Execute data function"""
    
    # check if command is command
    if data.IsChatMessage() and data.GetParam(0).lower() == MySet.Command.lower():

        # if command is not from valid source -> quit
        if not IsFromValidSource(data, MySet.Usage):
            return

        # if user has no permission -> quit
        if not HasPermission(data):
            return

        # check on onlylive setting or if user is live
        if not MySet.OnlyLive or Parent.IsLive():

            # if command is on cooldown -> quit
            if IsOnCooldown(data):
                return

            # if no value was set send info response
            if data.GetParamCount() < 2:
                message = MySet.InfoResponse.replace("$username", data.UserName).replace("$min", str(MySet.Min)).replace("$max", str(MySet.Max)).replace("$currency", Parent.GetCurrencyName())
                SendResp(data, message)
                return
            
            
            # if parameter is 'allin' bet all the points otherwise bet the value
            if data.GetParam(1).lower() == "allin" and MySet.AcceptAllin:
               
                bet = Parent.GetPoints(data.User)
                if bet < 1:
                    message = MySet.NotEnoughResponse.replace("$username", data.UserName).replace("$currency", Parent.GetCurrencyName()).replace("$points", str(1))
                    SendResp(data, message)
                    return
                else:
                    message = MySet.AllinResponse.replace("$username", data.UserName).replace("$points", str(bet)).replace("$currency", Parent.GetCurrencyName())
                    SendResp(data, message)
           
            else:            
                
                # if bet is not int send info response
                try:
                    bet = int(data.GetParam(1))
                except:
                    message = MySet.InfoResponse.replace("$username", data.UserName).replace("$min", str(MySet.Min)).replace("$max", str(MySet.Max)).replace("$currency", Parent.GetCurrencyName())
                    SendResp(data, message)
                    return
            
                # if bet is not between min and max send info response
                if not MySet.Min <= bet <= MySet.Max:
                    message = MySet.InfoResponse.replace("$username", data.UserName).replace("$min", str(MySet.Min)).replace("$max", str(MySet.Max)).replace("$currency", Parent.GetCurrencyName())
                    SendResp(data, message)
                    return

                # check if user has more points than his bet
                if not HasEnoughPoints(data, bet):
                    return

            # replace spaces from emotes and put it into a list, afterwards add the premium emote to it
            emotelist = MySet.Emotes.replace(" ","").split(",")
            emotelist.append(MySet.PremiumEmote.replace(" ",""))

            # subtract usage costs
            Parent.RemovePoints(data.User, data.User, bet)

            # pull the lever
            slot1 = emotelist[Parent.GetRandom(0, len(emotelist))]
            slot2 = emotelist[Parent.GetRandom(0, len(emotelist))]
            slot3 = emotelist[Parent.GetRandom(0, len(emotelist))]
            slots = [slot1, slot2, slot3]

            # define output string for response message
            slotsString = slot1 + " " + slot2 + " " + slot3

            # count the slots, send win or lose responses and add points to player
            if slots.count(slot1) == 3:
                if slot1 == MySet.PremiumEmote:
                    message = MySet.EpicWinResponse.replace("$username", data.UserName).replace("$slots", slotsString).replace("$points", str(bet*MySet.MultiplierEpicWin)).replace("$currency", Parent.GetCurrencyName())
                    SendResp(data, message)
                    Parent.AddPoints(data.User, data.User, bet*MySet.MultiplierEpicWin)
                    AddCooldown(data)
                    return
                else:
                    message = MySet.JackpotResponse.replace("$username", data.UserName).replace("$slots", slotsString).replace("$points", str(bet*MySet.MultiplierJackpot)).replace("$currency", Parent.GetCurrencyName())
                    SendResp(data, message)
                    Parent.AddPoints(data.User, data.User, bet*MySet.MultiplierJackpot)
                    AddCooldown(data)
                    return
            elif (slot1 == slot2 or slot2 == slot3):
                message = MySet.TwoSidebySideResponse.replace("$username", data.UserName).replace("$slots", slotsString).replace("$points", str(bet*MySet.MultiplierTwoSidebySide)).replace("$currency", Parent.GetCurrencyName())
                SendResp(data, message)
                Parent.AddPoints(data.User, data.User, bet*MySet.MultiplierTwoSidebySide)
                AddCooldown(data)
                return
            elif (slot1 == slot3):
                message = MySet.TwoApartResponse.replace("$username", data.UserName).replace("$slots", slotsString).replace("$points", str(bet*MySet.MultiplierTwoApart)).replace("$currency", Parent.GetCurrencyName())
                SendResp(data, message)
                Parent.AddPoints(data.User, data.User, bet*MySet.MultiplierTwoApart)
                AddCooldown(data)
                return
            else:
                message = MySet.LoseResponse.replace("$username", data.UserName).replace("$slots", slotsString).replace("$points", str(bet)).replace("$currency", Parent.GetCurrencyName())
                SendResp(data, message)
                AddCooldown(data)
                if MySet.Timeout:
                    Parent.SendStreamMessage("/timeout {0} {1}".format(data.User, MySet.TL))
                return        

def Tick():
    """Required tick function"""

#---------------------------------------
# [Optional] Functions for usage handling
#---------------------------------------
def SendResp(data, sendMessage):
    """Sends message to Stream or discord chat depending on settings"""

    if not data.IsFromDiscord() and not data.IsWhisper():
        Parent.SendStreamMessage(sendMessage)

    if not data.IsFromDiscord() and data.IsWhisper():
        Parent.SendStreamWhisper(data.User, sendMessage)

    if data.IsFromDiscord() and not data.IsWhisper():
        Parent.SendDiscordMessage(sendMessage)

    if data.IsFromDiscord() and data.IsWhisper():
        Parent.SendDiscordDM(data.User, sendMessage)

def CheckUsage(data, rUsage):
    """Return true or false depending on the message is sent from
    a source that's in the usage setting or not"""

    if not data.IsFromDiscord():
        l = ["Stream Chat", "Chat Both", "All", "Stream Both"]
        if not data.IsWhisper() and (rUsage in l):
            return True

        l = ["Stream Whisper", "Whisper Both", "All", "Stream Both"]
        if data.IsWhisper() and (rUsage in l):
            return True

    if data.IsFromDiscord():
        l = ["Discord Chat", "Chat Both", "All", "Discord Both"]
        if not data.IsWhisper() and (rUsage in l):
            return True

        l = ["Discord Whisper", "Whisper Both", "All", "Discord Both"]
        if data.IsWhisper() and (rUsage in l):
            return True

    return False

def IsOnCooldown(data):
    """Return true if command is on cooldown and send cooldown message if enabled"""
    cooldown = Parent.IsOnCooldown(ScriptName, MySet.Command)
    userCooldown = Parent.IsOnUserCooldown(ScriptName, MySet.Command, data.User)
    caster = (Parent.HasPermission(data.User, "Caster", "") and MySet.CasterIgnoreCD)

    if (cooldown or userCooldown) and caster is False:

        if MySet.UseCD:
            cooldownDuration = Parent.GetCooldownDuration(ScriptName, MySet.Command)
            userCDD = Parent.GetUserCooldownDuration(ScriptName, MySet.Command, data.User)

            if cooldownDuration > userCDD:
                m_CooldownRemaining = cooldownDuration

                message = MySet.OnCooldown.replace("$username", data.UserName).replace("$cooldown", str(m_CooldownRemaining))
                SendResp(data, message)

            else:
                m_CooldownRemaining = userCDD

                message = MySet.OnUserCooldown.replace("$username", data.UserName).replace("$cooldown", str(m_CooldownRemaining))
                SendResp(data, message)
        return True
    return False

def HasPermission(data):
    """Returns true if user has permission and false if user doesn't"""
    if not Parent.HasPermission(data.User, MySet.Permission, MySet.PermissionInfo):
        message = MySet.PermissionResponse.replace("$username", data.UserName).replace("$permission", MySet.Permission).replace("$permissioninfo", MySet.PermissionInfo)
        SendResp(data, message)
        return False
    return True

def IsFromValidSource(data, Usage):
    """Return true or false depending on the message is sent from
    a source that's in the usage setting or not"""
    if not data.IsFromDiscord():
        l = ["Stream Chat", "Chat Both", "All", "Stream Both"]
        if not data.IsWhisper() and (Usage in l):
            return True

        l = ["Stream Whisper", "Whisper Both", "All", "Stream Both"]
        if data.IsWhisper() and (Usage in l):
            return True

    if data.IsFromDiscord():
        l = ["Discord Chat", "Chat Both", "All", "Discord Both"]
        if not data.IsWhisper() and (Usage in l):
            return True

        l = ["Discord Whisper", "Whisper Both", "All", "Discord Both"]
        if data.IsWhisper() and (Usage in l):
            return True
    return False

def AddCooldown(data):
    """add cooldowns"""
    if Parent.HasPermission(data.User, "Caster", "") and MySet.CasterIgnoreCD:
        Parent.AddCooldown(ScriptName, MySet.Command, MySet.Cooldown)
        return

    else:
        Parent.AddUserCooldown(ScriptName, MySet.Command, data.User, MySet.UserCooldown)
        Parent.AddCooldown(ScriptName, MySet.Command, MySet.Cooldown)

def HasEnoughPoints(data, points):
    """Return true if user has enough points for the command and false if user doesn't"""
    if not Parent.RemovePoints(data.User, data.UserName, points):
        message = MySet.NotEnoughResponse.replace("$username", data.UserName).replace("$currency", Parent.GetCurrencyName()).replace("$points", str(points))
        SendResp(data, message)
        return False
    Parent.AddPoints(data.User, data.UserName, points)
    return True