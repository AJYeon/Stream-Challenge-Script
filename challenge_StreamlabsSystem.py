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
sigrdmin = None
challenger = None
userWeapon = ""
sigrdminWeapon = ""
userLineNumber = 0
winLossRecord = ""
scriptDirectory = ""
recordFile = ""
records = []


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
    

# called when your script starts up
def Init():
    global recordFile,records
    """
    scriptDirectory = os.getcwd()
    changeFileDirectory()
    """
    recordFile = os.path.join(libFolder,"challenge_record.txt")
    with open(recordFile,"r") as f:
        records = f.readlines()
    records = [line.rstrip("\n") for line in records]
    f.close()
    #os.chdir(scriptDirectory)
       
    

# called whenever the chatbot has data - chat messages, whispers, etc. - that
# your script might care about
def Execute(data):
    global sigrdmin, challenger, userWeapon, sigrdminWeapon, userLineNumber, winLossRecord, scriptDirectory, recordFile, records
    if data.IsChatMessage() and data.GetParam(0).lower() == '!challenge':
        try:
            userFound = False
            userLineNumber = 0
            for user in records:
                userLineNumber = user
                if records[user][records[user].find("name") + 5:records[user].find("weapon1")-1] == data.User:
                    fightState = records[user][records[user].find("fight") + 6:records[user].find("record")-1]
                    if fightState:
                        userWeapon = records[user][records[user].find("weapon1") + 8:records[user].find("weapon2")-1]
                        userHitPoints = records[user][records[user].find("HP1") + 4:records[user].find("HP2")-1]
                        winLossRecord = records[user][records[user].find("record") + 7:len(records[user])]
                        challenger = Fighter.fighter(data.User,weapon = userWeapon, hitPoints = userHitPoints)
                        challenger.setWeaponStats()
                        sigrdminWeapon = records[user][records[user].find("weapon2") + 8:records[user].find("HP1")-1]
                        sigrdminHitPoints = records[user][records[user].find("HP2") + 4:records[user].find("fight")-1]
                        sigrdmin = Fighter.fighter(data.User,weapon = sigrdminWeapon, hitPoints = sigrdminHitPoints)
                        sigrdmin.setWeaponStats()
                        userFound = True
                        break
                    else:
                        challenger = Fighter.fighter(data.User)
                        userWeapon = challenger.pickWeaponUser()
                        challenger.setWeaponStats()
                        sigrdmin = Fighter.fighter("SIGRDMIN")
                        sigrdminWeapon = sigrdmin.pickWeaponSigurd()
                        sigrdmin.setWeaponStats()
                        userFound = True
                        break
            if not userFound:
                userLineNumber += 1
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
                        writeTextFile(recordFile,records)
                        #os.chdir(scriptDirectory)
                        Parent.SendStreamMessage(sigrdmin.pickSurvive() + " | CURRENT SITUATION:" + data.User + "'s HP: " + challenger.returnHP() + " " + sigrdmin.returnName() + "'s HP: " + sigrdmin.returnHP() + " |")
                    else:
                        sigrdminScore = winLossRecord[winLossRecord.find("-") + 1:]
                        updatedRecord = winLossRecord[:winLossRecord.find("-") +1] + str(int(sigrdminScore) + 1)
                        records[usrLineNumber] = "name=" + data.User + " weapon1= weapon2= HP1= HP2= fight=False record=" + updatedRecord + "\n"
                        #changeFileDirectory()
                        writeTextFile(recordFile,records)
                        #os.chdir(scriptDirectory)
                        Parent.SendStreamMessage(sigrdmin.pickVictory() + " | CURRENT RECORD:" + data.User + " " + updatedRecord + " " + sigrdmin.returnName() + " |")   
                else:
                    usrScore = winLossRecord[:winLossRecord.find("-")]
                    updatedRecord = str(int(usrScore) + 1) + winLossRecord[winLossRecord.find("-"):]
                    records[usrLineNumber] = "name=" + data.User + " weapon1= weapon2= HP1= HP2= fight=False record=" + updatedRecord + "\n"
                    #changeFileDirectory()
                    writeTextFile(recordFile,records)
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
                        writeTextFile(recordFile,records)
                        #os.chdir(scriptDirectory)
                        Parent.SendStreamMessage(sigrdmin.pickSurvive() + " | CURRENT SITUATION:" + data.User + "'s HP: " + challenger.returnHP() + " " + sigrdmin.returnName() + "'s HP: " + sigrdmin.returnHP() + " |")
                    else:
                        usrScore = winLossRecord[:winLossRecord.find("-")]
                        updatedRecord = str(int(usrScore) + 1) + winLossRecord[winLossRecord.find("-"):]
                        records[usrLineNumber] = "name=" + data.User + " weapon1= weapon2= HP1= HP2= fight=False record=" + updatedRecord + "\n"
                        #changeFileDirectory()
                        writeTextFile(recordFile,records)
                        #os.chdir(scriptDirectory)
                        Parent.SendStreamMessage(sigrdmin.pickDefeat() + " | CURRENT RECORD: " + data.User + " " + updatedRecord + " " + sigrdmin.returnName() + " |")
                else:
                    sigrdminScore = winLossRecord[winLossRecord.find("-") + 1:]
                    updatedRecord = winLossRecord[:winLossRecord.find("-") +1] + str(int(sigrdminScore) + 1)
                    records[usrLineNumber] = "name=" + data.User + " weapon1= weapon2= HP1= HP2= fight=False record=" + updatedRecord + "\n"
                    #changeFileDirectory()
                    writeTextFile(recordFile,records)
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
    pass

                             
def Unload():
    return
