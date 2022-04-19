from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from PIL import Image
import random
import time
import warnings
import urllib.request
import csv

#ignore depreciation warnings from selenium
warnings.filterwarnings("ignore", category=DeprecationWarning)

ff = None

def login():
    global ff, username, password
    username = "thegordproject"
    password = "G0rd1234"
    ff = webdriver.Firefox()
    ff.get("https://www.instagram.com/")
    while True:
        try:
            usernameForm = ff.find_element(By.NAME, "username").send_keys(username)
            passwordForm = ff.find_element(By.NAME, "password").send_keys(password + Keys.ENTER)
            break
        except:
            time.sleep(1)
    while True:
        try:
            ff.find_element_by_xpath("//button[text()='Not Now']").click()
            time.sleep(1)
            try:
                ff.find_element_by_xpath("//button[text()='Not Now']").click()
                time.sleep(1)
            except:
                time.sleep(1)
            break
        except:
            time.sleep(1)

def watermark(source):
    baseImage = Image.open(source)
    baseWidth, baseHeight = baseImage.size

    #picks random gordhead image out of 4
    wmPath = "C:\Gord\Images\GordHead" + str(random.randint(1,4)) + ".png"
    wm = Image.open(wmPath)

    #picks randoms size for gordhead, and resizez wm accordingly
    sizes = random.randint(1,4)
    sizeFactor = 1
    if sizes == 1:
        sizeFactor = 0.65
    elif sizes == 2:
        sizeFactor = 0.55
    elif sizes == 3:
        sizeFactor = 0.4
    elif sizes == 4:
        sizeFactor = 0.33
    size = int(baseHeight*sizeFactor), int(baseHeight*sizeFactor)
    wm = wm.resize(size)
    wmWidth, wmHeight = wm.size

    #picks a side (1 or 2) for gord to be pasted
    side = random.randint(1,2)
    if side == 1:
        position = (0, baseHeight-wmHeight)
    else:
        position = (baseWidth-wmWidth, baseHeight-wmHeight)

    #pasts the background and gords head on to a black image and returns
    output = Image.new('RGBA', (baseWidth, baseHeight), (0,0,0,0))
    output.paste(baseImage, (0,0))
    output.paste(wm, position, mask = wm)
    return(output)

def getNewImages():
    print("GET NEW IMAGES CALLED")
    global ff
    imgSources = []
    users = []
    postNumbers = []

    #Goes to random hashtag
    hashtags = ['landscape', 'landscapephotography', 'mountains', 'travelphotography', 'photography', 'landscapes', 'nature', 'naturephotography']
    searchUrl = "https://www.instagram.com/explore/tags/" + hashtags[random.randint(0,len(hashtags)-1)]+ "/"
    ff.get(searchUrl)

    #Opens first picture
    while True:
        try:
            element = ff.find_element(By.CLASS_NAME, "FFVAD")
            break
        except:
            time.sleep(1)
    ff.execute_script("arguments[0].click();", element)

    #for the first 9 (top posts)
    for i in range(1,10):
        while True:
            try:
                #get usnerame
                user = ff.find_element_by_xpath("/html/body/div[6]/div[3]/div/article/div/div[2]/div/div/div[1]/div/header/div[2]/div[1]/div[1]/div/span/a").get_attribute('href')
                break
            except:
                time.sleep(1)
        #get postnumber
        postNumber = ff.current_url
        user = user[26:-1]
        postNumber = postNumber[28:-1]
        users.append(user)
        postNumbers.append(postNumber)
        #click the next button
        while True:
            try:
                if i == 1:
                    ff.find_element_by_xpath("/html/body/div[6]/div[2]/div/div/button").click()
                else:
                    ff.find_element_by_xpath("/html/body/div[6]/div[2]/div/div[2]/button").click()
                break
            except:
                time.sleep(1)

    #click x button
    ff.find_element_by_xpath("/html/body/div[6]/div[1]/button").click()

    #get image sources
    imgSources.append(ff.find_element_by_xpath("/html/body/div[1]/section/main/article/div[1]/div/div/div[1]/div[1]/a/div/div[1]/img").get_attribute('src'))
    imgSources.append(ff.find_element_by_xpath("/html/body/div[1]/section/main/article/div[1]/div/div/div[1]/div[2]/a/div/div[1]/img").get_attribute('src'))
    imgSources.append(ff.find_element_by_xpath("/html/body/div[1]/section/main/article/div[1]/div/div/div[1]/div[3]/a/div/div[1]/img").get_attribute('src'))
    imgSources.append(ff.find_element_by_xpath("/html/body/div[1]/section/main/article/div[1]/div/div/div[2]/div[1]/a/div/div[1]/img").get_attribute('src'))
    imgSources.append(ff.find_element_by_xpath("/html/body/div[1]/section/main/article/div[1]/div/div/div[2]/div[2]/a/div/div[1]/img").get_attribute('src'))
    imgSources.append(ff.find_element_by_xpath("/html/body/div[1]/section/main/article/div[1]/div/div/div[2]/div[3]/a/div/div[1]/img").get_attribute('src'))
    imgSources.append(ff.find_element_by_xpath("/html/body/div[1]/section/main/article/div[1]/div/div/div[3]/div[1]/a/div/div[1]/img").get_attribute('src'))
    imgSources.append(ff.find_element_by_xpath("/html/body/div[1]/section/main/article/div[1]/div/div/div[3]/div[2]/a/div/div[1]/img").get_attribute('src'))
    imgSources.append(ff.find_element_by_xpath("/html/body/div[1]/section/main/article/div[1]/div/div/div[3]/div[3]/a/div/div[1]/img").get_attribute('src'))

    #for each post
    for i in range(0,9):
        #check if image has been dowloaded before
        new = True
        with open("C:\Gord\memory.csv", 'r+') as memory:
            csvReader = csv.reader(memory)
            for row in csvReader:
                if postNumbers[i] == row[0]:
                    new = False
        if new:
            #download image
            originalPath = "C:\Gord\Images\Originals\\" + postNumbers[i] + ".jpg"
            urllib.request.urlretrieve(imgSources[i], originalPath)
            #watermark image
            watermarkedImage = watermark(originalPath)
            watermarkedImage.save("C:\Gord\Images\Watermarked\\" + postNumbers[i] + ".png")
            #add to csvfile
            newLine = [postNumbers[i], users[i], '1', '0']
            print(newLine)
            with open("C:\Gord\memory.csv", 'a', newline='') as memory:
                csvWriter = csv.writer(memory)
                csvWriter.writerow(newLine)

def captionGenerator(tag):
    def pickRandom(bank, q=1):
        hashtagBank = ["#nature ", "#landscape ", "#wilderness ", "#love ", "#instagood ", "#fashion ", "#photooftheday ", "#beautiful ", "#art ", "#photography ", "#happy ", "#picoftheday ", "#cute ", "#follow ", "#tbt ", "#followme ", "#nature ", "#like4like ", "#travel ", "#instagram ", "#style ", "#repost ", "#summer ", "#instadaily ", "#selfie ", "#me ", "#friends ", "#fitness ", "#girl ", "#food ", "#fun ", "#beauty ", "#instalike ", "#smile ", "#family ", "#like ", "#likeforlike ", "#music ", "#ootd ", "Gord", "King", "#follow4follow ", "#makeup ", "#amazing ", "#igers ", "#nofilter ", "#dog ", "#model ", "#beach ", "#instamood ", "#foodporn ", "#motivation ", "#followforfollow ", "#gordo ", "#beans ", "#fortheboys ", "#cool ", "#swag ", "#420 ", "#69 "]
        #positive adjective bank
        paBank = ["good", "great", "amazing", "awesome", "stellar", "fantastic", "cool", "excellent", "wicked", "legit", "awe-inspiring", "sweet"]
        salutationBank = ["Hello! ", "Hi! ", "Salut! ", "Bonjour! ", "Good Morning! ", "Hello! ", "What's up!? ", "Suuuup! ", "Howdy! ", "Hola! ", "Good Evening! ", "Yo! ", ]
        contentBank = ["It's me, Gord! ", "Hope you're having a great day. ", "Please enjoy this post. "]

        output = ""
        for i in range(0, q):
            if bank == "hashtag":
                output += hashtagBank[random.randint(0, len(hashtagBank)-1)]
            elif bank == "pa":
                output += paBank[random.randint(0, len(paBank)-1)]
            elif bank == "salutation":
                output += salutationBank[random.randint(0, len(salutationBank)-1)]
            elif bank == "content":
                output += contentBank[random.randint(0, len(contentBank)-1)]
        return output


    caption = pickRandom("salutation") + pickRandom("content") + "\n" + "\n" + "#TheGordProject " + pickRandom("hashtag", 18)
    caption += "\n" + "\n" + "@" + tag
    return(caption)

def post():
    #check if there are downloaded images ready to post
    readyToPost = False
    imageToPost = ""
    usernameOf = ""
    while readyToPost == False:
        with open("C:\Gord\memory.csv", 'r') as memory:
            csvReader = csv.reader(memory)
            for row in csvReader:
                if row[2] == '1' and row[3] == '0':
                    imageToPost = row[0]
                    usernameOf = row[1]
                    print(imageToPost)
                    print(readyToPost)
                    readyToPost = True
                    break
    #if there's no images ready to post(to break the loop) GET NEW IMAGES
        if readyToPost == False:
            getNewImages()

    imageToPostSrc = "C:\Gord\Images\Watermarked\\" + imageToPost + ".png"

    #click new post button
    while True:
        try:
            ff.find_element_by_xpath('/html/body/div[1]/section/nav/div[2]/div/div/div[3]/div/div[3]/div/button').click()
            break
        except:
            time.sleep(1)
    #upload image
    while True:
        try:
            ff.find_element_by_xpath("/html/body/div[8]/div[2]/div/div/div/div[2]/div[1]/form/input").send_keys(imageToPostSrc)
            break
        except:
            time.sleep(1)

    #select original crop
    while True:
        try:
            ff.find_element_by_xpath("/html/body/div[6]/div[2]/div/div/div/div[2]/div[1]/div/div/div/div[1]/div/div[2]/div/button").click()
            break
        except:
            time.sleep(1)
    while True:
        try:
            ff.find_element_by_xpath("/html/body/div[6]/div[2]/div/div/div/div[2]/div[1]/div/div/div/div[1]/div/div[1]/div/button[1]").click()
            break
        except:
            time.sleep(1)

    #next (crop)
    while True:
        try:
            ff.find_element_by_xpath("/html/body/div[6]/div[2]/div/div/div/div[1]/div/div/div[3]/div/button").click()
            break
        except:
            time.sleep(1)
    #next (edit)
    while True:
        try:
            ff.find_element_by_xpath("/html/body/div[6]/div[2]/div/div/div/div[1]/div/div/div[3]/div/button").click()
            break
        except:
            time.sleep(1)
    #generate caption, input caption
    caption = captionGenerator(usernameOf)
    while True:
        try:
            ff.find_element_by_xpath("/html/body/div[6]/div[2]/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/textarea").send_keys(caption)
            time.sleep(1)
            break
        except:
            time.sleep(1)
    #click share
    while True:
        try:
            ff.find_element_by_xpath("/html/body/div[6]/div[2]/div/div/div/div[1]/div/div/div[3]/div/button").click()
            break
        except:
            time.sleep(1)

    #wait for confirmation text before closing
    while True:
        try:
            confirmation = ff.find_element_by_xpath("//h2[text()='Your post has been shared.']")
            ff.find_element_by_xpath("/html/body/div[6]/div[1]/button").click()
            break
        except:
            time.sleep(1)
    #mark as posted?????
    with open("C:\Gord\memory.csv", 'r') as memory:
        memoryList = list(csv.reader(memory))
        for row in memoryList:
            if row[0] == imageToPost:
                row[3] = '1'

    with open("C:\Gord\memory.csv", 'w',  newline='') as memory:
        memoryWriter = csv.writer(memory)
        memoryWriter.writerows(memoryList)

def testing():
    #click new post button
    while True:
        try:
            ff.find_element_by_xpath('/html/body/div[1]/section/nav/div[2]/div/div/div[3]/div/div[3]/div/button').click()
            break
        except:
            time.sleep(1)
    #upload image
    while True:
        try:
            ff.find_element_by_xpath("/html/body/div[8]/div[2]/div/div/div/div[2]/div[1]/form/input").send_keys("C:\Gord\Images\gord1.jpg")
            break
        except:
            time.sleep(1)

    #select original crop
    while True:
        try:
            ff.find_element_by_xpath("/html/body/div[6]/div[2]/div/div/div/div[2]/div[1]/div/div/div/div[1]/div/div[2]/div/button").click()
            break
        except:
            time.sleep(1)
    while True:
        try:
            ff.find_element_by_xpath("/html/body/div[6]/div[2]/div/div/div/div[2]/div[1]/div/div/div/div[1]/div/div[1]/div/button[1]").click()
            break
        except:
            time.sleep(1)

login()

#while True:
#    post()
#testCaption  = captionGenerator("nicholasmicholas")
#print(testCaption)
