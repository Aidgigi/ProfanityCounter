import praw, re, time, postC
import logger as log
from prawcore.exceptions import RequestException, Forbidden, ServerError
from praw.exceptions import APIException, ClientException

reddit=praw.Reddit('probot')

#making an unread messages loop
unreadMessages=[]

def mainFn():
    global unreadMessages
    try:
        for item in reddit.inbox.unread():

            #loading our posts analyzed file
            postsFile=open("postsanalyzed.txt","r+")
            pa=str(postsFile.readlines())

            #loading the banned subs file
            bannedSubs=open("bansublist.txt", "r+")
            bs=str(bannedSubs.readlines())

            #appending our unread messages list
            unreadMessages.append(item)
            reddit.inbox.mark_read(unreadMessages)


            #checking the message for a bot mention
            if "u/profanitycounter2" in item.body:
                #making the message into a comment
                comment=reddit.comment(id=item.id)
                if comment.id not in pa:

                    #starting a user stats record
                    if "[startstats]" in item.body.lower():
                        # TODO: make starting the stats work
                        print(0)

                    #retrieved a user's stat record
                    if "[stats]" in item.body.lower():
                        ## TODO: code the entire stats system
                        print(0)

                    #to allow a user to check one own's profanity usage
                    if "[self]" in item.body.lower():
                        comAuthor=comment.author

                        if str(comment.subreddit) not in bs:
                            #getting and processing our string using the parent comment author
                            print(f"Debug Info: user:{comment.author}; sub:{comment.subreddit}; parent:{comment.parent_id}")
                            log.debug(f"System Used: user:{comment.author}; sub:{comment.subreddit}; parent:{comment.parent_id}")

                            #trying to post normally
                            try:
                                newComment=comment.reply(postC.postConstructor2(str(comment.author),0))
                                print(f"Bot commented at: {comment.parent_id}")
                                log.debug(f"Commented at: {comment.parent_id}")

                            #catching our 'Forbidden' error, meaning that we've been banned at this sub
                            except Forbidden:
                                print(f"Bot now banned at: {comment.subreddit}")
                                log.warning(f"Banned now at: {comment.subreddit}")

                                try:
                                    #sending a message to the user who created the error
                                    comAuthor.message(f"You used me on r/{comment.subreddit}",postC.postConstructor2(str(parentauthor),comment.author,1))

                                except Forbidden:
                                    print(f"{comAuthor}\'s account has been suspended, continuing without action.")
                                    log.warning(f"{comAuthor} used with a suspended account, continuing")

                            if str(comment.subreddit) in bs:
                                print(f"Bot run on know banned sub: {comment.subreddit}. PMing user.")
                                log.debug(f"Bot used on KBS: {comment.subreddit}")

                                try:
                                    comAuthor.message(f"You used me on r/{comment.subreddit}",postC.postConstructor2(str(parentauthor),comment.author,1))
                                    print(f"User {comment.author} was successfully PMed")
                                    log.debug(f"User {comment.author} was successfully PMed")

                                except Forbidden:
                                    print(f"{comAuthor}\'s account has been suspended, continuing without action.")
                                    log.warning(f"{comAuthor} used with a suspended account, continuing")


                    #plain profanity checking
                    else:
                        #checking if our parent is a comment or post, and then proceeding
                        #parent is comment
                        if comment.parent_id.startswith("t1_"):
                            #getting some info about the parent
                            parentcomment=reddit.comment(id=comment.parent_id.split("_")[1])
                            comAuthor=comment.author
                            parentauthor=parentcomment.author


                            #checking if the bot is being used in a free sub
                            if str(parentcomment.subreddit) not in bs:

                                #getting and processing our string using the parent comment author
                                print(f"Debug Info: user:{comment.author}; sub:{comment.subreddit}; parent:{comment.parent_id}")
                                log.debug(f"System Used: user:{comment.author}; sub:{comment.subreddit}; parent:{comment.parent_id}")

                                #trying to post our comment
                                try:
                                    newComment=comment.reply(postC.postConstructor(str(parentauthor),comment.author,0))
                                    print(f"Bot commented at: {comment.parent_id}")
                                    log.debug(f"Commented at: {comment.parent_id}")


                                #catching our 'Forbidden' error, meaning that we've been banned at this sub
                                except Forbidden:
                                    print(f"Bot now banned at: {comment.subreddit}")
                                    log.warning(f"Banned now at: {comment.subreddit}")

                                    try:
                                        #sending a message to the user who created the error
                                        comAuthor.message(f"You used me on r/{comment.subreddit}",postC.postConstructor(str(parentauthor),comment.author,1))

                                    except Forbidden:
                                        print(f"{comAuthor}\'s account has been suspended, continuing without action.")
                                        log.warning(f"{comAuthor} used with a suspended account, continuing")


                            if str(parentcomment.subreddit) in bs:
                                print(f"Bot run on know banned sub: {comment.subreddit}. PMing user.")
                                log.debug(f"Bot used on KBS: {comment.subreddit}")

                                try:
                                    comAuthor.message(f"You used me on r/{comment.subreddit}",postC.postConstructor(str(parentauthor),comment.author,1))
                                    print(f"User {comment.author} was successfully PMed")
                                    log.debug(f"User {comment.author} was successfully PMed")

                                except Forbidden:
                                    print(f"{comAuthor}\'s account has been suspended, continuing without action.")
                                    log.warning(f"{comAuthor} used with a suspended account, continuing")



                        #parent is post
                        if comment.parent_id.startswith("t3_"):
                            #getting info on the parent post
                            parentPost=reddit.submission(id=comment.parent_id.split("_")[1])
                            comAuthor=comment.author
                            parentauthor=parentPost.author

                            if str(parentPost.subreddit) not in bs:
                                #getting and processing our string using the parent comment author
                                print(f"Debug Info: user:{comment.author}; sub:{comment.subreddit}; parent:{comment.parent_id}")
                                log.debug(f"System Used: user:{comment.author}; sub:{comment.subreddit}; parent:{comment.parent_id}")

                                #trying to post our comment
                                try:
                                    newComment=comment.reply(postC.postConstructor(str(parentauthor),comment.author,0))
                                    print(f"Bot commented at: {comment.parent_id}")
                                    log.debug(f"Commented at: {comment.parent_id}")


                                #catching our 'Forbidden' error, meaning that we've been banned at this sub
                                except Forbidden:
                                    print(f"Bot now banned at: {comment.subreddit}")
                                    log.warning(f"Banned now at: {comment.subreddit}")

                                    try:
                                        #sending a message to the user who created the error
                                        comAuthor.message(f"You used me on r/{comment.subreddit}",postC.postConstructor(str(comment.author),1))

                                    except Forbidden:
                                        print(f"{comAuthor}\'s account has been suspended, continuing without action.")
                                        log.warning(f"{comAuthor} used with a suspended account, continuing")


                            #bot is banned
                            if str(parentPost.subreddit) in bs:
                                print(f"Bot run on know banned sub: {comment.subreddit}. PMing user.")
                                log.debug(f"Bot used on KBS: {comment.subreddit}")

                                try:
                                    comAuthor.message(f"You used me on r/{comment.subreddit}",postC.postConstructor(str(comment.author),1))
                                    print(f"User {comment.author} was successfully PMed")
                                    log.debug(f"User {comment.author} was successfully PMed")

                                except Forbidden:
                                    print(f"{comAuthor}\'s account has been suspended, continuing without action.")
                                    log.warning(f"{comAuthor} used with a suspended account, continuing")







                postsFile.write(f"{comment.id}\n")

                log.debug("System executed successfully.")

    except RequestException:
        print("Connection to the API was dropped - Reconnecting in 30 seconds")
        log.error("Connection to the API was dropped - Reconnecting in 30 seconds")
        time.sleep(30)

    except APIException:
        print("The bot was ratelimited by the API - Reconnecting")
        log.error("The bot was ratelimited by the API - Reconnecting")
        time.sleep(10)

    except ServerError:
        print("Error encountered while communicating with the server - Reconnecting in 1 minute")
        log.error("Error encountered while communicating with the server - Reconnecting in 1 minute")
        time.sleep(60)

    except ClientException:
        log.error("Client Exception encountered - Continuing")
        time.sleep(10)

    except Forbidden:
        print("Out of loop forbidden error - Continuing")
        log.error("Out of loop forbidden error - Continuing")

    #sleeping to prevent api dropouts
    time.sleep(5)

    unreadMessages=[]

while True:
    mainFn()
