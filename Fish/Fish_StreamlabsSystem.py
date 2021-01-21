#!/usr/bin/python
# -*- coding: utf-8 -*-
# pylint: disable=invalid-name
"""Fish command"""
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
ScriptName = "Fish"
Website = "https://github.com/marianwulf"
Creator = "Marox"
Version = "1.1.0"
Description = "Fish command"
#---------------------------------------
# Versions
#---------------------------------------
""" Releases (open README.md for full release notes)
1.0.0 - Initial Release
1.0.1 - fixed cost
1.1.0 - changed code for better usability in ui
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
            self.Command = "!fish"
            self.Cost = 0
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
            self.B1Name = "Carp"
            self.B1WinChance = 80
            self.B1Win = 7
            self.B1Lose = 3
            self.B1StartText = "$username you try to fish $targetname. Good luck!"
            self.B1WinText = "$username you won $points $currency!"
            self.B1LoseText = "$username you failed and lost $points $currency!"
            self.B2Name = "Herring"
            self.B2WinChance = 60
            self.B2Win = 15
            self.B2Lose = 15
            self.B2StartText = "$username you try to fish $targetname. Good luck!"
            self.B2WinText = "$username you won $points $currency!"
            self.B2LoseText = "$username you failed and lost $points $currency!"
            self.B3Name = "Sardine"
            self.B3WinChance = 40
            self.B3Win = 30
            self.B3Lose = 18
            self.B3StartText = "$username you try to fish $targetname. Good luck!"
            self.B3WinText = "$username you won $points $currency!"
            self.B3LoseText = "$username you failed and lost $points $currency!"
            self.B4Name = "Tuna"
            self.B4WinChance = 20
            self.B4Win = 40
            self.B4Lose = 13
            self.B4StartText = "$username you try to fish $targetname. Good luck!"
            self.B4WinText = "$username you won $points $currency!"
            self.B4LoseText = "$username you failed and lost $points $currency!"
            self.B5Name = "Pufferfish"
            self.B5WinChance = 10
            self.B5Win = 80
            self.B5Lose = 15
            self.B5StartText = "$username you try to fish $targetname. Good luck!"
            self.B5WinText = "$username you won $points $currency!"
            self.B5LoseText = "$username you failed and lost $points $currency!"

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
            
            # define Boss Array
            Boss = [[MySet.B1Name, MySet.B1WinChance, MySet.B1Win, MySet.B1Lose, MySet.B1StartText.replace("$username", data.UserName).replace("$targetname", MySet.B1Name), MySet.B1WinText.replace("$username", data.UserName).replace("$points", str(MySet.B1Win)).replace("$currency", Parent.GetCurrencyName()), MySet.B1LoseText.replace("$username", data.UserName).replace("$points", str(MySet.B1Lose)).replace("$currency", Parent.GetCurrencyName())], \
                    [MySet.B2Name, MySet.B2WinChance, MySet.B2Win, MySet.B2Lose, MySet.B2StartText.replace("$username", data.UserName).replace("$targetname", MySet.B2Name), MySet.B2WinText.replace("$username", data.UserName).replace("$points", str(MySet.B2Win)).replace("$currency", Parent.GetCurrencyName()), MySet.B2LoseText.replace("$username", data.UserName).replace("$points", str(MySet.B2Lose)).replace("$currency", Parent.GetCurrencyName())], \
                    [MySet.B3Name, MySet.B3WinChance, MySet.B3Win, MySet.B3Lose, MySet.B3StartText.replace("$username", data.UserName).replace("$targetname", MySet.B3Name), MySet.B3WinText.replace("$username", data.UserName).replace("$points", str(MySet.B3Win)).replace("$currency", Parent.GetCurrencyName()), MySet.B3LoseText.replace("$username", data.UserName).replace("$points", str(MySet.B3Lose)).replace("$currency", Parent.GetCurrencyName())], \
                    [MySet.B4Name, MySet.B4WinChance, MySet.B4Win, MySet.B4Lose, MySet.B4StartText.replace("$username", data.UserName).replace("$targetname", MySet.B4Name), MySet.B4WinText.replace("$username", data.UserName).replace("$points", str(MySet.B4Win)).replace("$currency", Parent.GetCurrencyName()), MySet.B4LoseText.replace("$username", data.UserName).replace("$points", str(MySet.B4Lose)).replace("$currency", Parent.GetCurrencyName())], \
                    [MySet.B5Name, MySet.B5WinChance, MySet.B5Win, MySet.B5Lose, MySet.B5StartText.replace("$username", data.UserName).replace("$targetname", MySet.B5Name), MySet.B5WinText.replace("$username", data.UserName).replace("$points", str(MySet.B5Win)).replace("$currency", Parent.GetCurrencyName()), MySet.B5LoseText.replace("$username", data.UserName).replace("$points", str(MySet.B5Lose)).replace("$currency", Parent.GetCurrencyName())]]            
            
            # set highest lose to the first boss and then check if the others are higher
            highestlose = MySet.B1Lose
            
            for BossIT in Boss:
                if BossIT[3] > highestlose:
                    highestlose = BossIT[3]
            
            # check if user has more points than highest possible lost
            if not HasEnoughPoints(data, highestlose + MySet.Cost):
                return
            
            # subtract usage costs
            Parent.RemovePoints(data.User, data.UserName, MySet.Cost)
            
            # select random boss and determine winchance
            selectedboss = Parent.GetRandom(0,len(Boss))
            selectedwin = Parent.GetRandom(1,101)
            
            # switch into selected boss
            Boss = Boss[selectedboss]
            
            # send start message
            message = Boss[4]
            SendResp(data, message)
            
            # check if you won or lost, add/remove points and send response
            if selectedwin <= Boss[1]:
                Parent.AddPoints(data.User, data.UserName, Boss[2])
                message = Boss[5]
                SendResp(data, message)
                AddCooldown(data)
                return
            elif selectedwin > Boss[1]:
                Parent.RemovePoints(data.User, data.UserName, Boss[3])
                message = Boss[6]
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