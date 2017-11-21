INFO_LINE_INDICATOR = "Rk"
MATCH_NUM = 0
#DATE = 1
#TIME = 2
#DAY = 3
WINNER = 4
WINNER_POINTS = 5
LOSER = 7
LOSER_POINTS = 8

import copy
class Match(object):

    def __init__(self , seasonNumber , winner , winnerPoints , loser , \
                 loserPoints): #Constructor
        self.seasonNumber = seasonNumber
        self.winner = winner
        self.winnerPoints = winnerPoints
        self.loser = loser
        self.loserPoints = loserPoints
        self.isTie = (winnerPoints == loserPoints)
        
    def __str__(self): #toString
        if not self.isTie:
            return str(self.winner) + " (" + str(self.winnerPoints) + ") beat " + \
               str(self.loser) + " (" + str(self.loserPoints) + ")."
        else:
            return str(self.winner) + " (" + str(self.winnerPoints) + ") tied " + \
               str(self.loser) + " (" + str(self.loserPoints) + ")."


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
    
def readFile(filename):
    f = open(filename , "r")
    matches = []
    for line in f:
        line = line.strip()
        newMatch = createMatch(line)
        if not newMatch == None:
            matches.append(newMatch)
    f.close()
    return matches

def createMatch(data):
    tempArray = data.split(",")
    if not tempArray[0] == INFO_LINE_INDICATOR:
        matchNum = int(tempArray[MATCH_NUM])
        winner = str(tempArray[WINNER])
        winner = winner.strip()
        newWinner = ""
        for i in xrange(len(winner)):
            if winner[i].isalpha() or winner[i] == " ":
                newWinner += winner[i]
        winnerPoints = str(tempArray[WINNER_POINTS])
        loser = str(tempArray[LOSER])
        loser = loser.strip()
        newLoser = ""
        for i in xrange(len(loser)):
            if loser[i].isalpha() or loser[i] == " ":
                newLoser += loser[i]
        loserPoints = str(tempArray[LOSER_POINTS])
        temp = Match(matchNum , newWinner , winnerPoints , newLoser , loserPoints)
        return temp
    else:
        return None

def createTeams(matches):
    teams = []
    for element in matches:
        team1 = element.winner
        team2 = element.loser
        if not team1 in teams:
            teams.append(team1)
        if not team2 in teams:
            teams.append(team2)
    teamNodes = copy.deepcopy(teams)
    for x in xrange(len(teams)):
        teamNodes[x] = TeamNode(teamNodes[x] , [])
    return teams , teamNodes

def implementMatchResults(matches , teams , teamNodes):
    for match in matches:
        if not match.isTie: #There is a winner and a loser
            winner = match.winner
            loser = match.loser
            indexOfWinner = teams.index(winner)
            indexOfLoser = teams.index(loser)
            teamNodes[indexOfLoser].addTeamLostTo(teamNodes[indexOfWinner])

def topologicalSort(node , rankedList , traversalsMade , breakOut):
    if breakOut[0]:
        return
    if str(node) in rankedList:
        return
    if node.lostTo == []:
        rankedList.append(str(node))
        return
    else:
        while node.lostTo != []: #Remove all children
            if ([str(node) , str(node.lostTo[0])]) in traversalsMade:
                print "Traversal already made."
                breakOut[0] = True
                return
            traversalsMade.append([str(node) , str(node.lostTo[0])])
            topologicalSort(node.lostTo[0] , rankedList , traversalsMade , breakOut)
            node.lostTo.remove(node.lostTo[0])
        #No more children left, add yourself to list
        rankedList.append(str(node))
        return

def run():
    matches = readFile("Ski Test.txt")
    teams , teamNodes = createTeams(matches)
    implementMatchResults(matches , teams , teamNodes)

    for x in teamNodes:
        print str(x) + "\nTeams lost to: " + str(x.getTeamsLostTo())
    print "==="
    resultRanks = []
    for x in xrange(len(teamNodes)):
        containsChains = [False]
        topologicalSort(teamNodes[x] , resultRanks , [] , containsChains)
        if containsChains[0]:
            print "This data set contains chains. Proceeding to tiebreaking."
            break
    if containsChains[0]:
        print "Point sort"
        pointSort(teamNodes)
    else:
        print resultRanks #THIS IS WHEN THERE ARE NO CHAINS AND YOU CAN KEEP
        #RESULTRANKS AS THE FINAL RESULT

def pointSort(teams):
    
    
run()

#Determining whether or not there are chains that need to be dealt with:
#First, call topological sort. Have a blank array for traversal-storage.
#Each time you make a traversal, append [the parent node's team name ,
#the child node's team name] into the array. Whenever you're about to make a
#traversal, check if the parent --> child is in the traversal-storage array. If it is,
#break out of the recursion and mark the data set as a structure containing chains.
#Make sure that at the end of each recursive call, reset the traversal-storage array.
