FILE_TO_READ = "ALL.txt"
INFO_LINE_INDICATOR = "Rk"

#Add 1 to the next 5 ints if using "ALL.txt"
MATCH_NUM = 1
WINNER = 5
WINNER_POINTS = 6
LOSER = 8
LOSER_POINTS = 9

DROP_OUT_MODIFIER = 1
POINT_SORT_TEST_AMOUNT = 1000000

import copy
import random
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
            return str(self.winner) + " (" + str(self.winnerPoints) + ") beat "\
                   + str(self.loser) + " (" + str(self.loserPoints) + ")."
        else:
            return str(self.winner) + " (" + str(self.winnerPoints) + ") tied "\
                   + str(self.loser) + " (" + str(self.loserPoints) + ")."


class TeamNode(object):

    def __init__(self , teamName , lostTo , beat , scoreDifference , points):
        self.teamName = teamName
        self.lostTo = lostTo
        self.beat = beat
        self.points = points
        self.scoreDifference = scoreDifference

    def addTeamBeat(self , newTeam):
        self.beat.append(newTeam)

    def addPoints(self , points):
        self.points += points

    def addTeamLostTo(self , newTeam , scoreDifference):
        self.lostTo.append(newTeam)
        self.scoreDifference.append(scoreDifference)

    def getTeamsBeat(self):
        result = []
        for x in self.beat:
            result.append(str(x))
        return result

    def getTeamsLostTo(self):
        result = []
        for x in self.lostTo:
            result.append(str(x))
        return result
    
    def __str__(self):
        return str(self.teamName)
    
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
        temp = Match(matchNum , newWinner , winnerPoints , newLoser ,\
                     loserPoints)
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
        teamNodes[x] = TeamNode(teamNodes[x] , [] , [] , [] , 0)
    return teams , teamNodes

def implementMatchResults(matches , teams , teamNodes):
    for match in matches:
        if not match.isTie: #There is a winner and a loser
            winner = match.winner
            loser = match.loser
            scoreDifference = int(match.winnerPoints) - int(match.loserPoints)
            indexOfWinner = teams.index(winner)
            indexOfLoser = teams.index(loser)
            teamNodes[indexOfLoser].addTeamLostTo(teamNodes[indexOfWinner] , \
                                                  scoreDifference)
            teamNodes[indexOfWinner].addTeamBeat(teamNodes[indexOfLoser])
        #If there's a tie, the match isn't counted.

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
                breakOut[0] = True
                return
            traversalsMade.append([str(node) , str(node.lostTo[0])])
            topologicalSort(node.lostTo[0] , rankedList , traversalsMade\
                            , breakOut)
            node.lostTo.remove(node.lostTo[0])
        #No more children left, add yourself to list
        rankedList.append(str(node))
        return

def pointSort(teamNodes):
    traversalCount = 0
    N = len(teamNodes)
    result = []
    while traversalCount < POINT_SORT_TEST_AMOUNT:
        randomStartIndex = random.randint(0 , N - 1)
        currentTeam = teamNodes[randomStartIndex]
        dropOut = False
        result = []
        currentTeam.addPoints(-1)
        while not dropOut:
            traversalCount += 1
            currentTeam.addPoints(1)
            lostTo = currentTeam.lostTo
            beat = currentTeam.beat
            if (float(len(beat)) + float(len(lostTo))) == 0:
                winLossRatio = 0
            else:
                winLossRatio = (float(len(beat)) / (float(len(beat)) + \
                                           float(len(lostTo))))
            if len(lostTo) == 0:
                dropOut = True
            elif random.randint(1 , 1000) < (winLossRatio * 1000 * \
                                             DROP_OUT_MODIFIER):
                dropOut = True
            else:
                traverseIndex = random.randint(0 , len(lostTo) - 1)
                currentTeam = lostTo[traverseIndex]
    while len(teamNodes) != 0:
        largest = 0
        for x in teamNodes:
            if x.points > largest:
                largest = x.points
        for x in xrange(len(teamNodes)):
            if teamNodes[x].points == largest:
                result.append(teamNodes[x])
                teamNodes.remove(teamNodes[x])
                break
    return result

def run():
    matches = readFile(FILE_TO_READ)
    teams , teamNodes = createTeams(matches)
    implementMatchResults(matches , teams , teamNodes)
    print "The Teams"
    for x in teamNodes:
        print str(x)
    print "============================================"
    resultRanks = []
    print "Attempting to run Topological Sort..."
    for x in xrange(len(teamNodes)):
        containsChains = [False]
        topologicalSort(teamNodes[x] , resultRanks , [] , containsChains)
        if containsChains[0]:
            print "This data set contains chains. Proceeding to use Point Sort."
            break
    if containsChains[0]:
        #Need to redo the matches because topological sort is destructive
        teams , teamNodes = createTeams(matches)
        implementMatchResults(matches , teams , teamNodes)
        print "Performing Point Sort..."
        result = pointSort(teamNodes)
        print "Results"
        for x in xrange(len(result)):
            print str(x + 1) + ". " + str(result[x]) + " | " + "Score: " + \
                  str(result[x].points)
    else:
        print "Results"
        for x in xrange(len(resultRanks)):
            print str(x + 1) + ". " + resultRanks[x]

run()
