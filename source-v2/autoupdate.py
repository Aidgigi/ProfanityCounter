import stats, time
import logger as log

statRecFile = open("statRec.txt","r")
statRec = statRecFile.readlines()
statRecFile.close()


while True:
    print("UPDATING STARTING")
    onStart=time.time()
    for file in statRec:
        auth = file.split(".")[0]
        stats.updateStats(auth)

    print("UPDATING FINISHED")
    onFin=time.time()
    print(f"Updating took: {str(round(onFin - onStart))} seconds")
    time.sleep(43200)
