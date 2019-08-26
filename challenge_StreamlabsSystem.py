#---------------------------
#   Import Libraries
#---------------------------
import os
import sys
libFolder = os.path.join(os.path.dirname(__file__), "lib")
sys.path.append(libFolder)
import Fighter


# chatbot won't load a script that doesn't define these variables
ScriptName = "Challenge"
Website = "https://streamlabs.com"
Description = "Fire Emblem Combat simulator game"
Creator = "StreamMin"
Version = "1.0.0"    

# global data used by the script
userLineNumber = 0
recordFile = "challenge_record.txt"
configFile = "config.json"
path = ''
records = []
settings = {}


def writeTextFile(filename,content):
    with open(filename,"w") as f:
        f.writelines("%s\n" % line for line in content)
    f.close()

def readTextFile(filename):
    with open(filename,"r") as f:
        data = f.readlines()
    data = [line.rstrip("\n") for line in data]
    f.close()
    return data

def openRecordsFile():
    location = os.path.join(os.path.dirname(__file__), recordFile)
    os.startfile(location)
    return

# called when your script starts up
def Init():
    global settings, configFile, path
    path = os.path.dirname(__file__)
    try:
	with codecs.open(os.path.join(path, configFile), encoding='utf-8-sig', mode='r') as file:
            settings = json.load(file, encoding='utf-8-sig')
    except:
	settings = {
			"liveOnly": True,
			"permission": "Everyone",
			"minReward": 1,
			"maxReward": 10,
                        "cooldown": 60,
                        "maxChallenger": 1
	}

    

# called whenever the chatbot has data - chat messages, whispers, etc. - that
# your script might care about
def Execute(data):
    global userLineNumber, winLossRecord, scriptDirectory, recordFile, records
    if data.IsChatMessage() and data.GetParam(0).lower() == '!challenge' and Parent.HasPermission(data.User, settings["permission"], ""):
        try:
            cooldownCheck = Parent.IsOnCooldown(ScriptName,'!challenge')
            if not cooldownCheck:
                Parent.AddCooldown(ScriptName,"!challenge",settings["cooldown"])  # Put the command on cooldown
            user = data.UserName
            userFound = False
            userLineNumber = 0
            recordPath = os.path.join(path, recordFile)
            records = readTextFile(recordPath)
            for line in records:
                if line[line.find("name") + 5:line.find("weapon1")-1] == user:
                    fightState = line[line.find("fight") + 6:line.find("record")-1]
                    if fightState == "True": # Continue the FIGHT!
                        userWeapon = line[line.find("weapon1") + 8:line.find("weapon2")-1]
                        userHitPoints = int(line[line.find("HP1") + 4:line.find("HP2")-1])
                        challenger = Fighter.fighter(user,weapon = userWeapon, hitPoints = userHitPoints)
                        challenger.setWeaponStats()
                        sigrdminWeapon = line[line.find("weapon2") + 8:line.find("HP1")-1]
                        sigrdminHitPoints = int(line[line.find("HP2") + 4:line.find("fight")-1])
                        sigrdmin = Fighter.fighter("SIGRDMIN",weapon = sigrdminWeapon, hitPoints = sigrdminHitPoints)
                        sigrdmin.setWeaponStats()
                        winLossRecord = line[line.find("record") + 7:len(line)]
                        userFound = True
                        break
                    else: # Start a new FIGHT!
                        challenger = Fighter.fighter(user)
                        randomWeapon = Parent.GetRandom(0,3)
                        userWeapon = challenger.pickWeaponUser(randomWeapon)
                        challenger.setWeaponStats()
                        sigrdmin = Fighter.fighter("SIGRDMIN")
                        randomWeapon = Parent.GetRandom(0,4)
                        sigrdminWeapon = sigrdmin.pickWeaponSigurd(randomWeapon)
                        sigrdmin.setWeaponStats()
                        winLossRecord = line[line.find("record") + 7:len(line)]
                        userFound = True
                        break
                userLineNumber += 1
            if userFound == False:
                challenger = Fighter.fighter(user)
                randomWeapon = Parent.GetRandom(0,3)
                userWeapon = challenger.pickWeaponUser(randomWeapon)
                challenger.setWeaponStats()
                sigrdmin = Fighter.fighter("SIGRDMIN")
                randomWeapon = Parent.GetRandom(0,4)
                sigrdminWeapon = sigrdmin.pickWeaponSigurd(randomWeapon)
                sigrdmin.setWeaponStats()
                winLossRecord = "0-0"
            Parent.SendStreamMessage("| " + user + " ( HP : " + str(challenger.returnHP()) + " )" + " vs. " + sigrdmin.returnName() + " ( HP : " + str(sigrdmin.returnHP()) + " )" + " |")
            Parent.SendStreamMessage(sigrdmin.returnName() + " unsheathes " + sigrdminWeapon + "! " + user + " unsheathes " + userWeapon + "!")
            initiative = Parent.GetRandom(0,2)
            if initiative == 0:
                initiativeFighter = user
                secondFighter = sigrdmin.returnName()
                hitRoll = Parent.GetRandom(0,100)
                initiativeState = challenger.getAttackState(hitRoll)
                quoteLength = len(initiativeState)
                if initiativeState[quoteLength - 7: quoteLength] != "misses!":
                    Parent.SendStreamMessage(str(challenger.returnDamage()))
                    sigrdmin.takeDamage(challenger.returnDamage())
            else:
                initiativeFighter = sigrdmin.returnName()
                Parent.SendStreamMessage(sigrdmin.pickAttack())
                secondFighter = user
                hitRoll = Parent.GetRandom(0,100)
                initiativeState = sigrdmin.getAttackState(hitRoll)
                quoteLength = len(initiativeState)
                if initiativeState[quoteLength - 7: quoteLength] != "misses!":
                    challenger.takeDamage(sigrdmin.returnDamage())
            Parent.SendStreamMessage(initiativeFighter + " has the initiative! " + initiativeFighter + initiativeState)
            if initiativeFighter == user:
                if int(sigrdmin.returnHP()) != int(0):
                    hitRoll = Parent.GetRandom(0,100)
                    counterState = sigrdmin.getAttackState(hitRoll)
                    quoteLength = len(counterState)
                    if counterState[quoteLength - 7: quoteLength] != "misses!":
                        challenger.takeDamage(sigrdmin.returnDamage())
                    Parent.SendStreamMessage(sigrdmin.pickAttack())
                    Parent.SendStreamMessage(secondFighter + " retaliates! " + secondFighter + counterState)
                    if int(challenger.returnHP()) != int(0):
                        if userFound == False:
                            records.append("name=" + user + " weapon1=" + userWeapon + " weapon2=" + sigrdminWeapon + " HP1=" + str(challenger.returnHP()) + " HP2=" + str(sigrdmin.returnHP()) + " fight=True record=" + winLossRecord)
                        else:
                            records[userLineNumber] = "name=" + user + " weapon1=" + userWeapon + " weapon2=" + sigrdminWeapon + " HP1=" + str(challenger.returnHP()) + " HP2=" + str(sigrdmin.returnHP()) + " fight=True record=" + winLossRecord
                        writeTextFile(recordPath,records)
                        Parent.SendStreamMessage(sigrdmin.pickSurvive())
                        Parent.SendStreamMessage(" | CURRENT SITUATION : " + user + " ( HP : " + str(challenger.returnHP()) + " )" + " vs. " + sigrdmin.returnName() + " ( HP : " + str(sigrdmin.returnHP()) + " )" + " |")
                    else:
                        sigrdminScore = winLossRecord[winLossRecord.find("-") + 1:]
                        updatedRecord = winLossRecord[:winLossRecord.find("-") +1] + str(int(sigrdminScore) + 1)
                        if userFound == False:
                            records.append("name=" + user + " weapon1= weapon2= HP1= HP2= fight=False record=" + updatedRecord)
                        else:
                            records[userLineNumber] = "name=" + user + " weapon1= weapon2= HP1= HP2= fight=False record=" + updatedRecord
                        writeTextFile(recordPath,records)
                        Parent.SendStreamMessage(sigrdmin.pickVictory())
                        Parent.SendStreamMessage(" | CURRENT RECORD: " + user + " " + updatedRecord + " " + sigrdmin.returnName() + " |") 
                else:
                    usrScore = winLossRecord[:winLossRecord.find("-")]
                    updatedRecord = str(int(usrScore) + 1) + winLossRecord[winLossRecord.find("-"):]
                    if userFound == False:
                        records.append("name=" + user + " weapon1= weapon2= HP1= HP2= fight=False record=" + updatedRecord)
                    else:
                        records[userLineNumber] = "name=" + user + " weapon1= weapon2= HP1= HP2= fight=False record=" + updatedRecord
                    writeTextFile(recordPath,records)
                    Parent.SendStreamMessage(sigrdmin.pickDefeat())
                    Parent.SendStreamMessage(" | CURRENT RECORD: " + user + " " + updatedRecord + " " + sigrdmin.returnName() + " |")
            elif initiativeFighter == sigrdmin.returnName():
                if int(challenger.returnHP()) != int(0):
                    hitRoll = Parent.GetRandom(0,100)
                    counterState = challenger.getAttackState(hitRoll)
                    quoteLength = len(counterState)
                    if counterState[quoteLength - 7: quoteLength] != "misses!":
                        sigrdmin.takeDamage(challenger.returnDamage())
                    Parent.SendStreamMessage(secondFighter + " retaliates! " + secondFighter + counterState)
                    if int(sigrdmin.returnHP()) != int(0):
                        if userFound == False:
                            records.append("name=" + user + " weapon1=" + userWeapon + " weapon2=" + sigrdminWeapon + " HP1=" + str(challenger.returnHP()) + " HP2=" + str(sigrdmin.returnHP()) + " fight=True record=" + winLossRecord)
                        else:
                            records[userLineNumber] = "name=" + user + " weapon1=" + userWeapon + " weapon2=" + sigrdminWeapon + " HP1=" + str(challenger.returnHP()) + " HP2=" + str(sigrdmin.returnHP()) + " fight=True record=" + winLossRecord
                        writeTextFile(recordPath,records)
                        Parent.SendStreamMessage(sigrdmin.pickSurvive())
                        Parent.SendStreamMessage(" | CURRENT SITUATION : " + user + " ( HP : " + str(challenger.returnHP()) + " )" + " vs. " + sigrdmin.returnName() + " ( HP : " + str(sigrdmin.returnHP()) + " )" + " |")
                    else:
                        userScore = winLossRecord[:winLossRecord.find("-")]
                        updatedRecord = str(int(userScore) + 1) + winLossRecord[winLossRecord.find("-"):]
                        if userFound == False:
                            records.append("name=" + user + " weapon1= weapon2= HP1= HP2= fight=False record=" + updatedRecord)
                        else:
                            records[userLineNumber] = "name=" + user + " weapon1= weapon2= HP1= HP2= fight=False record=" + updatedRecord
                        writeTextFile(recordPath,records)
                        Parent.SendStreamMessage(sigrdmin.pickDefeat())
                        Parent.SendStreamMessage(" | CURRENT RECORD: " + user + " " + updatedRecord + " " + sigrdmin.returnName() + " |")
                else:
                    sigrdminScore = winLossRecord[winLossRecord.find("-") + 1:]
                    updatedRecord = winLossRecord[:winLossRecord.find("-") +1] + str(int(sigrdminScore) + 1)
                    if userFound == False:
                        records.append("name=" + user + " weapon1= weapon2= HP1= HP2= fight=False record=" + updatedRecord)
                    else:
                        records[userLineNumber] = "name=" + user + " weapon1= weapon2= HP1= HP2= fight=False record=" + updatedRecord
                    writeTextFile(recordPath,records)
                    Parent.SendStreamMessage(sigrdmin.pickVictory())
                    Parent.SendStreamMessage(" | CURRENT RECORD: " + user + " " + updatedRecord + " " + sigrdmin.returnName() + " |")
        except:
            pass
            
# called frequently to mark the passage of time; if there's some condition
# your bot wants to act on *other* than data from the bot, and if you can
# write code that watches for that condition, it can go here; but beware this
# gets run frequently, so if the check is resource-intensive then you don't
# want to run it on *every* tick
                             
def Tick():
    return

#---------------------------
# Parse method (Allows you to create your own custom $parameters) TODO: Print leaderboard against Sigrdmin
#---------------------------
"""                                                                        
def Parse(parseString, userid, username, targetid, targetname, message):
    
    if "$myparameter" in parseString:
        return parseString.replace("$myparameter","I am a cat!")
    
    return parseString
"""
                                                                            
def Unload():
    return
