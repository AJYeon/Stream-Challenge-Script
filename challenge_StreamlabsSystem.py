#---------------------------
#   Import Libraries
#---------------------------
import os
import sys
#libFolder = os.path.join(os.path.dirname(__file__), "lib")
#sys.path.append(libFolder)
import Fighter


# chatbot won't load a script that doesn't define these variables
ScriptName = "Challenge"
Website = "https://streamlabs.com"
Description = "Fire Emblem Combat simulator game"
Creator = "StreamMin"
Version = "1.0.0"    

# global data used by the script
userLineNumber = 0
#winLossRecord = ""
#scriptDirectory = ""
recordFile = "challenge_record.txt"
configFile = "config.json"
path = ''
records = []
settings = {}


def changeFileDirectory():

    rootDirectory = os.getcwd()
    twitchDirectory = os.path.join(rootDirectory,"Twitch")
    fileDirectory = os.path.join(twitchDirectory,"Files")
    print(fileDirectory)
    os.chdir(fileDirectory)


def writeTextFile(filename,content):
    with open(filename,"w") as f:
        f.writelines(content)
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
                        "maxChallenger": 1,
			"responseAnnouncement": "Whoever writes $word first gets $reward $currency!",
			"wonResponse": "$user wrote $word first and won $reward $currency!"
		}
        return

    

# called whenever the chatbot has data - chat messages, whispers, etc. - that
# your script might care about
def Execute(data):
    global userLineNumber, winLossRecord, scriptDirectory, recordFile, records
    if data.IsChatMessage() and data.GetParam(0).lower() == '!challenge' and Parent.HasPermission(data.User, settings["permission"], "") and ((settings["liveOnly"] and Parent.IsLive()) or (not settings["liveOnly"])):
        try:
            cooldownCheck = Parent.IsOnCooldown(ScriptName,'!challenge')
            if not cooldownCheck:
                Parent.AddCooldown(ScriptName,"!challenge",settings["cooldown"])  # Put the command on cooldown
            userFound = False
            userLineNumber = 0
            recordPath = os.path.join(path, recordFile)
            records = readTextFile(recordPath)
            for line in records:
                if line[line.find("name") + 5:line.find("weapon1")-1] == data.User:
                    fightState = line[line.find("fight") + 6:line.find("record")-1]
                    if fightState: # Continue the FIGHT!
                        userWeapon = line[line.find("weapon1") + 8:line.find("weapon2")-1]
                        userHitPoints = line[line.find("HP1") + 4:line.find("HP2")-1]
                        winLossRecord = line[line.find("record") + 7:len(line)]
                        challenger = Fighter.fighter(data.User,weapon = userWeapon, hitPoints = userHitPoints)
                        challenger.setWeaponStats()
                        sigrdminWeapon = line[line.find("weapon2") + 8:line.find("HP1")-1]
                        sigrdminHitPoints = line[line.find("HP2") + 4:line.find("fight")-1]
                        sigrdmin = Fighter.fighter(data.User,weapon = sigrdminWeapon, hitPoints = sigrdminHitPoints)
                        sigrdmin.setWeaponStats()
                        userFound = True
                        break
                    else: # Start a new FIGHT!
                        challenger = Fighter.fighter(data.User)
                        userWeapon = challenger.pickWeaponUser()
                        challenger.setWeaponStats()
                        sigrdmin = Fighter.fighter("SIGRDMIN")
                        sigrdminWeapon = sigrdmin.pickWeaponSigurd()
                        sigrdmin.setWeaponStats()
                        userFound = True
                        break
                userLineNumber += 1
            if not userFound:
                challenger = Fighter.fighter(data.User)
                userWeapon = challenger.pickWeaponUser()
                challenger.setWeaponStats()
                sigrdmin = Fighter.fighter("SIGRDMIN")
                sigrdminWeapon = sigrdmin.pickWeaponSigurd()
                sigrdmin.setWeaponStats()
                winLossRecord = "0-0"
            Parent.SendStreamMessage("| " + data.User + " vs. " + sigrdmin.returnName() + " |")
            Parent.SendStreamMessage(sigrdmin.returnName() + " unsheathes " + sigurdWeapon + "! " + data.User + "unsheathes " + userWeapon + "!")
            initiative = Parent.GetRandom(1, 2)
            if initiative == 1:
                initiativeFighter = data.User
                secondFighter = sigrdmin.returnName()
                initiativeState = challenger.getAttackState()
                if initiativeState[:7] != "misses!":
                    sigrdmin.takeDamage(challenger.returnDamage())
            else:
                initiativeFighter = sigrdmin.returnName()
                Parent.SendStreamMessage(sigrdmin.pickAttack())
                secondFighter = data.User
                initiativeState = sigrdmin.getAttackState()
                if initiativeState[:7] != "misses!":
                    challenger.takeDamage(sigrdmin.returnDamage())
            Parent.SendStreamMessage(initiativeFighter + " has the initiative! " + initiativeFighter + initiativeState)
            if initiativeFighter == data.User:
                if sigrdmin.returnHP() != 0:
                    counterState = sigrdmin.getAttackState()
                    if counterState[:7] != "misses!":
                        challenger.takeDamage(sigrdmin.returnDamage())
                    Parent.SendStreamMessage(sigrdmin.pickAttack())
                    Parent.SendStreamMessage(secondFighter + "retaliates!" + secondFighter + counterState)
                    if challenger.returnHP() != 0:
                        records[usrLineNumber] = "name=" + data.User + " weapon1=" + userWeapon + " weapon2=" + sigurdWeapon + " HP1=" + challenger.returnHP() + " HP2=" + sigrdmin.returnHP() + " fight=True record=" + winLossRecord + "\n"
                        #changeFileDirectory()
                        writeTextFile(recordPath,records)
                        #os.chdir(scriptDirectory)
                        Parent.SendStreamMessage(sigrdmin.pickSurvive() + " | CURRENT SITUATION:" + data.User + "'s HP: " + challenger.returnHP() + " " + sigrdmin.returnName() + "'s HP: " + sigrdmin.returnHP() + " |")
                    else:
                        sigrdminScore = winLossRecord[winLossRecord.find("-") + 1:]
                        updatedRecord = winLossRecord[:winLossRecord.find("-") +1] + str(int(sigrdminScore) + 1)
                        records[usrLineNumber] = "name=" + data.User + " weapon1= weapon2= HP1= HP2= fight=False record=" + updatedRecord + "\n"
                        #changeFileDirectory()
                        writeTextFile(recordPath,records)
                        #os.chdir(scriptDirectory)
                        Parent.SendStreamMessage(sigrdmin.pickVictory() + " | CURRENT RECORD:" + data.User + " " + updatedRecord + " " + sigrdmin.returnName() + " |")   
                else:
                    usrScore = winLossRecord[:winLossRecord.find("-")]
                    updatedRecord = str(int(usrScore) + 1) + winLossRecord[winLossRecord.find("-"):]
                    records[usrLineNumber] = "name=" + data.User + " weapon1= weapon2= HP1= HP2= fight=False record=" + updatedRecord + "\n"
                    #changeFileDirectory()
                    writeTextFile(recordPath,records)
                    #os.chdir(scriptDirectory)
                    Parent.SendStreamMessage(sigrdmin.pickDefeat() + " | CURRENT RECORD: " + data.User + " " + updatedRecord + " " + sigrdmin.returnName() + " |")
            elif initiativeFighter == sigrdmin.returnName():
                if challenger.returnHP() != 0:
                    counterState = challenger.getAttackState()
                    if counterState[:7] != "misses!":
                        sigrdmin.takeDamage(challenger.returnDamage())
                    Parent.SendStreamMessage(secondFighter + "retaliates!" + secondFighter + counterState)
                    if sigrdmin.returnHP() != 0:
                        records[usrLineNumber] = "name=" + data.User + " weapon1=" + userWeapon + " weapon2=" + sigurdWeapon + " HP1=" + challenger.returnHP() + " HP2=" + sigrdmin.returnHP() + " fight=True record=" + winLossRecord + "\n"
                        #changeFileDirectory()
                        writeTextFile(recordPath,records)
                        #os.chdir(scriptDirectory)
                        Parent.SendStreamMessage(sigrdmin.pickSurvive() + " | CURRENT SITUATION:" + data.User + "'s HP: " + challenger.returnHP() + " " + sigrdmin.returnName() + "'s HP: " + sigrdmin.returnHP() + " |")
                    else:
                        usrScore = winLossRecord[:winLossRecord.find("-")]
                        updatedRecord = str(int(usrScore) + 1) + winLossRecord[winLossRecord.find("-"):]
                        records[usrLineNumber] = "name=" + data.User + " weapon1= weapon2= HP1= HP2= fight=False record=" + updatedRecord + "\n"
                        #changeFileDirectory()
                        writeTextFile(recordPath,records)
                        #os.chdir(scriptDirectory)
                        Parent.SendStreamMessage(sigrdmin.pickDefeat() + " | CURRENT RECORD: " + data.User + " " + updatedRecord + " " + sigrdmin.returnName() + " |")
                else:
                    sigrdminScore = winLossRecord[winLossRecord.find("-") + 1:]
                    updatedRecord = winLossRecord[:winLossRecord.find("-") +1] + str(int(sigrdminScore) + 1)
                    records[usrLineNumber] = "name=" + data.User + " weapon1= weapon2= HP1= HP2= fight=False record=" + updatedRecord + "\n"
                    #changeFileDirectory()
                    writeTextFile(recordPath,records)
                    #os.chdir(scriptDirectory)
                    Parent.SendStreamMessage(sigrdmin.pickVictory() + " | CURRENT RECORD:" + data.User + " " + updatedRecord + " " + sigrdmin.returnName() + " |")
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
