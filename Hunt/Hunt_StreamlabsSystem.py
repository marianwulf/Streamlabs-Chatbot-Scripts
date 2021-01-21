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
Version = "1.3.0"
Description = "Hunt command"
#---------------------------------------
# Versions
#---------------------------------------
""" Releases (open README.md for full release notes)
1.0.0 - Initial Release
1.1.0 - other users can join the hunt
1.2.0 - add winchance & winpoints per attendee
1.2.1 - minimum attendees to succeed
1.2.2 - visual bugfix - max 100% win chance
1.3.0 - changed code for better usability in ui
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
            self.Command = "!hunt"
            self.JoinCommand = "!joinhunt"
            self.Cost = 0
            self.MinAttendees = 0
            self.Permission = "Everyone"
            self.PermissionInfo = ""
            self.Usage = "Stream Chat"
            self.UseCD = True
            self.Cooldown = 5
            self.OnCooldown = "$username the command is still on cooldown for $cooldown seconds!"
            self.UserCooldown = 10
            self.OnUserCooldown = "$username the command is still on user cooldown for $cooldown seconds!"
            self.CasterIgnoreCD = True
            self.ActiveGameTime = 60
            self.ActiveGameResponse = "$username the hunt against $targetname is currently active. Type $joincommand in the next $remainingtime seconds to join the fight."
            self.NoActiveGameResponse = "$username there is no hunt currently active. Type $command to begin hunting."
            self.MinAttendeesResponse = "$username not enough people joined the hunt, so it was aborted."
            self.JoinedFightResponse = "$username you joined the hunt against $targetname! Attendees: $attendees - Win Chance: $winchance% - Total Win Points: $points $currency - Win Points per User: $attendeepoints"
            self.AlreadyJoinedFight = "$username you already joined the hunt!"
            self.NotEnoughResponse = "$username you don't have enough $currency to attempt this! You will need atleast $points $currency."
            self.PermissionResponse = "$username -> only $permission ($permissioninfo) and higher can use this command"
            self.Timeout = False
            self.TL = 60
            self.B1Name = "Rat"
            self.B1WinChance = 80
            self.B1Win = 7
            self.B1Lose = 3
            self.B1StartText = "$username you started a hunt against a $targetname. Win Chance: $winchance% - Total Win Points: $points - Added Win Chance per Attendee: $addedwinchance - Added Win Points per Attendee: $addedwinpoints! Everybody can join the hunt with $joincommand. Good Luck!"
            self.B1WinText = "$username and his/her $attendees crewmates have won $points $currency at the hunt against $targetname! So everybody won $attendeepoints $currency."
            self.B1LoseText = "$username and his/her crewmates lost $points $currency each"
            self.B1AddWinChancePerAttendee = 0
            self.B1AddWinPointsPerAttendee = 0
            self.B2Name = "Skunk"
            self.B2WinChance = 60
            self.B2Win = 15
            self.B2Lose = 15
            self.B2StartText = "$username you started a hunt against a $targetname. Win Chance: $winchance% - Total Win Points: $points - Added Win Chance per Attendee: $addedwinchance - Added Win Points per Attendee: $addedwinpoints! Everybody can join the hunt with $joincommand. Good Luck!"
            self.B2WinText = "$username and his/her $attendees crewmates have won $points $currency at the hunt against $targetname! So everybody won $attendeepoints $currency."
            self.B2LoseText = "$username and his/her crewmates lost $points $currency each"
            self.B2AddWinChancePerAttendee = 0
            self.B2AddWinPointsPerAttendee = 0
            self.B3Name = "Boar"
            self.B3WinChance = 40
            self.B3Win = 30
            self.B3Lose = 18
            self.B3StartText = "$username you started a hunt against a $targetname. Win Chance: $winchance% - Total Win Points: $points - Added Win Chance per Attendee: $addedwinchance - Added Win Points per Attendee: $addedwinpoints! Everybody can join the hunt with $joincommand. Good Luck!"
            self.B3WinText = "$username and his/her $attendees crewmates have won $points $currency at the hunt against $targetname! So everybody won $attendeepoints $currency."
            self.B3LoseText = "$username and his/her crewmates lost $points $currency each"
            self.B3AddWinChancePerAttendee = 0
            self.B3AddWinPointsPerAttendee = 0
            self.B4Name = "Bear"
            self.B4WinChance = 20
            self.B4Win = 40
            self.B4Lose = 13
            self.B4StartText = "$username you started a hunt against a $targetname. Win Chance: $winchance% - Total Win Points: $points - Added Win Chance per Attendee: $addedwinchance - Added Win Points per Attendee: $addedwinpoints! Everybody can join the hunt with $joincommand. Good Luck!"
            self.B4WinText = "$username and his/her $attendees crewmates have won $points $currency at the hunt against $targetname! So everybody won $attendeepoints $currency."
            self.B4LoseText = "$username and his/her crewmates lost $points $currency each"
            self.B4AddWinChancePerAttendee = 0
            self.B4AddWinPointsPerAttendee = 0
            self.B5Name = "Lion"
            self.B5WinChance = 10
            self.B5Win = 80
            self.B5Lose = 15
            self.B5StartText = "$username you started a hunt against a $targetname. Win Chance: $winchance% - Total Win Points: $points - Added Win Chance per Attendee: $addedwinchance - Added Win Points per Attendee: $addedwinpoints! Everybody can join the hunt with $joincommand. Good Luck!"
            self.B5WinText = "$username and his/her $attendees crewmates have won $points $currency at the hunt against $targetname! So everybody won $attendeepoints $currency."
            self.B5LoseText = "$username and his/her crewmates lost $points $currency each"
            self.B5AddWinChancePerAttendee = 0
            self.B5AddWinPointsPerAttendee = 0
            self.HighestLose = 0

        # load variables that do not need to be customisable from the ui
        self.ActiveGame = False
        self.ActiveGameAttendees = []
        self.ActiveGameEnd = None
        self.BossStarterUserName = ""
        self.Boss = []
        self.selectedboss = 0

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
                    
            # send message about active hunt if one is active
            if MySet.ActiveGame:
                message = MySet.ActiveGameResponse.replace("$username", data.UserName).replace("$targetname", MySet.Boss[0]).replace("$joincommand", MySet.JoinCommand).replace("$remainingtime", str(round(MySet.ActiveGameEnd - time.time())))
                SendResp(data, message)
                return
                
            else:
                
                # define bosses
                MySet.Boss = [[MySet.B1Name, MySet.B1WinChance, MySet.B1Win, MySet.B1Lose, MySet.B1StartText.replace("$username", data.UserName).replace("$targetname", MySet.B1Name).replace("$winchance", str(MySet.B1WinChance)).replace("$points", str(MySet.B1Win)).replace("$addedwinchance", str(MySet.B1AddWinChancePerAttendee)).replace("$addedwinpoints", str(MySet.B1AddWinPointsPerAttendee)).replace("$joincommand", MySet.JoinCommand), MySet.B1WinText.replace("$username", data.UserName).replace("$targetname", MySet.B1Name).replace("$attendees", str(0)).replace("$points", str(MySet.B1Win)).replace("$currency", Parent.GetCurrencyName()).replace("$attendeepoints", str(MySet.B1Win)), MySet.B1LoseText.replace("$username", data.UserName).replace("$targetname", MySet.B1Name).replace("$points", str(MySet.B1Lose)).replace("$currency", Parent.GetCurrencyName()), MySet.B1AddWinChancePerAttendee, MySet.B1AddWinPointsPerAttendee], \
                            [MySet.B2Name, MySet.B2WinChance, MySet.B2Win, MySet.B2Lose, MySet.B2StartText.replace("$username", data.UserName).replace("$targetname", MySet.B2Name).replace("$winchance", str(MySet.B2WinChance)).replace("$points", str(MySet.B2Win)).replace("$addedwinchance", str(MySet.B2AddWinChancePerAttendee)).replace("$addedwinpoints", str(MySet.B2AddWinPointsPerAttendee)).replace("$joincommand", MySet.JoinCommand), MySet.B2WinText.replace("$username", data.UserName).replace("$targetname", MySet.B2Name).replace("$attendees", str(0)).replace("$points", str(MySet.B2Win)).replace("$currency", Parent.GetCurrencyName()).replace("$attendeepoints", str(MySet.B2Win)), MySet.B2LoseText.replace("$username", data.UserName).replace("$targetname", MySet.B2Name).replace("$points", str(MySet.B2Lose)).replace("$currency", Parent.GetCurrencyName()), MySet.B2AddWinChancePerAttendee, MySet.B2AddWinPointsPerAttendee], \
                            [MySet.B3Name, MySet.B3WinChance, MySet.B3Win, MySet.B3Lose, MySet.B3StartText.replace("$username", data.UserName).replace("$targetname", MySet.B3Name).replace("$winchance", str(MySet.B3WinChance)).replace("$points", str(MySet.B3Win)).replace("$addedwinchance", str(MySet.B3AddWinChancePerAttendee)).replace("$addedwinpoints", str(MySet.B3AddWinPointsPerAttendee)).replace("$joincommand", MySet.JoinCommand), MySet.B3WinText.replace("$username", data.UserName).replace("$targetname", MySet.B3Name).replace("$attendees", str(0)).replace("$points", str(MySet.B3Win)).replace("$currency", Parent.GetCurrencyName()).replace("$attendeepoints", str(MySet.B3Win)), MySet.B3LoseText.replace("$username", data.UserName).replace("$targetname", MySet.B3Name).replace("$points", str(MySet.B3Lose)).replace("$currency", Parent.GetCurrencyName()), MySet.B3AddWinChancePerAttendee, MySet.B3AddWinPointsPerAttendee], \
                            [MySet.B4Name, MySet.B4WinChance, MySet.B4Win, MySet.B4Lose, MySet.B4StartText.replace("$username", data.UserName).replace("$targetname", MySet.B4Name).replace("$winchance", str(MySet.B4WinChance)).replace("$points", str(MySet.B4Win)).replace("$addedwinchance", str(MySet.B4AddWinChancePerAttendee)).replace("$addedwinpoints", str(MySet.B4AddWinPointsPerAttendee)).replace("$joincommand", MySet.JoinCommand), MySet.B4WinText.replace("$username", data.UserName).replace("$targetname", MySet.B4Name).replace("$attendees", str(0)).replace("$points", str(MySet.B4Win)).replace("$currency", Parent.GetCurrencyName()).replace("$attendeepoints", str(MySet.B4Win)), MySet.B4LoseText.replace("$username", data.UserName).replace("$targetname", MySet.B4Name).replace("$points", str(MySet.B4Lose)).replace("$currency", Parent.GetCurrencyName()), MySet.B4AddWinChancePerAttendee, MySet.B4AddWinPointsPerAttendee], \
                            [MySet.B5Name, MySet.B5WinChance, MySet.B5Win, MySet.B5Lose, MySet.B5StartText.replace("$username", data.UserName).replace("$targetname", MySet.B5Name).replace("$winchance", str(MySet.B5WinChance)).replace("$points", str(MySet.B5Win)).replace("$addedwinchance", str(MySet.B5AddWinChancePerAttendee)).replace("$addedwinpoints", str(MySet.B5AddWinPointsPerAttendee)).replace("$joincommand", MySet.JoinCommand), MySet.B5WinText.replace("$username", data.UserName).replace("$targetname", MySet.B5Name).replace("$attendees", str(0)).replace("$points", str(MySet.B5Win)).replace("$currency", Parent.GetCurrencyName()).replace("$attendeepoints", str(MySet.B5Win)), MySet.B5LoseText.replace("$username", data.UserName).replace("$targetname", MySet.B5Name).replace("$points", str(MySet.B5Lose)).replace("$currency", Parent.GetCurrencyName()), MySet.B5AddWinChancePerAttendee, MySet.B5AddWinPointsPerAttendee]]            
            
                MySet.HighestLose = MySet.B1Lose
            
                for BossIT in MySet.Boss:
                    if BossIT[3] > MySet.HighestLose:
                        MySet.HighestLose = BossIT[3]
            
                # check if user has more points than highest possible lost
                if not HasEnoughPoints(data, MySet.HighestLose + MySet.Cost):
                    return
            
                Parent.RemovePoints(data.User, data.UserName, MySet.Cost)
            
                # enable hunt
                MySet.ActiveGame = True
                MySet.ActiveGameEnd = time.time() + MySet.ActiveGameTime
                MySet.ActiveGameAttendees.append(data.User)
                MySet.BossStarterUserName = data.UserName
                
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
                if not HasEnoughPoints(data, MySet.HighestLose + MySet.Cost):
                    return
                
                # check if user already joined and send message if
                if data.User in MySet.ActiveGameAttendees:
                    message = MySet.AlreadyJoinedFight.replace("$username", data.UserName).replace("$targetname", MySet.Boss[0])
                    SendResp(data, message)
                    return
            
                # subtract usage costs
                Parent.RemovePoints(data.User, data.UserName, MySet.Cost)
                
                
                # recalculate win chance after adding new attendee
                if MySet.Boss[1] + MySet.Boss[7] < 100:
                    MySet.Boss[1] += MySet.Boss[7]
                else:
                    MySet.Boss[1] = 100
                # recalculate win points after adding new attendee
                MySet.Boss[2] += MySet.Boss[8]
                       
                # add user to game and notify
                MySet.ActiveGameAttendees.append(data.User)
                message = MySet.JoinedFightResponse.replace("$username", data.UserName).replace("$targetname", MySet.Boss[0]).replace("$attendees", str(len(MySet.ActiveGameAttendees))).replace("$winchance", str(MySet.Boss[1])).replace("$points", str(MySet.Boss[2])).replace("$currency", Parent.GetCurrencyName()).replace("$attendeepoints", str(MySet.Boss[2]/len(MySet.ActiveGameAttendees)))
                SendResp(data, message)  

                # update WinText message
                if MySet.selectedboss == 0:
                    MySet.Boss[5] = MySet.B1WinText.replace("$username", MySet.BossStarterUserName).replace("$targetname", MySet.B1Name).replace("$attendees", str(len(MySet.ActiveGameAttendees)-1)).replace("$points", str(MySet.Boss[2])).replace("$currency", Parent.GetCurrencyName()).replace("$attendeepoints", str(MySet.Boss[2]/len(MySet.ActiveGameAttendees)))
                elif MySet.selectedboss == 1:
                    MySet.Boss[5] = MySet.B2WinText.replace("$username", MySet.BossStarterUserName).replace("$targetname", MySet.B2Name).replace("$attendees", str(len(MySet.ActiveGameAttendees)-1)).replace("$points", str(MySet.Boss[2])).replace("$currency", Parent.GetCurrencyName()).replace("$attendeepoints", str(MySet.Boss[2]/len(MySet.ActiveGameAttendees)))
                elif MySet.selectedboss == 2:
                    MySet.Boss[5] = MySet.B3WinText.replace("$username", MySet.BossStarterUserName).replace("$targetname", MySet.B3Name).replace("$attendees", str(len(MySet.ActiveGameAttendees)-1)).replace("$points", str(MySet.Boss[2])).replace("$currency", Parent.GetCurrencyName()).replace("$attendeepoints", str(MySet.Boss[2]/len(MySet.ActiveGameAttendees)))
                elif MySet.selectedboss == 3:
                    MySet.Boss[5] = MySet.B4WinText.replace("$username", MySet.BossStarterUserName).replace("$targetname", MySet.B4Name).replace("$attendees", str(len(MySet.ActiveGameAttendees)-1)).replace("$points", str(MySet.Boss[2])).replace("$currency", Parent.GetCurrencyName()).replace("$attendeepoints", str(MySet.Boss[2]/len(MySet.ActiveGameAttendees)))
                elif MySet.selectedboss == 4:
                    MySet.Boss[5] = MySet.B5WinText.replace("$username", MySet.BossStarterUserName).replace("$targetname", MySet.B5Name).replace("$attendees", str(len(MySet.ActiveGameAttendees)-1)).replace("$points", str(MySet.Boss[2])).replace("$currency", Parent.GetCurrencyName()).replace("$attendeepoints", str(MySet.Boss[2]/len(MySet.ActiveGameAttendees)))
            
            else:
                # notify that no game is active 
                message = MySet.NoActiveGameResponse.replace("$username", data.UserName).replace("$command", MySet.Command)
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
            message = MySet.MinAttendeesResponse.replace("$username", MySet.BossStarterUserName)
            Parent.SendStreamMessage(message)
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
                Parent.SendStreamMessage("/timeout {0} {1}".format(MySet.BossStarterUserName.lower(), MySet.TL))
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