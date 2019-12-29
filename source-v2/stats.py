import praw, time, os, json, pSearch, operator
import pSearch

reddit = praw.Reddit('probot')


#this function will see if a user is registered in the stat system, and return
#some system readable information
def testStat(auth):
    #user is in the system
    try:
        test = open(f"./users/{auth}.json", "r")
        return True

    #user is not in the system
    except FileNotFoundError:
        return False


def startRec(auth):
    #checking if the user already has a profile in the system
    if testStat(auth)==False:
        #opening our user stat template json file
        template = open("statProfileTemplate.json","r")
        statRecFile = open("statRec.txt","a")
        templateDict = json.load(template)
        template.close()

        #mutating our template dict and copying it to the user's file
        with open(f"./users/{auth}.json","w+") as userFile:
            #writing the user's name
            templateDict["user"]["name"] = str(auth)

            #adding timestamp that recording was started
            #getting the time
            templateDict["user"]["startRecTime"] = round(time.time())

            #getting ther user's bad word stats
            badWordObject = pSearch.search(str(auth),0,1)
            badWordDict = badWordObject[2]["badWords"]

            #updating the time took var
            templateDict["user"]["sysTimeUsed"] = int(badWordObject[1])

            templateDict["user"]["favoriteWord"] = max(badWordDict.items(), key=operator.itemgetter(1))[0]
            #checking if the users favorite bad word isn't really their favorite
            if badWordDict[templateDict["user"]["favoriteWord"]] == 0: templateDict["user"]["favoriteWord"] = "None"

            templateDict["user"]["favoriteWordNP"] = badWordObject[3]

            #adding the user's profanity usage
            templateDict["user"]["profanityUsage"] = badWordDict

            #adding the total profanity count
            templateDict["user"]["profanityTotal"] = sum(badWordDict.values())

            #writing the file to the stat record
            statRecFile.write(f"{auth}.json\n")
            statRecFile.close()

            #dumping the dictionairy to the file
            json.dump(templateDict,userFile,indent=2)

    else:
        return 0


#this function will update a user statistics
def updateStats(auth):
    if testStat(auth) == True:
        #opening our user file and loading it
        userFile = open(f"./users/{auth}.json","r")
        userDict = json.load(userFile)
        userFile.close()

        #getting ther user's bad word stats
        badWordObject = pSearch.search(str(auth),0,1)
        badWordDict = badWordObject[2]["badWords"]

        #updating the time took var
        userDict["user"]["sysTimeUsed"] = int(userDict["user"]["sysTimeUsed"]+int(badWordObject[1]))

        userDict["user"]["favoriteWord"] = max(badWordDict.items(), key=operator.itemgetter(1))[0]
        if badWordDict[userDict["user"]["favoriteWord"]] == 0: userDict["user"]["favoriteWord"] = "None"

        userDict["user"]["favoriteWordNP"] = badWordObject[3]

        #adding the user's profanity usage
        userDict["user"]["profanityUsage"] = badWordDict

        #adding the total profanity count
        userDict["user"]["profanityTotal"] = sum(badWordDict.values())

        #opening the file in write mode
        userFile = open(f"./users/{auth}.json","w+")

        #dumping the dictionairy to the file
        json.dump(userDict,userFile,indent=2)

        userFile.close()

    else:
        return False

def updateStatInc(auth,stat,val):
    #opening our user file and loading it
    userFile = open(f"./users/{auth}.json","r")
    userDict = json.load(userFile)
    userFile.close()
    userFile = open(f"./users/{auth}.json","w+")

    userDict["user"][stat] = userDict["user"][stat] + val

    #dumping the dictionairy to the file
    json.dump(userDict,userFile,indent=2)

    userFile.close()


def fetchStats(auth):
    if testStat(auth) == True:
        userFile = open(f"./users/{auth}.json","r")
        return json.load(userFile)
        userFile.close()
