#!/usr/bin/python
# -*- coding: utf-8 -*-
# pylint: disable=invalid-name
"""Rob command, replica of the textbased version."""
#---------------------------------------
# Libraries and references
#---------------------------------------
import codecs
import json
import os
import winsound
import ctypes
#---------------------------------------
# [Required] Script information
#---------------------------------------
ScriptName = "Rob"
Website = "https://www.twitch.tv/maroxtv"
Creator = "Marox"
Version = "1.0.1"
Description = "Rob command"
#---------------------------------------
# Versions
#---------------------------------------
""" Releases (open README.txt for full release notes)
1.0.0 - Initial Release
1.0.1 - added User Blacklist, fixed cost
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
            self.Command = "!rob"
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
            self.TargetNotEnoughResponse = "$username the target $targetname has not enough $currency to attempt this!"
            self.WinResponse = "$username managed to rob $points $currency from $targetname"
            self.LoseResponse = "$username tried to rob some $currency from $targetname but $username got rekt and $targetname managed to rob $points $currency from $username instead!"
            self.PermissionResponse = "$username -> only $permission ($permissioninfo) and higher can use this command"
            self.InfoResponse = "$username you have to choose a target to try to rob from"
            self.NotHereResponse = "$username you can only rob from users who are currently in the viewerlist!"
            self.SelfRobResponse = "$username you can not rob yourself!"
            self.Max = 20
            self.Min = 10
            self.Protected = False
            self.Blacklist = ""
            self.BlacklistResponse = "$username you can not rob $targetname. User is blacklisted."
            self.Timeout = False
            self.TL = 60

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
    if data.IsChatMessage() and data.GetParam(0).lower() == MySet.Command.lower():

        if not IsFromValidSource(data, MySet.Usage):
            return

        if not Parent.HasPermission(data.User, MySet.Permission, MySet.PermissionInfo):
            message = MySet.PermissionResponse.format(data.User, MySet.Permission, MySet.PermissionInfo)
            SendResp(data, message)

        if not HasPermission(data):
            return

        if not MySet.OnlyLive or Parent.IsLive():

            if IsOnCooldown(data):
                return
                
            userblacklist = MySet.Blacklist.lower().replace(" ","").split(',')
            targetname = data.GetParam(1).lower().replace('@', '')
            
            if targetname in userblacklist:
                message = MySet.BlacklistResponse.format(data.UserName, data.GetParam(1))
                SendResp(data,message)
                return
            
            if targetname == Parent.GetChannelName().lower and MySet.Protected:
                value = Parent.GetRandom(MySet.Min, MySet.Max)
                Parent.RemovePoints(data.User, data.UserName, value)
                message = MySet.LoseResponse.format(data.UserName, Parent.GetCurrencyName(), value, data.GetParam(1))
                SendResp(data, message)
                AddCooldown(data)
                return

            if data.GetParamCount() < 2:
                message = MySet.InfoResponse.replace("$username", data.UserName)
                SendResp(data, message)
                return
            
            if targetname == data.User:
                message = MySet.SelfRobResponse.replace("$username", data.UserName)
                SendResp(data,message)
                return
            
            viewerlist = Parent.GetViewerList() 
            
            for viewerlistIT in viewerlist:
                viewerlistIT = viewerlistIT.lower()
                    
                    
            if targetname not in viewerlist:
                message = MySet.NotHereResponse.replace("$username", data.UserName)
                SendResp(data,message)
                return
                
            value = Parent.GetRandom(MySet.Min,MySet.Max)
            
            
            if not Parent.RemovePoints(data.User, data.UserName, MySet.Max + MySet.Cost):
                message = MySet.NotEnoughResponse.replace("$username", data.UserName).replace("$currency", Parent.GetCurrencyName()).replace("$points", str(MySet.Max + MySet.Cost))
                SendResp(data, message)
                return
            Parent.AddPoints(data.User, data.UserName, MySet.Max + MySet.Cost)
            
            if not Parent.RemovePoints(targetname, targetname, value):
                message = MySet.TargetNotEnoughResponse.replace("$username", data.UserName).replace("$targetname", data.GetParam(1)).replace("$currency", Parent.GetCurrencyName())
                SendResp(data, message)
                return
            Parent.AddPoints(targetname, targetname, value)
            
            Parent.RemovePoints(data.User, data.UserName, MySet.Cost)
            
            outcome = Parent.GetRandom(1, 3)
            if outcome == 1:
                Parent.RemovePoints(data.User, data.UserName, value)
                Parent.AddPoints(targetname, targetname, value)
                message = MySet.LoseResponse.replace("$username", data.UserName).replace("$currency", Parent.GetCurrencyName()).replace("$points", str(value)).replace("$targetname", data.GetParam(1))
                SendResp(data, message)
                AddCooldown(data)
                if MySet.Timeout:
                    Parent.SendStreamMessage("/timeout {0} {1}".format(data.User, MySet.TL))
                return

            elif outcome == 2:
                Parent.RemovePoints(targetname, targetname, value)
                Parent.AddPoints(data.User, data.UserName, value)
                message = MySet.WinResponse.replace("$username", data.UserName).replace("$currency", Parent.GetCurrencyName()).replace("$points", str(value)).replace("$targetname", data.GetParam(1))
                SendResp(data, message)
                AddCooldown(data)
                return

            else:
                message = "Rob hat nen Bug :("
                SendResp(data, message)

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
