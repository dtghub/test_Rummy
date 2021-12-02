
def checkForRun(startPosition, playLength, playerHand):
    isMatch = True
    for i in range(startPosition, startPosition + playLength - 1):
        if (isMatch):
            if ((playerHand[i][0] != playerHand[i + 1][0]) or (int(playerHand[i][1:3]) != (int(playerHand[i + 1][1:3]) - 1))):
                isMatch = False 
    
    if (isMatch):
        setToReturn = playerHand[startPosition:(startPosition + playLength)]
    else:
        setToReturn = []

    print("RTR:", setToReturn)

    return(setToReturn)





def checkForSet(startPosition, playLength, playerHand):
    cardToMatch = playerHand[startPosition]
    faceToMatch = cardToMatch[1:3]
    cardsMatched = 1
    setToReturn = [cardToMatch]
    for i in range(startPosition + 1, len(playerHand)):
        if (playerHand[i][1:3] == faceToMatch):
            cardsMatched += 1
            if (cardsMatched <= playLength):
                setToReturn.append(playerHand[i])

    if (cardsMatched < playLength):
        setToReturn = []

    print("STR:",setToReturn)
    
    return(setToReturn)




def findPlays(listOfPlays, playLength):
    isPlaysFound = False

    for i in range(len(listOfPlays["playerHand"]) - playLength + 1):

        playsFound = checkForRun(i, playLength, listOfPlays["playerHand"])
        if (playsFound != []):
            listOfPlays["newPlaysFound"].append(playsFound)
            isPlaysFound = True


        playsFound = checkForSet(i, playLength, listOfPlays["playerHand"])
        if (playsFound != []):
            listOfPlays["newPlaysFound"].append(playsFound)
            isPlaysFound = True

    return(listOfPlays, isPlaysFound)







# identify what plays are possible from the current position
def identifyListOfPlays(listOfPlays):
    print("Under Construction")
 
    playLength = 3
    isPlaysFound = True
    maxPlays = len(listOfPlays["playerHand"])
    if maxPlays == 0:
        isPlaysFound = False

    while(isPlaysFound and (playLength <= maxPlays)):
        listOfPlays, isPlaysFound = findPlays(listOfPlays, playLength)
        playLength += 1

    return(listOfPlays, isPlaysFound)





def checkForMeldSet(handPosition, listOfPlays, setToCheck):
    replacedSet = []
    setToReplace = []
    cardToMeld = []

    cardToMatch = listOfPlays["playerHand"][handPosition]
    faceToMatch = cardToMatch[1:3]

    if (setToCheck[0][1:3] == faceToMatch):
        newSet = copy.deepcopy(setToCheck)
        newSet.append(cardToMatch)
        replacedSet = setToCheck
        setToReplace = newSet
        cardToMeld = cardToMatch
   
    if (cardToMeld != []):
        playToReturn = []
        playToReturn.append([cardToMeld])
        playToReturn.append(setToReplace)
        playToReturn.append(replacedSet)
    else:
        playToReturn = []


    return(playToReturn)





#see if the card can be added to the start or end of a run
def checkForMeldRun(startPosition, listOfPlays, runToCheck):
    print("fixme: add support for aces high or low?")

    replacedRun = []
    runToReplace = []
    cardToMeld = []

    cardToMatch = listOfPlays["playerHand"][startPosition]
    suitToMatch = cardToMatch[0]
    faceToMatch = cardToMatch[1:3]
    # runToCheck = []


    firstCard = 0
    lastCard = len(runToCheck) - 1

    if ((runToCheck[firstCard][0] == suitToMatch) and (int(runToCheck[firstCard][1:3]) == int(faceToMatch) + 1)):
        newRun = [cardToMatch]
        newRun.extend(runToCheck)
        replacedRun = runToCheck
        runToReplace = newRun
        cardToMeld = cardToMatch

    if ((runToCheck[lastCard][0] == suitToMatch) and (int(runToCheck[lastCard][1:3]) == int(faceToMatch)-1)):
        newRun = copy.deepcopy(runToCheck)
        newRun.append(cardToMatch)
        replacedRun = runToCheck
        runToReplace = newRun
        cardToMeld = cardToMatch

    if (cardToMeld != []):
        playToReturn = []
        playToReturn.append([cardToMeld])
        playToReturn.append(runToReplace)
        playToReturn.append(replacedRun)
    else:
        playToReturn = []

    return(playToReturn)





def checkForMelds(handPosition, listOfPlays):
    meldsFound = []

    for playToCheck in listOfPlays["playsFound"]:
        # is it a set? if not it's a run
        if (playToCheck[0][1:3] == playToCheck[1][1:3]):
            meldPlay = checkForMeldSet(handPosition, listOfPlays, playToCheck)
        else:
            meldPlay = checkForMeldRun(handPosition, listOfPlays, playToCheck)
        if (meldPlay != []):
            meldsFound.append(meldPlay)
    return(meldsFound)







def identifyListOfMelds(listOfPlays):
    isMeldsFound = False

    if (len(listOfPlays["playsFound"]) > 0):
        for i in range(len(listOfPlays["playerHand"])):
            playsFound = checkForMelds(i, listOfPlays)
            if (playsFound != [] ):
                for playFound in playsFound:
                    listOfPlays["newPlaysFound"].append(playFound)
                isMeldsFound = True

    return(listOfPlays, isMeldsFound)









def findPlaysInComputerHand(listOfPlays):


    # injected values for testing
    # listOfPlays["playerHand"] = ['C02', 'C10', 'H10', 'D3', 'D10', 'S06', 'S07', 'S08', 'S09', 'S10']
    # listOfPlays["playerHand"] = ['S01', 'S02', 'S03', 'S04', 'S05', 'S06', 'S07', 'S08', 'S09', 'S10']
    # listOfPlays["runs"] = [['C03', 'C04', 'C05'], ['H07', 'H08', 'H09'], ['H02', 'H03', 'H04']]
    # listOfPlays["sets"] = [['D02', 'H02', 'S02'], ['C09', 'H09', 'D09']]


    listOfPlays, isPlaysFound = identifyListOfPlays(listOfPlays)
    listOfPlays, isMeldsFound = identifyListOfMelds(listOfPlays)

    
    return(listOfPlays, (isPlaysFound or isMeldsFound))







def calculateScore(listOfPlays):
    totalScore = 0
    for play in listOfPlays["playsFound"]:
        for card in play:
            cardValue = int(card[1:3])
            totalScore += cardValue
    listOfPlays["bestScoreSoFar"] = totalScore
    return(listOfPlays)



# def removeCardsFromHand(playerHand, cardsToRemove):
#     for groupOfCards in cardsToRemove:
#         for removedCard in groupOfCards:
#             playerHand.remove(removedCard)
#     return(playerHand)





def removeCardsFromHand(playerHand, cardsToRemove):
    for nextCard in cardsToRemove:
            playerHand.remove(nextCard)
    return(playerHand)



def evalNextPlay(possiblePlay, listOfPlays):
    print("evalNextPlay")

    # newListOfPlays = initListOfPlays()
    newListOfPlays = copy.deepcopy(listOfPlays)
    newListOfPlays["newPlaysFound"] = []
    # newListOfPlays["playerHand"] = copy.deepcopy(listOfPlays["playerHand"])
    # newListOfPlays["playsFound"] = copy.deepcopy(listOfPlays["playsFound"])
    # # newListOfPlays["newPlaysFound"] = copy.deepcopy(listOfPlays["newPlaysFound"])
    # newListOfPlays["playsMadeSoFarInBranch"] = copy.deepcopy(listOfPlays["playsMadeSoFarInBranch"])
    listOfPlays = newListOfPlays

    listOfPlays["playsMadeSoFarInBranch"].append(possiblePlay)


    # are we playing a new run or set, or just melding one card

    if (len(possiblePlay[1][0]) == 1):
        listOfPlays["playsFound"].append(possiblePlay)
        listOfPlays["playerHand"] = removeCardsFromHand(listOfPlays["playerHand"], possiblePlay)  
    else:
        meldedCard = possiblePlay[0]
        newRun = possiblePlay[1]
        originalRun = possiblePlay[2]
        listOfPlays["playerHand"].remove(meldedCard[0])
        listOfPlays["playsFound"].remove(originalRun)
        listOfPlays["playsFound"].append(newRun)

    # do we need to go deeper?
    listOfPlays, isPlaysFound = findPlaysInComputerHand(listOfPlays)
    if (isPlaysFound):
        # listOfPlays["playsFound"].append(listOfPlays["newPlaysFound"])
        listOfPlays = initiateNewPlaysIteration(listOfPlays)
    # else:
    #     listOfPlays["playsFound"].append(listOfPlays["newPlaysFound"])

    listOfPlays = calculateScore(listOfPlays)

    return(listOfPlays)














#call playComputerHand() again with each of the possible plays idenified
def initiateNewPlaysIteration(listOfPlays):
    bestListOfPlaysSoFar = initListOfPlays()

    for possiblePlay in listOfPlays["newPlaysFound"]:
        nextListOfPlays = copy.deepcopy(listOfPlays)
        nextListOfPlays = evalNextPlay(possiblePlay, nextListOfPlays)
        if (nextListOfPlays["bestScoreSoFar"] >= bestListOfPlaysSoFar["bestScoreSoFar"]):
            bestListOfPlaysSoFar = nextListOfPlays

    return(bestListOfPlaysSoFar)












def playComputerHand(listOfPlays):
    # bestScoreSoFar=0
    # bestHandSoFar=[]
    # listOfPlays = initListOfPlays()

    print("Under Construction")

    listOfPlays, isPlaysFound = findPlaysInComputerHand(listOfPlays)

    print("POSS:", listOfPlays)

    if (listOfPlays["newPlaysFound"] != []):
        # for newPlayFound in listOfPlays["newPlaysFound"]:
        #     listOfPlays["playsFound"].append(newPlayFound)
        bestHand = initiateNewPlaysIteration(listOfPlays)

        if(bestHand["bestScoreSoFar"] > listOfPlays["bestScoreSoFar"]):
            listOfPlays = copy.deepcopy(bestHand)
    
    return(listOfPlays)






def playComputerHandsFirstStage(gameState):
    print("Under Construction")
    #check if this is needed (i.e is the player going 1st)
    #if needed call the playComputerHand() routine for each player
    computerPlayerNumber = 0 #dummy value for just now

    listOfPlays = initListOfPlays()
    # listOfPlays["runs"] = copy.deepcopy(gameState["runs"][computerPlayerNumber])
    # listOfPlays["sets"] = copy.deepcopy(gameState["sets"][computerPlayerNumber])
    listOfPlays["playsFound"] = copy.deepcopy(gameState["plays"][computerPlayerNumber])
    listOfPlays["playerHand"] = copy.deepcopy(gameState["hands"][computerPlayerNumber])

    playingCard.convertFacesToNumbers(listOfPlays["playerHand"])


    # injected values for testing
    listOfPlays["playerHand"] = ['C02', 'C10', 'H10', 'D03', 'D10', 'S06', 'S07', 'S08', 'S09', 'S10']
    # listOfPlays["playerHand"] = ['S01', 'S02', 'S03', 'S04', 'S05', 'S06', 'S07', 'S08', 'S09', 'S10']
    # listOfPlays["runs"] = [['C03', 'C04', 'C05'], ['H07', 'H08', 'H09'], ['H02', 'H03', 'H04']]
    # listOfPlays["sets"] = [['D02', 'H02', 'S02'], ['C09', 'H09', 'D09']]



    listOfPlays["playerHand"].sort

    listOfPlays = playComputerHand(listOfPlays)

    playingCard.convertNumbersToFaces(listOfPlays["playerHand"])

    print(listOfPlays)

    return(gameState)
