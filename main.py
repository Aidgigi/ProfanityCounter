import praw, re, time
from prawcore.exceptions import RequestException, Forbidden, ServerError
from praw.exceptions import APIException, ClientException

#getting our bot info from our ini file
reddit=praw.Reddit('probot')

#making an unread messages loop
unreadMessages=[]

#check if words are truly found in words
def containsWord(s, w):
    return (' ' + w + ' ') in (' ' + s + ' ')



#our logging class
class logclass:

    def debug(self,msg):
        localtime = time.asctime( time.localtime(time.time()) )
        logf.write(f"DEBUG - {msg} - {localtime}\n")

    def error(self,msg):
        localtime = time.asctime( time.localtime(time.time()) )
        logf.write(f"ERROR - {msg} - {localtime}\n")

    def warning(self,msg):
        localtime = time.asctime( time.localtime(time.time()) )
        logf.write(f"WARNING - {msg} - {localtime}\n")

    def critical(self,msg):
        localtime = time.asctime( time.localtime(time.time()) )
        logf.write(f"CRITICAL - {msg} - {localtime}\n")

#creating a logclass instance
log=logclass()

#logging a start message
logf=open("log.txt","a")
log.debug("System Started")
logf.close()

#redditor post iterator function
def badWordCheck(auth):
    #our word usages dictionary
    badWords={"ass":0,"asshole":0,"ass hole":0,"arse":0,"anus":0,"anal":0,"bastard":0,"butthole":0,
    "butt":0,"buthole":0,"booty":0,"black cock":0,"black bitch":0,"black asshole":0,"bloody hell":0,
    "bitch":0,"bitch ass":0,"bitch hoe":0,"cock":0,"cuck":0,"cock sucker":0,"cocksucker":0,"cuck bitch":0,
    "coon":0,"cock fucker":0,"cockfucker":0,"damn":0,"dick":0,"dick sucker":0,"dickfucker":0,
    "dick licker":0,"douche":0,"douche bag":0,"douchebag":0,"erect":0,"erection":0,"errotic":0,
    "faggot":0,"fag":0,"fucker":0,"fucking":0,"fuck":0,"fuck you":0,"fuck off":0,"fuckwhole":0,"god damn":0,
    "god damnit":0,"homo":0,"hore":0,"lesbo":0,"mother fucker":0,
    "mother fuck":0,"motherfucker":0,"negro":0,"nigger":0,"nibba":0,"nigga":0,"negroid":0,"orgasm":0,
    "orgasim":0,"penis":0,"penis licker":0,"penislicker":0,"penis fucker":0,"penisfucker":0,"piss":0,
    "piss off":0,"pussy":0,"porn":0,"porno":0,"pusslicker":0,"pussy licker":0,"retard":0,"retarded":0,
    "raghead":0,"sexy":0,"shit":0,"shut the fuck up":0,"son of a bitch":0,"sex":0,"sadist":0,"tits":0,"tit":0,"towelhead":0,
    "towel head":0,"vagina":0,"whore":0,"weiner":0,"weenor":0}

    #getting our user to check
    user=reddit.redditor(auth)

    #making the blank worksMatchedList
    wordsMatchedList=[]

    #comment checking loop
    for comment in user.comments.new(limit=None):
        for key in badWords:
            if containsWord(comment.body,key):
                badWords[key]=badWords[key]+1

    #post checking loop
    for post in user.submissions.new(limit=None):
        for key in badWords:
            if containsWord(post.selftext,key):
                badWords[key]=badWords[key]+1
            if containsWord(post.title,key):
                badWords[key]=badWords[key]+1

    #making sure only bad words that were used are included in our output string
    for key in badWords:
        if badWords[key]!=0:
            wordsMatchedList.append(f"{key}|{str(badWords[key])}")

    #returning out list that also contains are bad words
    #and number of time that said word was uses
    return wordsMatchedList


#Our string constructer function
def postConstructor(auth,commentor,mode):
    #getting our bad word usage list from the above function
    wordsMatched=badWordCheck(auth)

    #making the regular mode posthttps://duckduckgo.com/
    if mode==0:
        #Constructing our header
        #creating the beginning of our post, as well as the syntax needed to create a table
        commentHeader=f"""UH OH! Someone has been using stinky language and u/{commentor} decided to check u/{auth}\'s bad word usage.\n\n
I have gone back one thousand posts and comments and reviewed their potty language usage.\n\n ^NOTE: ^Using ^me ^under ^the ^same ^comment
 ^or ^parent ^will ^cause ^me ^to ^be ^ratelimited, ^please ^be ^gentle.\n\n"""

        #setting a blank tableComponents var
        tableComponents="|Bad Word|Times Used|\n:--|:-:|"
        #iterating through our wordsMatched list, processing the values and making the added rows
        for badWord in wordsMatched:
            cString="\n|"+badWord.split("|")[0]+"|"+badWord.split("|")[1]
            tableComponents=tableComponents+cString
            #returning the final string that we made

        #special blank comment
        if not wordsMatched:
            tableComponents=f"However, the plans were foiled, {auth} is a good, Christian boy."

    #making the message mode post
    if mode==1:
        #making the header
        commentHeader=f"""Hello u/{commentor}. You tried using me on a sub that I\'ve been banned in, so here is u/{auth}\'s profanity report.
\n\nI have gone back one thousand posts and comments and reviewed their potty language usage.\n\n ^NOTE: ^Using ^me ^under ^the ^same ^comment
 ^or ^parent ^will ^cause ^me ^to ^be ^ratelimited, ^please ^be ^gentle.\n\n"""

        #setting a blank tableComponents varhttps://duckduckgo.com/
        tableComponents="|Bad Word|Times Used|\n:--|:-:|"
        #iterating through our wordsMatched list, processing the values and making the added rows
        for badWord in wordsMatched:
            cString="\n|"+badWord.split("|")[0]+"|"+badWord.split("|")[1]
            tableComponents=tableComponents+cString
            #returning the final string that we made

        #special blank comment
        if not wordsMatched:
            tableComponents=f"Wow! {auth} has never used profanity on Reddit!"

    finalComment=commentHeader+tableComponents

    return finalComment


#our main loop
while True:
    try:
        for item in reddit.inbox.unread():
            #opening our log
            logf=open('log.txt','a')

            #loading our posts analyzed file
            postsFile=open("postsanalyzed.txt","r+")
            pa=str(postsFile.readlines())

            bannedSubs=open("bansublist.txt", "r+")
            bs=str(bannedSubs.readlines())

            #appending our unread messages list
            unreadMessages.append(item)

            #checking for our username
            if "u/profanitycounter" in item.body:
                #making the message into a comment
                comment=reddit.comment(id=item.id)
                if comment.id not in pa:
                    if comment.parent_id.startswith("t1_"):
                        parentcomment=reddit.comment(id=comment.parent_id.split("_")[1])
                        comAuthor=comment.author
                        parentauthor=parentcomment.author

                        #getting and processing our string using the parent comment author
                        print(f"Debug Info: user:{comment.author}; sub:{comment.subreddit}; parent:{comment.parent_id}")
                        log.debug(f"System Used: user:{comment.author}; sub:{comment.subreddit}; parent:{comment.parent_id}")

                        #trying to post our comment
                        try:
                            newComment=comment.reply(postConstructor(str(parentauthor),comment.author,0))
                            print(f"Bot commented at: {comment.parent_id}")
                            log.debug(f"Commented at: {comment.parent_id}")
                            """if comment.parent_id.startswith("t3_"):
                            parentpost=reddit.submission(id=comment.parent_id.split("_")[1])
                            parentauthor=parentpost.author

                            #getting and processing our string using the parent comment author
                            newComment=comment.reply(postConstructor(str(parentauthor),comment.author))
                            print(f"Bot commented at: {comment.parent_id}")"""

                            #getting the parent comment and parent comment author
                            ## TODO:

                            #Writing to our pa file, making sure that each parent comment only recieves one comment
                            postsFile.write(f"{comment.id}\n")

                            reddit.inbox.mark_read(unreadMessages)



                        #catching our 'Forbidden' error, meaning that we've been banned at this sub
                        except Forbidden:
                            print(f"Bot banned at: {comment.subreddit}")
                            log.warning(f"Banned at: {comment.subreddit}")

                            try:
                                #adding this sub to our whitelist
                                if str(comment.subreddit) not in bs:
                                    bannedSubs.write(f"{comment.subreddit}\n")


                                #sending a message to the user who created the error
                                comAuthor.message(f"You used me on r/{comment.subreddit}",postConstructor(str(parentauthor),comment.author,1))

                            except Forbidden:
                                print(f"{comAuthor}\'s account has been suspended, continuing without action.")
                                log.warning(f"{comAuthor} used with a suspended account, continuing")

                            postsFile.write(f"{comment.id}\n")

                            reddit.inbox.mark_read(unreadMessages)

                        log.debug(f"System Executed Successfully")


                        #closing our files used for logging n' shit
                        postsFile.close()
                        bannedSubs.close()
                        logf.close()




    except RequestException:
        print("Connection to the API was dropped - Reconnecting in 30 seconds")
        log.error("Connection to the API was dropped - Reconnecting in 30 seconds")
        time.sleep(30)
        continue

    except APIException:
        print("The bot was ratelimited by the API - Reconnecting")
        log.error("The bot was ratelimited by the API - Reconnecting")
        time.sleep(10)
        continue

    except ServerError:
        print("Error encountered while communicating with the server - Reconnecting in 1 minute")
        log.error("Error encountered while communicating with the server - Reconnecting in 1 minute")
        time.sleep(60)
        continue

    except ClientException:
        log.error("Client Exception encountered - Continuing")
        time.sleep(10)
        continue

    except Forbidden:
        print("Out of loop forbidden error - Continuing")
        log.error("Out of loop forbidden error - Continuing")
        continue

    #sleeping to prevent api dropouts
    time.sleep(10)

    unreadMessages=[]
