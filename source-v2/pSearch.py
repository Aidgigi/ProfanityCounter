import praw, json, time, collections, stats
import logger as log

reddit=praw.Reddit('probot')

def most_common(lst):
    try:
        return max(set(lst), key=lst.count)

    except ValueError:
        return "None"


def search(auth,mode,mode2):
    timeOnSearch=time.time()
    #opening and defining are badWords json file
    badWordsF=open("badWords.json","r")
    badWords=json.load(badWordsF)
    badWordsF.close()

    #making the blank worksMatchedList
    wordsMatchedList=[]

    #checking if we already have the user's profanity stored
    if stats.testStat(auth) == True and mode2 == 0:
        uOb = stats.fetchStats(auth)["user"]
        badWords = uOb["profanityUsage"]

        favWord = uOb["favoriteWordNP"]

        for key in badWords:
            if badWords[key]!=0:
                wordsMatchedList.append(f"{key}|"+str(badWords[key]))

        #increasing our stat count
        stats.updateStatInc(auth,"calledOn",1)


    if stats.testStat(auth) == False or mode2 == 1:
        #getting our user to check
        user=reddit.redditor(auth)


        #making a list of the user's word usage
        wordsUsed=[]

        for comment in user.comments.new(limit=1000):
            for word in comment.body.split(" "):
                wordsUsed.append(word)

        for post in user.submissions.new(limit=1000):
            for word in post.selftext.split(" "):
                wordsUsed.append(word)
            for word in post.title.split(" "):
                wordsUsed.append(word)

        #deleting all of the null elements
        for word in wordsUsed:
            if word == '':
                wordsUsed.remove(word)

        for word in wordsUsed:
            for key in badWords["badWords"]:
                if word==key:
                    badWords["badWords"][key]=badWords["badWords"][key]+1

        for key in badWords["badWords"]:
            if badWords["badWords"][key]!=0:
                wordsMatchedList.append(f"{key}|"+str(badWords["badWords"][key]))

        favWord = most_common(wordsUsed)

    timeOnComplete=time.time()
    timeTook=int(timeOnComplete-timeOnSearch)
    log.debug(f"Searching for {auth} to: {str(timeTook)} seconds")
    print(f"Searching for {auth} took: {str(timeTook)} seconds")

    #if normal mode, return list with time
    if mode==0:
        return wordsMatchedList, round(timeTook), badWords, favWord

    #if stat mode, return only the dictionairy
    if mode==1:
        return badWords
