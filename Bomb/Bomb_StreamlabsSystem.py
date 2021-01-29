#!/usr/bin/python
# -*- coding: utf-8 -*-
# pylint: disable=invalid-name
"""Bomb command"""
#---------------------------------------
# Libraries and references
#---------------------------------------
import codecs
import json
import os
import winsound
import ctypes
import time
from array import *
#---------------------------------------
# [Required] Script information
#---------------------------------------
ScriptName = "Bomb"
Website = "https://github.com/marianwulf"
Creator = "Marox"
Version = "1.0.1"
Description = "Bomb command"
#---------------------------------------
# Versions
#---------------------------------------
""" Releases (open README.md for full release notes)
1.0.0 - Initial Release
1.0.1 - fixed empty targetnames in active users viewerlist
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
            self.Command = "!bomb"
            self.Permission = "Everyone"
            self.PermissionInfo = ""
            self.Usage = "Stream Chat"
            self.RandomPassCommands = False
            self.EnableWrongCommandResponse = False
            self.PassCommandsList = "!gift,!donotcopypasteme,!bomb123"
            self.UseCD = True
            self.Cooldown = 30
            self.OnCooldown = "$username the command is still on cooldown for $cooldown seconds!"
            self.CasterIgnoreCD = False
            self.ActiveGameTime = 120
            self.Max = 20
            self.Min = 10
            self.WinPointsPercentage = 100
            self.Timeout = False
            self.TL = 60
            self.Blacklist = "Streamlabs,Nightbot,Anotherttvviewer,Soundalerts,Bebiyoda,Commanderroot"
            self.NoTargetFoundResponse = "$username unfortunately there is no valid target in the viewerlist :("
            self.StartResponse = "$username you started the bomb game and gave it to $targetname. Use $command to pass it to the next person!"
            self.PassResponse = "$username you gave the bomb to $targetname. Use $command to pass it to the next person!"
            self.TargetLostNotEnough = "The bomb exploded and $loser had only $pointslost $currency, so he lost everything. $winner was the last person to pass the bomb and won $pointswon $currency"
            self.TargetLost = "The bomb exploded and $loser lost $pointslost $currency. $winner was the last person to pass the bomb and won $pointswon $currency"
            self.ActiveGameButNotBombHolderResponse = "$username the game is currently active but you are not the bomb owner"
            self.NotEnoughResponse = "$username you don´t have enough $currency to attempt this! You will need atleast $points $currency."
            self.PermissionResponse = "$username -> only $permission ($permissioninfo) and higher can use this command"
            
        # load variables that do not need to be customisable from the ui
        self.ActiveGame = False
        self.ActiveGameEnd = None
        self.BombHolder = ""
        self.LastBombHolder = ""
        self.Viewerlist = []
        # replace spaces from blacklist and put it into a list
        self.UserBlacklist = self.Blacklist.lower().replace(" ","").split(',')
        # if RandomPassCommands is enabled put commands into a list
        if self.RandomPassCommands == True:
            self.ActiveCommandList = self.PassCommandsList.lower().replace(" ","").split(',')
        self.ActiveCommand = self.Command

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
    if data.IsChatMessage() and data.GetParam(0).lower() == MySet.ActiveCommand.lower():

        # if command is not from valid source -> quit
        if not IsFromValidSource(data, MySet.Usage):
            return

        # check on onlylive setting or if user is live
        if not MySet.OnlyLive or Parent.IsLive():

            # if command is on cooldown -> quit
            if IsOnCooldown(data):
                return
                    
            # check if a game is active
            if MySet.ActiveGame:
                
                # if user is not the bomb holder send message
                if data.UserName != MySet.BombHolder:
                    message = MySet.ActiveGameButNotBombHolderResponse.replace("$username", data.UserName)
                    SendResp(data, message)
                    return

                # get random target from viewerlist
                targetname = MySet.Viewerlist[Parent.GetRandom(0,len(MySet.Viewerlist))]
                
                # if target is the same person as the bomb holder or blacklisted try again. if no other target is found send message
                tries = 0
                while targetname.lower() == MySet.BombHolder.lower() or targetname.lower() in MySet.UserBlacklist:
                    if tries >= 25:
                        message = MySet.NoTargetFoundResponse.replace("$username", data.UserName)
                        SendResp(data, message)
                        #reset game and add cooldown
                        MySet.ActiveGame = False
                        MySet.ActiveGameEnd = None
                        Parent.AddCooldown(ScriptName, MySet.Command, MySet.Cooldown)
                        return
                    targetname = MySet.Viewerlist[Parent.GetRandom(0,len(MySet.Viewerlist))]
                    tries += 1

                # set new bomb holder
                MySet.LastBombHolder = MySet.BombHolder
                MySet.BombHolder = Parent.GetDisplayName(targetname)

                # if RandomPassCommands is enabled get new random command
                if MySet.RandomPassCommands == True:
                    LastActiveCommand = MySet.ActiveCommand
                    while LastActiveCommand == MySet.ActiveCommand:
                        MySet.ActiveCommand = MySet.ActiveCommandList[Parent.GetRandom(0,len(MySet.ActiveCommandList))]

                # send pass response
                message = MySet.PassResponse.replace("$username", data.UserName).replace("$targetname", MySet.BombHolder).replace("$command", MySet.ActiveCommand)
                SendResp(data, message)

                
            else:
                
                # if user has no permission -> quit
                if not HasPermission(data):
                    return
                
                # check if user has more points than highest possible lost
                if not HasEnoughPoints(data, MySet.Max):
                    return
            
                # enable bomb
                MySet.ActiveGame = True
                MySet.ActiveGameEnd = time.time() + Parent.GetRandom((MySet.ActiveGameTime*0.8), (MySet.ActiveGameTime*1.2))
                MySet.LastBombHolder = data.UserName
                
                # get active users from viewerlist and delete empty strings returned from chatbot
                MySet.Viewerlist = Parent.GetActiveUsers()
                MySet.Viewerlist = filter(None, MySet.Viewerlist)

                # if there are less than 2 viewers reset game, add cooldown and send message
                if len(MySet.Viewerlist) < 2:
                    message = MySet.NoTargetFoundResponse.replace("$username", data.UserName)
                    SendResp(data, message)
                    MySet.ActiveGame = False
                    MySet.ActiveGameEnd = None
                    Parent.AddCooldown(ScriptName, MySet.Command, MySet.Cooldown)
                    return
                # get random viewer from viewerlist
                targetname = MySet.Viewerlist[Parent.GetRandom(0,len(MySet.Viewerlist))]
                
                # if target is the same person as the starting user or blacklisted try again. if no other target is found send message
                tries = 0
                while targetname.lower() == data.User or targetname.lower() in MySet.UserBlacklist:
                    if tries >= 25:
                        message = MySet.NoTargetFoundResponse.replace("$username", data.UserName)
                        SendResp(data, message)
                        MySet.ActiveGame = False
                        MySet.ActiveGameEnd = None
                        Parent.AddCooldown(ScriptName, MySet.Command, MySet.Cooldown)
                        return
                    targetname = MySet.Viewerlist[Parent.GetRandom(0,len(MySet.Viewerlist))]
                    tries += 1

                MySet.BombHolder = Parent.GetDisplayName(targetname)
            
                # if RandomPassCommands is enabled get new random command
                if MySet.RandomPassCommands == True:
                    LastActiveCommand = MySet.ActiveCommand
                    while LastActiveCommand == MySet.ActiveCommand:
                        MySet.ActiveCommand = MySet.ActiveCommandList[Parent.GetRandom(0,len(MySet.ActiveCommandList))]
                
                # send start message
                message = MySet.StartResponse.replace("$username", data.UserName).replace("$targetname", MySet.BombHolder).replace("$command", MySet.ActiveCommand)
                SendResp(data, message)


def Tick():
    """Required tick function"""

    # check if game time if over
    if MySet.ActiveGame and time.time() >= MySet.ActiveGameEnd:

        #reset game times
        MySet.ActiveGame = False
        MySet.ActiveGameEnd = None
        MySet.ActiveCommand = MySet.Command

        # get current points from the bomb holder and set the amount that will be lost
        targetcurrentpoints = int(Parent.GetPoints(MySet.BombHolder.lower()))
        randompoints = Parent.GetRandom(MySet.Min, MySet.Max + 1)

        # if current points are lower than the points that will be lost trigger another response
        if targetcurrentpoints < randompoints:
            Parent.RemovePoints(MySet.BombHolder.lower(), MySet.BombHolder, targetcurrentpoints)
            Parent.AddPoints(MySet.LastBombHolder.lower(), MySet.LastBombHolder, int((randompoints*MySet.WinPointsPercentage)/100))
            message = MySet.TargetLostNotEnough.replace("$winner", MySet.LastBombHolder).replace("$loser", MySet.BombHolder).replace("$pointswon", str(int((randompoints*MySet.WinPointsPercentage)/100))).replace("$pointslost", str(targetcurrentpoints)).replace("$currency", Parent.GetCurrencyName())
            Parent.SendStreamMessage(message)
            Parent.AddCooldown(ScriptName, MySet.Command, MySet.Cooldown)
            if MySet.Timeout:
                    Parent.SendStreamMessage("/timeout {0} {1}".format(MySet.BombHolder.lower(), MySet.TL))
            return
        else:
            Parent.RemovePoints(MySet.BombHolder.lower(), MySet.BombHolder, randompoints)
            Parent.AddPoints(MySet.LastBombHolder.lower(), MySet.LastBombHolder, int((randompoints*MySet.WinPointsPercentage)/100))
            message = MySet.TargetLost.replace("$winner", MySet.LastBombHolder).replace("$loser", MySet.BombHolder).replace("$pointswon", str(int((randompoints*MySet.WinPointsPercentage)/100))).replace("$pointslost", str(randompoints)).replace("$currency", Parent.GetCurrencyName())
            Parent.SendStreamMessage(message)
            Parent.AddCooldown(ScriptName, MySet.Command, MySet.Cooldown)
            if MySet.Timeout:
                    Parent.SendStreamMessage("/timeout {0} {1}".format(MySet.BombHolder.lower(), MySet.TL))
            return

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

                #message = MySet.OnUserCooldown.replace("$username", data.UserName).replace("$cooldown", str(m_CooldownRemaining))
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
        #Parent.AddUserCooldown(ScriptName, MySet.Command, data.User, MySet.UserCooldown)
        Parent.AddCooldown(ScriptName, MySet.Command, MySet.Cooldown)

def HasEnoughPoints(data, points):
    """Return true if user has enough points for the command and false if user doesn't"""
    if not Parent.RemovePoints(data.User, data.UserName, points):
        message = MySet.NotEnoughResponse.replace("$username", data.UserName).replace("$currency", Parent.GetCurrencyName()).replace("$points", str(points))
        SendResp(data, message)
        return False
    Parent.AddPoints(data.User, data.UserName, points)
    return True
