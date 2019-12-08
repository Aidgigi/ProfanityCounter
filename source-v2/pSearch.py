import praw, json, time, collections
import logger as log

reddit=praw.Reddit('probot')


def search(auth,mode):
    timeOnSearch=time.time()
    #opening and defining are badWords json file
    badWordsF=open("badWords.json","r")
    badWords=json.load(badWordsF)
    badWordsF.close()

    #getting our user to check
    user=reddit.redditor(auth)

    #making the blank worksMatchedList
    wordsMatchedList=[]

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


    for word in wordsUsed:
        for key in badWords["badWords"]:
            if word==key:
                badWords["badWords"][key]=badWords["badWords"][key]+1

    for key in badWords["badWords"]:
        if badWords["badWords"][key]!=0:
            wordsMatchedList.append(f"{key}|"+str(badWords["badWords"][key]))

    timeOnComplete=time.time()
    timeTook=str(timeOnComplete-timeOnSearch)
    log.debug(f"Searching for {auth} to: {timeTook} seconds")
    print(f"Searching for {auth} took: {timeTook} seconds")

    #if normal mode, return list with time
    if mode==0:
        return wordsMatchedList, timeTook.split(".")[0]

    #if stat mode, return only the dictionairy
    if mode==1:
        return badWords

    #returns plain dict, along with time
    if mode==2:
        return badWords, timeTook.split(".")[0]
