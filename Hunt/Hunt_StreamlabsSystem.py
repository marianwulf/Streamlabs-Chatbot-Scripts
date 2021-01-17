#!/usr/bin/python
# -*- coding: utf-8 -*-
# pylint: disable=invalid-name
"""Hunt command"""
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
ScriptName = "Hunt"
Website = "https://github.com/marianwulf"
Creator = "Marox"
Version = "1.2.1"
Description = "Hunt command"
#---------------------------------------
# Versions
#---------------------------------------
""" Releases (open README.txt for full release notes)
1.0.0 - Initial Release
1.1.0 - other users can join the hunt
1.2.0 - add winchance & winpoints per attendee
1.2.1 - minimum attendees to succeed
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
                # load variables that do not need to be customisable from the ui
                self.ActiveGame = False
                self.ActiveGameAttendees = []
                self.ActiveGameEnd = None
                self.BossStarterUserName = ""
                self.Boss = []
                self.selectedboss = 0

        else: #set variables if no custom settings file is found
            self.OnlyLive = False
            self.Command = "!hunt"
            self.JoinCommand = "!joinhunt"
            self.Cost = 0
            self.MinAttendees = 0
            self.Permission = "Everyone"
            self.PermissionInfo = ""
            self.Usage = "Stream Chat"
            self.UseCD = True
            self.Cooldown = 5
            self.OnCooldown = "{0} the command is still on cooldown for {1} seconds!"
            self.UserCooldown = 10
            self.OnUserCooldown = "{0} the command is still on user cooldown for {1} seconds!"
            self.CasterCD = True
            self.ActiveGame = False
            self.ActiveGameAttendees = []
            self.ActiveGameEnd = None
            self.ActiveGameTime = 60
            self.BossStarterUserName = ""
            self.ActiveGameResponse = "{0} the hunt against {1} is currently active. Type {2} in the next {3} seconds to join the fight."
            self.NoActiveGameResponse = "{0} there is no hunt currently active. Type {1} to begin hunting."
            self.MinAttendeesResponse = "{0} not enough people joined the hunt, so it was aborted."
            self.JoinedFightResponse = "{0} you joined the hunt against {1}! Attendees: {2} - Win Chance {3} - Total Win Points {4} - Win Points per User {5}"
            self.AlreadyJoinedFight = "{0} you already joined the hunt!"
            self.NotEnoughResponse = "{0} you don't have enough {1} to attempt this! You will need atleast {2} {1}."
            self.PermissionResponse = "{0} -> only {1} ({2}) and higher can use this command"
            self.Timeout = False
            self.TL = 60
            self.Boss = []
            self.B1Name = "Feigeratte"
            self.B1WinChance = 80
            self.B1Win = 7
            self.B1Lose = 3
            self.B1StartText = "{0} du trittst gegen [Weiß] Feigeratte an. Win Chance {1} - Total Win Points {2} - Added Win Chance per Attendee {3} - Added Win Points per Attendee {4}! Viel Glück!"
            self.B1WinText = "{0} und seine {1} Crewmitglieder haben insgesamt {2} {3} gewonnen! Somit hat jeder {4} {3} bekommen."
            self.B1LoseText = "{0} du hast {1} {2} verloren!"
            self.B1AddWinChancePerAttendee = 0
            self.B1AddWinPointsPerAttendee = 0
            self.B2Name = "Üblesstinktier"
            self.B2WinChance = 60
            self.B2Win = 15
            self.B2Lose = 15
            self.B2StartText = "{0} du trittst gegen [Grün] Üblesstinktier an. Win Chance {1} - Total Win Points {2} - Added Win Chance per Attendee {3} - Added Win Points per Attendee {4}! Viel Glück!"
            self.B2WinText = "{0} und seine {1} Crewmitglieder haben insgesamt {2} {3} gewonnen! Somit hat jeder {4} {3} bekommen."
            self.B2LoseText = "{0} du hast {1} {2} verloren!"
            self.B2AddWinChancePerAttendee = 0
            self.B2AddWinPointsPerAttendee = 0
            self.B3Name = "Geilesau"
            self.B3WinChance = 40
            self.B3Win = 30
            self.B3Lose = 18
            self.B3StartText = "{0} du trittst gegen [Blau] Geilesau an. Win Chance {1} - Total Win Points {2} - Added Win Chance per Attendee {3} - Added Win Points per Attendee {4}! Viel Glück!"
            self.B3WinText = "{0} und seine {1} Crewmitglieder haben insgesamt {2} {3} gewonnen! Somit hat jeder {4} {3} bekommen."
            self.B3LoseText = "{0} du hast {1} {2} verloren!"
            self.B3AddWinChancePerAttendee = 0
            self.B3AddWinPointsPerAttendee = 0
            self.B4Name = "Jauerbär"
            self.B4WinChance = 20
            self.B4Win = 40
            self.B4Lose = 13
            self.B4StartText = "{0} du trittst gegen [Lila] Jauerbär an. Win Chance {1} - Total Win Points {2} - Added Win Chance per Attendee {3} - Added Win Points per Attendee {4}! Viel Glück!"
            self.B4WinText = "{0} und seine {1} Crewmitglieder haben insgesamt {2} {3} gewonnen! Somit hat jeder {4} {3} bekommen."
            self.B4LoseText = "{0} du hast {1} {2} verloren!"
            self.B4AddWinChancePerAttendee = 0
            self.B4AddWinPointsPerAttendee = 0
            self.B5Name = "Maroxotant"
            self.B5WinChance = 10
            self.B5Win = 80
            self.B5Lose = 15
            self.B5StartText = "{0} du trittst gegen [Gold] Maroxotant an. Win Chance {1} - Total Win Points {2} - Added Win Chance per Attendee {3} - Added Win Points per Attendee {4}! Viel Glück!"
            self.B5WinText = "{0} und seine {1} Crewmitglieder haben insgesamt {2} {3} gewonnen! Somit hat jeder {4} {3} bekommen."
            self.B5LoseText = "{0} du hast {1} {2} verloren!"
            self.B5AddWinChancePerAttendee = 0
            self.B5AddWinPointsPerAttendee = 0
            self.highestlose = 0

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

        # If command is not from valid source -> quit
        if not IsFromValidSource(data, MySet.Usage):
            return

        # if client has no permission -> quit
        if not Parent.HasPermission(data.User, MySet.Permission, MySet.PermissionInfo):
            message = MySet.PermissionResponse.format(data.User, MySet.Permission, MySet.PermissionInfo)
            SendResp(data, message)

        if not HasPermission(data):
            return

        # check on onlylive setting or if user is live
        if not MySet.OnlyLive or Parent.IsLive():

            # quit on cooldown
            if IsOnCooldown(data):
                return
                    
            # send message about active hunt if one is active
            if MySet.ActiveGame:
                message = MySet.ActiveGameResponse.format(data.UserName, MySet.Boss[0], MySet.JoinCommand, str(round(MySet.ActiveGameEnd - time.time())))
                SendResp(data, message)
                return
                
            else:
                
                # define bosses
                MySet.Boss = [[MySet.B1Name, MySet.B1WinChance, MySet.B1Win, MySet.B1Lose, MySet.B1StartText.format(data.UserName, MySet.B1WinChance, MySet.B1Win, MySet.B1AddWinChancePerAttendee, MySet.B1AddWinPointsPerAttendee), MySet.B1WinText.format(data.UserName, 0, MySet.B1Win, Parent.GetCurrencyName(), 0), MySet.B1LoseText.format(data.UserName, MySet.B1Lose, Parent.GetCurrencyName()), MySet.B1AddWinChancePerAttendee, MySet.B1AddWinPointsPerAttendee], \
                            [MySet.B2Name, MySet.B2WinChance, MySet.B2Win, MySet.B2Lose, MySet.B2StartText.format(data.UserName, MySet.B2WinChance, MySet.B2Win, MySet.B2AddWinChancePerAttendee, MySet.B2AddWinPointsPerAttendee), MySet.B2WinText.format(data.UserName, 0, MySet.B2Win, Parent.GetCurrencyName(), 0), MySet.B2LoseText.format(data.UserName, MySet.B2Lose, Parent.GetCurrencyName()), MySet.B2AddWinChancePerAttendee, MySet.B2AddWinPointsPerAttendee], \
                            [MySet.B3Name, MySet.B3WinChance, MySet.B3Win, MySet.B3Lose, MySet.B3StartText.format(data.UserName, MySet.B3WinChance, MySet.B3Win, MySet.B3AddWinChancePerAttendee, MySet.B3AddWinPointsPerAttendee), MySet.B3WinText.format(data.UserName, 0, MySet.B3Win, Parent.GetCurrencyName(), 0), MySet.B3LoseText.format(data.UserName, MySet.B3Lose, Parent.GetCurrencyName()), MySet.B3AddWinChancePerAttendee, MySet.B3AddWinPointsPerAttendee], \
                            [MySet.B4Name, MySet.B4WinChance, MySet.B4Win, MySet.B4Lose, MySet.B4StartText.format(data.UserName, MySet.B4WinChance, MySet.B4Win, MySet.B4AddWinChancePerAttendee, MySet.B4AddWinPointsPerAttendee), MySet.B4WinText.format(data.UserName, 0, MySet.B4Win, Parent.GetCurrencyName(), 0), MySet.B4LoseText.format(data.UserName, MySet.B4Lose, Parent.GetCurrencyName()), MySet.B4AddWinChancePerAttendee, MySet.B4AddWinPointsPerAttendee], \
                            [MySet.B5Name, MySet.B5WinChance, MySet.B5Win, MySet.B5Lose, MySet.B5StartText.format(data.UserName, MySet.B5WinChance, MySet.B5Win, MySet.B5AddWinChancePerAttendee, MySet.B5AddWinPointsPerAttendee), MySet.B5WinText.format(data.UserName, 0, MySet.B5Win, Parent.GetCurrencyName(), 0), MySet.B5LoseText.format(data.UserName, MySet.B5Lose, Parent.GetCurrencyName()), MySet.B5AddWinChancePerAttendee, MySet.B5AddWinPointsPerAttendee]]            
            
                MySet.highestlose = MySet.B1Lose
            
                for BossIT in MySet.Boss:
                    if BossIT[3] > MySet.highestlose:
                        MySet.highestlose = BossIT[3]
            
                # check if user has more points than highest possible lost
                if not Parent.RemovePoints(data.User, data.UserName, MySet.highestlose + MySet.Cost):
                    message = MySet.NotEnoughResponse.format(data.UserName, Parent.GetCurrencyName(), MySet.highestlose + MySet.Cost)
                    SendResp(data, message)
                    return
                Parent.AddPoints(data.User, data.UserName, MySet.highestlose + MySet.Cost)
            
                Parent.RemovePoints(data.User, data.UserName, MySet.Cost)
            
                # enable hunt
                MySet.ActiveGame = True
                MySet.ActiveGameEnd = time.time() + MySet.ActiveGameTime
                MySet.ActiveGameAttendees.append(data.User)
                MySet.BossStarterUserName = data.User
                
                # choose random boss
                MySet.selectedboss = Parent.GetRandom(0,len(MySet.Boss))
                MySet.Boss = MySet.Boss[MySet.selectedboss]
            
                # send boss start message
                message = MySet.Boss[4]
                SendResp(data, message)

    #check if command is join command      
    elif data.IsChatMessage() and data.GetParam(0).lower() == MySet.JoinCommand.lower():
    
        # If command is not from valid source -> quit
        if not IsFromValidSource(data, MySet.Usage):
            return

        # if client has no permission -> quit
        if not Parent.HasPermission(data.User, MySet.Permission, MySet.PermissionInfo):
            message = MySet.PermissionResponse.format(data.User, MySet.Permission, MySet.PermissionInfo)
            SendResp(data, message)

        if not HasPermission(data):
            return

        # check on onlylive setting or if user is live
        if not MySet.OnlyLive or Parent.IsLive():

             # quit on cooldown
            if IsOnCooldown(data):
                return
            
            # check if hunt is active 
            if MySet.ActiveGame:
            
                # check if user has more points than highest possible lost
                if not Parent.RemovePoints(data.User, data.UserName, MySet.highestlose + MySet.Cost):
                    message = MySet.NotEnoughResponse.format(data.UserName, Parent.GetCurrencyName(), MySet.highestlose + MySet.Cost)
                    SendResp(data, message)
                    return
                Parent.AddPoints(data.User, data.UserName, MySet.highestlose + MySet.Cost)
                
                # check if user already joined and send message if
                if data.User in MySet.ActiveGameAttendees:
                    message = MySet.AlreadyJoinedFight.format(data.UserName, MySet.Boss[0])
                    SendResp(data, message)
                    return
            
                # subtract usage costs
                Parent.RemovePoints(data.User, data.UserName, MySet.Cost)
                
                
                # recalculate win chance after adding new attendee
                MySet.Boss[1] += MySet.Boss[7]
                # recalculate win points after adding new attendee
                MySet.Boss[2] += MySet.Boss[8]
                       
                # add user to game and notify
                MySet.ActiveGameAttendees.append(data.User)
                message = MySet.JoinedFightResponse.format(data.UserName, MySet.Boss[0], len(MySet.ActiveGameAttendees), MySet.Boss[1], MySet.Boss[2], MySet.Boss[2]/len(MySet.ActiveGameAttendees))
                SendResp(data, message)  

                # update WinText message
                if MySet.selectedboss == 0:
                    MySet.Boss[5] = MySet.B1WinText.format(MySet.BossStarterUserName, len(MySet.ActiveGameAttendees)-1, MySet.Boss[2], Parent.GetCurrencyName(), MySet.Boss[2]/len(MySet.ActiveGameAttendees))
                elif MySet.selectedboss == 1:
                    MySet.Boss[5] = MySet.B2WinText.format(MySet.BossStarterUserName, len(MySet.ActiveGameAttendees)-1, MySet.Boss[2], Parent.GetCurrencyName(), MySet.Boss[2]/len(MySet.ActiveGameAttendees))
                elif MySet.selectedboss == 2:
                    MySet.Boss[5] = MySet.B3WinText.format(MySet.BossStarterUserName, len(MySet.ActiveGameAttendees)-1, MySet.Boss[2], Parent.GetCurrencyName(), MySet.Boss[2]/len(MySet.ActiveGameAttendees))
                elif MySet.selectedboss == 3:
                    MySet.Boss[5] = MySet.B4WinText.format(MySet.BossStarterUserName, len(MySet.ActiveGameAttendees)-1, MySet.Boss[2], Parent.GetCurrencyName(), MySet.Boss[2]/len(MySet.ActiveGameAttendees))
                elif MySet.selectedboss == 4:
                    MySet.Boss[5] = MySet.B5WinText.format(MySet.BossStarterUserName, len(MySet.ActiveGameAttendees)-1, MySet.Boss[2], Parent.GetCurrencyName(), MySet.Boss[2]/len(MySet.ActiveGameAttendees))     
            
            else:
                # notify that no game is active 
                message = MySet.NoActiveGameResponse.format(data.UserName, MySet.Command)
                SendResp(data, message)
                return


def Tick():
    """Required tick function"""
    
    # check if game time if over
    if MySet.ActiveGame and time.time() >= MySet.ActiveGameEnd:

        #reset game times
        MySet.ActiveGame = False
        MySet.ActiveGameEnd = None
        
        UserWinValue = Parent.GetRandom(1,101)
        
        # check if ActiveGameAttendees is lower than MinAttendees
        if len(MySet.ActiveGameAttendees) < MySet.MinAttendees:
            del MySet.ActiveGameAttendees[:]
            Parent.AddCooldown(ScriptName, MySet.Command, MySet.Cooldown)
            message = MySet.MinAttendeesResponse.format(data.User)
            SendResp(data, message)
            return

        # check if user wins against boss
        if UserWinValue <= MySet.Boss[1]:
            for ActiveGameAttendeesIT in MySet.ActiveGameAttendees:
                # Add won points (total/amount attendees = share points) to account and add cooldown to users
                Parent.AddPoints(ActiveGameAttendeesIT, ActiveGameAttendeesIT, MySet.Boss[2]/len(MySet.ActiveGameAttendees))
                Parent.AddUserCooldown(ScriptName, MySet.Command, ActiveGameAttendeesIT, MySet.UserCooldown)
                Parent.AddUserCooldown(ScriptName, MySet.JoinCommand, ActiveGameAttendeesIT, MySet.UserCooldown)
            message = MySet.Boss[5]
            Parent.SendStreamMessage(message)
            # clean up attendees array
            del MySet.ActiveGameAttendees[:]
            Parent.AddCooldown(ScriptName, MySet.Command, MySet.Cooldown)
            return
        elif UserWinValue > MySet.Boss[1]:
            # Remove lost points from account and add cooldown to users
            for ActiveGameAttendeesIT in MySet.ActiveGameAttendees:
                Parent.RemovePoints(ActiveGameAttendeesIT, ActiveGameAttendeesIT, MySet.Boss[3])
                Parent.AddUserCooldown(ScriptName, MySet.Command, ActiveGameAttendeesIT, MySet.UserCooldown)
                Parent.AddUserCooldown(ScriptName, MySet.JoinCommand, ActiveGameAttendeesIT, MySet.UserCooldown)
            message = MySet.Boss[6]
            Parent.SendStreamMessage(message)
            # clean up attendees array
            del MySet.ActiveGameAttendees[:]
            Parent.AddCooldown(ScriptName, MySet.Command, MySet.Cooldown)
            if MySet.Timeout:
                Parent.SendStreamMessage("/timeout {0} {1}".format(data.User, MySet.TL))
                return
        else:
            message = "Hunt hat nen Bug :("
            Parent.SendStreamMessage(message)

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
    caster = (Parent.HasPermission(data.User, "Caster", "") and MySet.CasterCD)

    if (cooldown or userCooldown) and caster is False:

        if MySet.UseCD:
            cooldownDuration = Parent.GetCooldownDuration(ScriptName, MySet.Command)
            userCDD = Parent.GetUserCooldownDuration(ScriptName, MySet.Command, data.User)

            if cooldownDuration > userCDD:
                m_CooldownRemaining = cooldownDuration

                message = MySet.OnCooldown.format(data.UserName, m_CooldownRemaining)
                SendResp(data, message)

            else:
                m_CooldownRemaining = userCDD

                message = MySet.OnUserCooldown.format(data.UserName, m_CooldownRemaining)
                SendResp(data, message)
        return True
    return False

def HasPermission(data):
    """Returns true if user has permission and false if user doesn't"""
    if not Parent.HasPermission(data.User, MySet.Permission, MySet.PermissionInfo):
        message = MySet.PermissionResponse.format(data.UserName, MySet.Permission, MySet.PermissionInfo)
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
    if Parent.HasPermission(data.User, "Caster", "") and MySet.CasterCD:
        Parent.AddCooldown(ScriptName, MySet.Command, MySet.Cooldown)
        return

    else:
        Parent.AddUserCooldown(ScriptName, MySet.Command, data.User, MySet.UserCooldown)
        Parent.AddCooldown(ScriptName, MySet.Command, MySet.Cooldown)
