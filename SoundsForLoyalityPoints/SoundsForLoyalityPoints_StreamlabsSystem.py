#!/usr/bin/python
# -*- coding: utf-8 -*-
# pylint: disable=invalid-name
"""Sounds for Loyality Points"""
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
from collections import deque
#---------------------------------------
# [Required] Script information
#---------------------------------------
ScriptName = "Sounds for Loyality Points"
Website = "https://github.com/marianwulf"
Creator = "Marox"
Version = "1.0.0"
Description = "Trigger Sounds for Streamlabs Loyality Points"
#---------------------------------------
# Versions
#---------------------------------------
""" Releases (open README.md for full release notes)
1.0.0 - Initial Release
"""
#---------------------------------------
# Variables
#---------------------------------------
settingsFile = os.path.join(os.path.dirname(__file__), "settings.json")
soundsPath = os.path.dirname(__file__) + "\\sounds"
AudioQueue = deque()

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
            self.Command = "!sound"
            self.Cost = 50
            self.Permission = "Everyone"
            self.PermissionInfo = ""
            self.Usage = "Stream Both"
            self.Volume = 25
            self.MessageDelayOnWhisper = 5
            self.UseCD = True
            self.Cooldown = 30
            self.OnCooldown = "$username the command is still on cooldown for $cooldown seconds!"
            self.UserCooldown = 180
            self.OnUserCooldown = "$username the command is still on user cooldown for $cooldown seconds!"
            self.CasterIgnoreCD = False
            self.NotEnoughResponse = "$username you don't have enough $currency to attempt this! You will need atleast $points $currency."
            self.PermissionResponse = "$username -> only $permission ($permissioninfo) and higher can use this command"
            self.AvailibleSoundsResponse = "Availible sounds: $sounds"
            self.PlayedSoundResponse = "$username played Sound: $sound"
            self.PlayedSoundviaWhisperResponse = "$username played Sound: $sound via whisper"
            self.SoundNotFoundResponse = "$username the sound you requested to play does not exist."
            
        self.ActiveDelay = False
        self.ActiveDelayTime = None
        self.ActiveDelayVars = []
        
        self.soundsList = []
        self.soundsListString = ""
        
        for sound in os.listdir(soundsPath):
            soundFile = sound.rsplit(".")
            if soundFile[1] == "mp3":
                costsFile = os.path.join(soundsPath, soundFile[0] + ".txt")
                if costsFile and os.path.isfile(costsFile):
                    with codecs.open(costsFile, encoding='utf-8-sig', mode='r') as f:
                        soundCost = int(f.readline())
                else:
                    soundCost = self.Cost
                
                self.soundsList.append([soundFile[0],soundCost])
                self.soundsListString += soundFile[0] + "("+ str(soundCost) + "), "
        
        self.soundsListString = self.soundsListString[:-2]
        Parent.Log(ScriptName, "Init Sounds: " + str(self.soundsListString))

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