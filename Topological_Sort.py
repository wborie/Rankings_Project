#Topological Sort

class TeamNode(object):

    def __init__(self , teamName , lostTo):
        self.teamName = teamName
        self.lostTo = lostTo

    def addTeamLostTo(self , newTeam):
        self.lostTo.append(newTeam)

    def getTeamsLostTo(self):
        result = []
        for x in self.lostTo:
            result.append(str(x))
        return result
    
    def __str__(self):
        return "Name: " + str(self.teamName)

elements = ["goggles" , "pants" , "boots" , "gloves" , "skis" , "helmet" , "scarf" , "socks" , "shirt" , "jacket"]
for x in xrange(len(elements)):
    elements[x] = TeamNode(elements[x] , [])

elements[0].addTeamLostTo(elements[3])
elements[1].addTeamLostTo(elements[4])
elements[1].addTeamLostTo(elements[3])
elements[1].addTeamLostTo(elements[2])
elements[5].addTeamLostTo(elements[0])
elements[6].addTeamLostTo(elements[9])
elements[7].addTeamLostTo(elements[4])
elements[8].addTeamLostTo(elements[6])
elements[8].addTeamLostTo(elements[9])

def top_sort(node , rankedList):
    if str(node) in rankedList:
        return
    if node.lostTo == []:
        rankedList.append(str(node))
        return
    else:
        while node.lostTo != []: #Remove all children
            top_sort(node.lostTo[0] , rankedList)
            node.lostTo.remove(node.lostTo[0])
        #No more children left, add yourself to list
        rankedList.append(str(node))
        return


for x in elements:
        print str(x) + "\nTeams lost to: " + str(x.getTeamsLostTo())

print "===="

rankedList = []
for x in xrange(len(elements)):
    top_sort(elements[x] , rankedList)
    
print rankedList



