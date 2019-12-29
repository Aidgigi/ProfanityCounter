import pSearch, stats
from datetime import datetime

"""
postConstructor() Normal fn:
    Mode 0, is the regular mode for the system. This is ran if the bot isn't banned on the sub, and everything is well.
    Mode 1, ran when the bot is banned on the sub it was ran on. Typically used to message the user
postConstructor2() fn: Used if a user wants to check their own profanity usage
    Mode 0, normal, unbanned
    Mode 1, banned
postConstructor3() fn: used for constructing responses related to the stats system
    Mode 0, startRec sucessful
    Mode 1, startRec unsucessful, already registered
"""

def postConstructor(auth,commentor,mode):
    #getting our bad word usage list from the above function
    wordsMatched=pSearch.search(auth,0,0)

    #making the regular mode post
    if mode==0:
        #Constructing our header
        #creating the beginning of our post, as well as the syntax needed to create a table

        if auth=="Aidgigi":
            commentHeader=f"""UH OH! Someone has been using stinky language and u/{commentor} decided to check my master\'s, u/{auth}, bad word usage.\n\n
I have gone back one thousand posts and comments and reviewed their potty language usage.\n\n ^Request ^time: ^{wordsMatched[1]}. ^This ^is ^profanitycounter ^version ^2, ^view ^update ^notes [^here. ](https://www.reddit.com/r/profanitycounter/comments/e9zvta/introducing_version_20_gone_sexual/)\n\n"""

        if commentor=="Aidgigi":
            commentHeader=f"""UH OH! Someone has been using stinky language and my master, u/{commentor}, decided to check u/{auth}\'s bad word usage.\n\n
I have gone back one thousand posts and comments and reviewed their potty language usage.\n\n ^Request ^time: ^{wordsMatched[1]}. ^This ^is ^profanitycounter ^version ^2, ^view ^update ^notes [^here. ](https://www.reddit.com/r/profanitycounter/comments/e9zvta/introducing_version_20_gone_sexual/)\n\n"""

        else:
            commentHeader=f"""UH OH! Someone has been using stinky language and u/{commentor} decided to check u/{auth}\'s bad word usage.\n\n
I have gone back one thousand posts and comments and reviewed their potty language usage.\n\n ^Request ^time: ^{wordsMatched[1]}. ^This ^is ^profanitycounter ^version ^2, ^view ^update ^notes [^here. ](https://www.reddit.com/r/profanitycounter/comments/e9zvta/introducing_version_20_gone_sexual/)\n\n"""

        #setting a blank tableComponents var
        tableComponents="|Bad Word|Times Used|\n:--|:-:|"
        #iterating through our wordsMatched list, processing the values and making the added rows
        for badWord in wordsMatched[0]:
            cString="\n|"+badWord
            tableComponents=tableComponents+cString
            #returning the final string that we made

        #special blank comment
        if not wordsMatched[0]:
            tableComponents=f"However, the plans were foiled, {auth} is a good, Christian boy."

    #making the message mode post
    if mode==1:
        #making the header
        commentHeader=f"""Hello u/{commentor}. You tried using me on a sub that I\'ve been banned in, so here is u/{auth}\'s profanity report.
\n\nI have gone back one thousand posts and comments and reviewed their potty language usage.\n\n ^Request ^time: ^{wordsMatched[1]}. ^This ^is ^profanitycounter ^version ^2, ^view ^update ^notes [^here. ](https://www.reddit.com/r/profanitycounter/comments/e9zvta/introducing_version_20_gone_sexual/)\n\n"""

        #setting a blank tableComponents var
        tableComponents="|Bad Word|Times Used|\n:--|:-:|"
        #iterating through our wordsMatched list, processing the values and making the added rows
        for badWord in wordsMatched[0]:
            cString="\n|"+badWord
            tableComponents=tableComponents+cString
            #returning the final string that we made

        #special blank comment
        if not wordsMatched[0]:
            tableComponents=f"Wow! {auth} has never used profanity on Reddit!"


    finalComment=commentHeader+tableComponents

    return finalComment


#our self check post constructor
def postConstructor2(auth,mode):
    #getting our bad word usage list from the above function
    wordsMatched=pSearch.search(auth,0,0)

    #making the regular mode post
    if mode==0:
        commentHeader=f"""UH OH! Someone is curious about their profanity usage, and u/{auth} decided to check their's.\n\n
I have gone back one thousand posts and comments and reviewed their potty language usage.\n\n ^Request ^time: ^{wordsMatched[1]}. ^This ^is ^profanitycounter ^version ^2, ^view ^update ^notes [^here. ](https://www.reddit.com/r/profanitycounter/comments/e9zvta/introducing_version_20_gone_sexual/)\n\n"""

        #setting a blank tableComponents var
        tableComponents="|Bad Word|Times Used|\n:--|:-:|"
        #iterating through our wordsMatched list, processing the values and making the added rows
        for badWord in wordsMatched[0]:
            cString="\n|"+badWord
            tableComponents=tableComponents+cString
            #returning the final string that we made

        #special blank comment
        if not wordsMatched[0]:
            tableComponents=f"However, the plans were foiled, {auth} is a good, Christian boy."

    if mode==1:
        commentHeader=f"""Hello u/{commentor}. You tried using me on a sub that I\'ve been banned in, so here is your profanity report.
\n\nI have gone back one thousand posts and comments and reviewed your potty language usage.\n\n ^Request ^time: ^{wordsMatched[1]}. ^This ^is ^profanitycounter ^version ^2, ^view ^update ^notes [^here. ](https://www.reddit.com/r/profanitycounter/comments/e9zvta/introducing_version_20_gone_sexual/)\n\n"""

        #setting a blank tableComponents var
        tableComponents="|Bad Word|Times Used|\n:--|:-:|"
        #iterating through our wordsMatched list, processing the values and making the added rows
        for badWord in wordsMatched[0]:
            cString="\n|"+badWord
            tableComponents=tableComponents+cString
            #returning the final string that we made

        #special blank comment
        if not wordsMatched[0]:
            tableComponents=f"Wow! You have never used profanity on Reddit!"

    finalComment=commentHeader+tableComponents

    return finalComment


#used for constructing posts related to the the stat system
def postConstructor3(auth,mode):

    if mode==0:
        return f"""Thanks u/{auth}, you are now successfully registered in the profanitycounter stats system. I will now keep track of your usage quota, your total profanity count, and more. You can check your stats by adding `[stats]` when tagging me."""

    if mode==1:
        return f"""Sorry u/{auth}, but you are already registered in the profanitycounter stats system. You can check your stats by tagging me along with `[stats]` in the comment."""

def postConstructor4(auth,mode):
    if mode==0:
        userInfo = stats.fetchStats(auth)["user"]
        del userInfo['name']
        del userInfo['profanityUsage']


        #constructing the comment/message header
        commentHeader = f"""Hello u/{auth}, thank you for checking your stats! Below you can find your full statistical report.\n\n ^Your ^stats, ^along ^with ^your ^profanity ^report ^are ^being ^updated ^daily. [^DM ^my ^master ](https://www.reddit.com/message/compose/?to=Aidgigi&subject=Requesting removal from profanitycounter stat system&message=I, u/{auth}, would like to be removed from the u/profanitycounter statistics system.) ^to ^be ^removed ^from ^the ^system.\n\n"""

        tableComponents = "|Statistic|Data|\n:--|:-:|"
        cString = "\n|Favorite bad word|" + userInfo["favoriteWord"]
        cString = cString + "\n|Favorite word|" +userInfo["favoriteWordNP"]
        cString = cString + "\n|Total profanity usage|" + str(userInfo["profanityTotal"])
        cString = cString + "\n|Recording since|" +  datetime.utcfromtimestamp(userInfo["startRecTime"]).strftime('%m-%d-%Y')
        cString = cString + "\n|Used the bot|" + str(userInfo["called"])
        cString = cString + "\n|Bot used on|" + str(userInfo["calledOn"])
        cString = cString + "\n|System time used|" + str(round(int(userInfo["sysTimeUsed"])/60,2)) + " minutes"


        return commentHeader + tableComponents + cString

    if mode == 1:
        return f"""Sorry u/{auth}, but you're not registered in the profanitycounter stats system. Please do so in order to check your stats.\n\n^This ^is ^profanitycounter ^version ^2, ^view ^update ^notes [^here. ](https://www.reddit.com/r/profanitycounter/comments/e9zvta/introducing_version_20_gone_sexual/)"""
