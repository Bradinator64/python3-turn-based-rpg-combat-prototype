import random, time
class Battle:
    def __init__(self, combatants):
        #Superlist of all combatants taking part in the battle.
        self.combatants = combatants
        #List of PC combatants
        self.combatantsPC = []
        #list of NPC combatants
        self.combatantsNPC = []
        #Boolean controlling if the battle is ongoing.
        self.inCombat = True

        #call the object's own .setup() and .battle() functions.
        self.setup()
        self.battle()

    #setup function to get the battle ready to be fought by sorting the creatures into teams and printing the teams taking part in the battle.
    def setup(self):
        #Sort combatants in list in order of their "speed" stat (combatant: combatant.speed) starting with the highest and ending with the lowest (reverse=True).
        self.combatants = sorted(self.combatants, key=lambda combatant: combatant.speed, reverse=True)
        for c in self.combatants:
            #If the creature is an instance of the PCCreature object, add it to the battle's list of PC combatants.
            if type(c).__name__ == "PCCreature":
                self.combatantsPC.append(c)
            #Else if the creature is an instance of the NPCCreature object, add it to the battle's list of NPC combatants.
            elif type(c).__name__ == "NPCCreature":
                self.combatantsNPC.append(c)
        #Print out the list of allied combatants.
        print("Allied Combatants:")
        for c in self.combatantsPC:
            print(c.name.title())
        print()
        #Print out the list of enemy combatants.
        print("Enemy Combatants:")
        for c in self.combatantsNPC:
            print(c.name.title())
        print("------------------------------------------")
        #Print turn order
        print("Turn Order: ")
        for c in self.combatants:
            print(c.name.title())
        print("------------------------------------------")

    def battle(self):
        while self.inCombat == True:
            #For each combatant in the battle's combatant list
            for combatant in self.combatants:
                #print the combatants name
                print(combatant.name + "'s turn")
                #call the combatant's selectAction() method (remember, each combatant is an object with a selectAction method)
                combatant.selectAction(self)
                print()
                print("------------------------------------------")
                #Run the battle object's checkDead() method.
                self.checkDead()
                #If the player combatant's list is empty (i.e. they've all been killed).
                if self.combatantsPC == []:
                    self.endBattle("enemy combatants")
                    #end the combat encounter.
                    self.inCombat = False
                    break
                #If the enemy combatant's list is empty (i.e. they've all been killed).
                elif self.combatantsNPC == []:
                    self.endBattle("player combatants")
                    #end the combat encounter
                    self.inCombat = False
                    break

    def checkDead(self):
        #For all the combatants in the battle's combatant list.
        for combatant in self.combatants:
            #Check if the combatant's isDead boolean is true.
            if combatant.isDead == True:
                #If the combatant is an object of type PCCreature.
                if type(combatant).__name__ == "PCCreature":
                    #Delete combatant from the list of player combatants.
                    self.combatantsPC.remove(combatant)
                #Else if the combatant is an object of type NPCCreature.
                elif type(combatant).__name__ == "NPCCreature":
                    #Delete the combatant from the list of enemy combatants.
                    self.combatantsNPC.remove(combatant)
                #Delete the combatant from the battle's combatant superlist.
                self.combatants.remove(combatant)
        
    #Takes a string argument.
    def endBattle(self, winner):
        print(str(winner) + " are victorious!")
        input()
        
#The superclass of all creatures, is the parent class of PCCreature and NPCCreature.
class Creature:
    def __init__(self, name, maxHP, speed, actions=[]):
        self.name = name
        self.maxHP = maxHP
        self.HP = maxHP
        self.speed = speed
        self.actions = actions
        self.isDead = False

    def printStats(self, withActions=False): #prints out the stat block of the object
        print("Name: " + self.name)
        print()
        print("HP: " + str(self.HP))
        print("Speed: " + str(self.speed))
        print()
        if withActions:
            self.printActions()

    def printActions(self): #prints all actions the object has
        for a in self.actions:
            print(a.name)

    def hasAction(self, action): #checks whether the object contains a specific action
        found = False
        for a in self.actions:
            if action.lower() == a.name.lower():
                found = True
                return a
        return False

    def takeDamage(self, value, stat="HP"):
        self.statAffected = stat
        statValue = getattr(self, self.statAffected)
        setattr(self, self.statAffected, statValue - value)
        self.printStats()
        if self.HP <= 0:
            self.isDead = True

    def restoreDamage(self, value, stat="HP"):
        self.statAffected = stat
        statValue = getattr(self, self.statAffected)
        if (stat == "HP") and (statValue + value >= self.maxHP):
            setattr(self, self.statAffected, self.maxHP)
        else:
            setattr(self, self.statAffected, statValue + value)
        self.printStats()

class PCCreature(Creature):
    def __init__(self, name, maxHP, speed, actions=[]):
        super().__init__(name, maxHP, speed, actions)
        self.targetList = []

    def selectAction(self, battle):
        action = self.selectActionToUse(battle)
        self.selectValidTarget(action, battle)

    def selectActionToUse(self, battle):
        self.printActions()
        playerHasAction = False
        while not playerHasAction:
            playerActionSelection = input("Select Action: ")
            playerActionSelection = self.hasAction(playerActionSelection)
            if playerActionSelection != False:
                if type(playerActionSelection).__name__ == "DamageAction":
                    self.targetList = battle.combatantsNPC[:]
                elif type(playerActionSelection).__name__ == "RestoreAction":
                    self.targetList = battle.combatantsPC[:]
                playerHasAction = True
                print(playerActionSelection.name)
                return playerActionSelection
            else:
                print(self.name + " does not possess that action.")

    def selectValidTarget(self, action, battle):
        playerSelectValidTarget = False
        """if type(action).__name__ == "DamageAction":
            targetList = battle.combatantsNPC
        elif type(action).__name__ == "RestoreAction":
            targetList = battle.combatantsPC"""
        while not playerSelectValidTarget:
            print("List of valid targets:")
            for target in self.targetList:
                print(target.name.title())
            print()
            playerTargetSelection = input("Select Ability Target: ").lower()
            if playerTargetSelection == "back":
                self.selectActionToUse(battle)
            else:    
                for target in self.targetList:
                    if target.name.lower() == playerTargetSelection:
                        action.effect(target)
                        playerSelectValidTarget = True
                if playerSelectValidTarget == False:
                    print("Invalid Target")
        

class NPCCreature(Creature):
    def __init__(self, name, maxHP, speed, actions=[]):
        super().__init__(name, maxHP, speed, actions)

    def selectAction(self, battle):
        time.sleep(1)
        npcActionNumber = random.randint(0, len(self.actions))
        npcAction = self.actions[npcActionNumber-1]
        if type(npcAction).__name__ == "DamageAction":
            targetNumber = random.randint(0, len(battle.combatantsPC))
            target = battle.combatantsPC[targetNumber-1]
            print(self.name + " is using " + str(npcAction.name.title()) + " on " + target.name)
            npcAction.effect(target)
        elif type(npcAction).__name__ == "RestoreAction":
            targetNumber = random.randint(0, len(battle.combatantsNPC))
            target = battle.combatantsNPC[targetNumber-1]
            print(self.name + " is using " + str(npcAction.name.title()) + " on " + target.name)
            npcAction.effect(target)
        time.sleep(1)


class Action:
    def __init__(self, name, value, stat="HP"):
        self.name = name
        self.value = value
        self.stat = stat

    def printAction(self):
        print()
        print("Action Name: " + self.name)
        print("Action Magnitude: " + str(self.value))
        print("Stat Affected: " + self.stat)

class DamageAction(Action):
    def __init__(self, name, value, stat="HP"):
        super().__init__(name, value, stat)

    def effect(self, target):
        print(target.name + " takes " + str(self.value) + " points of damage to " + self.stat)
        target.takeDamage(self.value, self.stat)

class RestoreAction(Action):
    def __init__(self, name, value, stat="HP"):
        super().__init__(name, value, stat)

    def effect(self, target):
        print(target.name + " has " + str(self.value) + " points restored to " + self.stat)
        target.restoreDamage(self.value, self.stat)
        
if __name__ == "__main__":
    # Action(name(string), value(int), stat(string)="HP")
    Attack = DamageAction("attack", 1)
    Heal = RestoreAction("heal", 2)
    PowerAttack = DamageAction("power attack", 4)

    # Creature(name(string), maxHP(int), speed(int), actions(array)=[])
    testPC = PCCreature("testPC", 10, 1, [Attack, Heal])
    testPC2 = PCCreature("testPC2", 20, 2, [Attack, PowerAttack])
    testNPC = NPCCreature("testNPC", 3, 0, [PowerAttack])
    testNPC2 = NPCCreature("testNPC2", 3, 0, [PowerAttack])

    # Battle(combatants(array))
    combatants = [testPC, testPC2, testNPC, testNPC2]
    testBattle = Battle(combatants)
