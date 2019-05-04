import config
import requests
import json

def getApiFormatted(config=config):
    return "{config.url}/api?output=json&apikey={config.key}".format(config=config)

def getStatus(config=config):
    response = requests.get('{url}&mode=qstatus'.format(url=getApiFormatted(config=config)))
    return json.loads(response.text).get("value")

def getFreeSpace(config=config):
    return getStatus(config=config).get("diskspace1")

def getNextInQueue(config=config):
    return getStatus(config=config).get("slots")[0]

def getSizeLeftOfNextInQueue(config=config):
    size = str(getNextInQueue(config=config).get("sizeleft"))
    size_float = float(0.0) # this is the size in gigabytes which we want to assign later
    if size.endswith(" KB"):
        size_float = (float(size.strip(" KB"))/1024)/1024
    elif size.endswith(" MB"):
        size_float = float(size.strip(" MB"))/1024
    elif size.endswith(" GB"):
        size_float = float(size.strip(" GB"))
    return size_float

def pause(config=config):
    response = requests.get("{url}&mode=pause".format(url=getApiFormatted(config=config)))

def resume(config=config):
    response = requests.get("{url}&mode=resume".format(url=getApiFormatted(config=config)))

def throttle(percentage, config=config):
    if int(percentage) <= 0:
        pause(config=config)
        return
    elif int(percentage) >= 100:
        percentage = 100.0
    resume(config=config)
    response = requests.get("{url}&mode=config&name=speedlimit&value={perc}".format(url=getApiFormatted(config=config), perc=int(percentage)))
    if json.loads(response.text).get("status"):
        return True
    else:
        print("Something weird happened. Check your SAB logs.")
        return False

def autoScale():
    spaceFree = float(getFreeSpace())
    spaceNeededForNext = getSizeLeftOfNextInQueue()
    spaceAfterNextDownload = spaceFree - spaceNeededForNext # this is to ensure completing the download won't put us over the threshold
    space_gap_max = config.free_space_unthrottled - config.free_space_throttled # this is the max dif between the 100% throttle and 0% throttle
    space_gap_cur = spaceAfterNextDownload - config.free_space_throttled # dif between 100% and the current + space needed for the next file
    percentage = 100 - (((space_gap_max-space_gap_cur) / space_gap_max) * 100) # calculate the percentage we need to set the throttle by how much of the throttled buffer is being used
    if percentage <= 0:
        throttle(percentage)
    space_gap_cur = spaceFree - config.free_space_throttled # dif between 100% and the current
    percentage = 100 - (((space_gap_max-space_gap_cur) / space_gap_max) * 100) # calculate the percentage again now we know it's all good to continue
    throttle(percentage)

    
if __name__ == "__main__":
    if config.loop:
        while True:
            autoScale()
    else:
        autoScale()