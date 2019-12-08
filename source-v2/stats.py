import praw, time, os, json, pSearch
import pSearch

reddit = praw.Reddit('probot')
userPath="./users"


def startRec(auth):
    #checking if the user already has a profile in the system
    try:
        test = open(f"./users/{auth}.json", "r")
        return 0

    except FileNotFoundError:
        #opening our user stat template json file
        template = open("statProfileTemplate.json","r")
        templateDict = json.load(template)
        template.close()

        #mutating our template dict and copying it to the user's file
        with open(f"./users/{auth}.json","w+") as userFile:
            #writing the user's name
            templateDict["user"]["name"] = "Aidgigi"

            #adding timestamp that recording was started
            #getting the time
            templateDict["user"]["startRecTime"] = time.time()

            #getting ther user's bad word stats
            badWordDict = pSearch.search(auth,1)["badWords"]

            #adding the user's profanity usage
            templateDict["user"]["profanityUsage"] = badWordDict

            #adding the total profanity count
            templateDict["user"]["profanityTotal"] = sum(badWordDict.values())

            json.dump(templateDict,userFile,indent=2)



def fetchStat(auth):
    print()
