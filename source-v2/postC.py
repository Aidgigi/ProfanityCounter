import pSearch

"""
postConstructor() Normal fn:
    Mode 0, is the regular mode for the system. This is ran if the bot isn't banned on the sub, and everything is well.
    Mode 1, ran when the bot is banned on the sub it was ran on. Typically used to message the user
postConstructor2() fn: Used if a user wants to check their own profanity usage
    Mode 0, normal, unbanned
    Mode 1, banned
"""

def postConstructor(auth,commentor,mode):
    #getting our bad word usage list from the above function
    wordsMatched=pSearch.search(auth,0)

    #making the regular mode post
    if mode==0:
        #Constructing our header
        #creating the beginning of our post, as well as the syntax needed to create a table

        if auth=="Aidgigi":
            commentHeader=f"""UH OH! Someone has been using stinky language and u/{commentor} decided to check my master\'s, u/{auth}, bad word usage.\n\n
I have gone back one thousand posts and comments and reviewed their potty language usage.\n\n ^Your ^request ^took ^a ^total ^of ^{wordsMatched[1]}
 ^seconds ^to ^process. ^Please ^be ^courteous ^when ^using ^me, ^share ^with ^others.\n\n"""

        if commentor=="Aidgigi":
            commentHeader=f"""UH OH! Someone has been using stinky language and my master, u/{commentor}, decided to check u/{auth}\'s bad word usage.\n\n
I have gone back one thousand posts and comments and reviewed their potty language usage.\n\n ^Your ^request ^took ^a ^total ^of ^{wordsMatched[1]}
 ^seconds ^to ^process. ^Please ^be ^courteous ^when ^using ^me, ^share ^with ^others.\n\n"""

        else:
            commentHeader=f"""UH OH! Someone has been using stinky language and u/{commentor} decided to check u/{auth}\'s bad word usage.\n\n
I have gone back one thousand posts and comments and reviewed their potty language usage.\n\n ^Your ^request ^took ^a ^total ^of ^{wordsMatched[1]}
 ^seconds ^to ^process. ^Please ^be ^courteous ^when ^using ^me, ^share ^with ^others.\n\n"""

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
\n\nI have gone back one thousand posts and comments and reviewed their potty language usage.\n\n ^Your ^request ^took ^a ^total ^of ^{wordsMatched[1]}
 ^seconds ^to ^process. ^Please ^be ^courteous ^when ^using ^me, ^share ^with ^others.\n\n"""

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
    wordsMatched=pSearch.search(auth,0)

    #making the regular mode post
    if mode==0:
        commentHeader=f"""UH OH! Someone is curious about their profanity usage, and u/{auth} decided to check their's.\n\n
I have gone back one thousand posts and comments and reviewed their potty language usage.\n\n ^Your ^request ^took ^a ^total ^of ^{wordsMatched[1]}
 ^seconds ^to ^process. ^Please ^be ^courteous ^when ^using ^me, ^share ^with ^others.\n\n"""

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
\n\nI have gone back one thousand posts and comments and reviewed your potty language usage.\n\n ^Your ^request ^took ^a ^total ^of ^{wordsMatched[1]}
 ^seconds ^to ^process. ^Please ^be ^courteous ^when ^using ^me, ^share ^with ^others.\n\n"""

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
