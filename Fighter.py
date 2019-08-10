import random

class fighter:
    def __init__(self,name,weapon = None,hitPoints = None):
        self.name = name
        self.weapon = weapon
        self.hitPoints = 0
        self.accuracy = 0
        self.damage = 0
        self.attackState = ""
        
        if hitPoints:
            self.hitPoints = hitPoints
        else:
            self.hitPoints = 60

    def setWeaponStats(self):
        if self.weapon == "Iron Sword":
            self.accuracy = 80
            self.damage = 15
        elif self.weapon == "Steel Sword":
            self.accuracy = 70
            self.damage = 20
        elif self.weapon == "Silver Sword":
            self.accuracy = 60
            self.damage = 30
        elif self.weapon == "Tyrfing":
            self.accuracy = 90
            self.damage = 60
        
    def pickWeaponUser(self):
        weaponList = ["Iron Sword","Steel Sword","Silver Sword"]
        self.weapon = random.choice(weaponList)
        return self.weapon


    def pickWeaponSigurd(self):
        weaponList = ["Iron Sword","Steel Sword","Silver Sword","Tyrfing"]
        self.weapon = random.choice(weaponList)
        return self.weapon
        
    def pickAttack(self):
        if self.weapon == "Tyrfing":
            tyrfingQuote = "One strike will decide it all!"
            return tyrfingQuote
        else:
            attackQuoteList = ["Here I come!","Raise your sword!","You're as foul as they come!","You will pay for crossing Lord StreamMin", "I've come to exact justice upon you!"]
            return random.choice(attackQuoteList)

    def pickSurvive(self):
        surviveQuoteList =["I must get stronger.","I will not betray your confidence in me, Lord StreamMin","You dastard!"]
        return random.choice(surviveQuoteList)

    def pickDefeat(self):
        defeatQuoteList = ["What a poor example I set.","I must become stronger...","Deirdrew, I'm sorry."]
        return random.choice(defeatQuoteList)

    def pickVictory(self):
        victoryQuoteList = ["Deirdrew, thank you for watching over me","I apologize, I must uphold justice and honor!","Baldr's light shines upon me!"]
        return random.choice(defeatQuoteList)
        
    def returnName(self):
        return self.name

    def returnHP(self):
        return self.hitPoints

    def returnDamage(self):
        return self.damage

    def takeDamage(self,foeDamage):
        self.hitPoints -= foeDamage
        if self.hitPoints < 0:
            self.hitPoints = 0
        
    def getAttackState(self):
        RNG = random.randint(0,99)
        if RNG < self.accuracy:
            self.attackState = " hits for " + self.damage  + " damage!"
            return self.attackState
        else:
            self.attackState = " misses!"
            return self.attackState
