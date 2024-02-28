import requests
def checker(userID,count):
    originalUserID = userID
    while userID <= (originalUserID+count):
        url = "https://www.roblox.com/users/"+str(userID)+"/profile"
        getHTTPData(url)
        skimmedData = skimHTTPData(userID)
        writeData(skimmedData)
        userID = int(userID)
        userID += 1
        print(userID)

# A deliberate typo is made in the endpoint "postz" instead of "posts"


def getHTTPData(url):
    try:
        response = requests.get(url)
        responsePage = response.text
        fileManager = open('output.txt','w')
        fileManager.writelines(responsePage)
        fileManager.close()
        # If the request fails (404) then print the error.
    except requests.exceptions.HTTPError as error:
        print(error)

        """
        404 Client Error: Not Found for url: 
        """
    except UnicodeEncodeError:
        print('Some weird unicode encoding error happened. Your output file may or may not be affected.')   

def postHTTPData(url,json):
    try:
        response = requests.post(url,json = json)
        responsePage = response.text
        fileManager = open('output.txt','w')
        fileManager.writelines(responsePage)
        fileManager.close()
        # If the request fails (404) then print the error.
    except requests.exceptions.HTTPError as error:
        print(error)

        """
        404 Client Error: Not Found for url: 
        """
    except UnicodeEncodeError:
        print('Some weird unicode encoding error happened. Your output file is fine though.')   


def skimHTTPData(userID):
    fileManager = open('output.txt','r')
    
    accountsFound = []
    usernameInt = 0
    for line in fileManager:
        #print(line)
        if '@' in line:
            usernameInt += 1
            if usernameInt == 5:
                print('found username')
                #print(line)
                foundData = 'username',line[line.find('@')+1:-1].replace('"\n','')
                accountsFound.append(foundData)

        if '<div data-profileuserid=' in line:
            print('found user id')
            foundData = 'userID',line[line.find('"')+1:line.find('"')*2].replace('"\n','')
            accountsFound.append(foundData)

        if 'data-friendscount=' in line:
            print('found friend count')
            foundData = 'friends',line[line.find('"')+1:line.find('"')*2].replace('"\n','')
            accountsFound.append(foundData)
        
        if 'data-followerscount=' in line:
            print('found follower count')
            foundData = 'followers',line[line.find('"')+1:line.find('"')*2].replace('"\n','')
            accountsFound.append(foundData)
        
        if 'data-followingscount=' in line:
            print('found following count')
            foundData = 'following',line[line.find('"')+1:line.find('"')*2].replace('"\n','')
            accountsFound.append(foundData)
    
    fileManager.close()
    url = 'https://users.roblox.com/v1/users/'+str(userID)
    getHTTPData(url)
    
    fileManager = open('output.txt','r')
    for line in fileManager:
        if '"created"' in line:
            print('found join date')
            foundData = 'created',line[line.find('"created":'):line.find('","is')].replace('"\n','').lstrip('"created":')
            accountsFound.append(foundData)
        if 'ned":true' in line:
            print('BANNED USER FOUND')
            foundData = 'isBanned',line[line.find('Banned":'):line.find(',"exter')].lstrip('Banned":').replace('"\n','')
            accountsFound.append(foundData)
            accountsFound.append(userID)
        elif 'ned":false' in line:
            print('not banned')
            foundData = 'isBanned',line[line.find('Banned":'):line.find(',"exter')].lstrip('Banned":').replace('"\n','')
            accountsFound.append(foundData)
        if '"hasVerifiedBadge"' in line:
            print('found verification status (blue check mark)')
            foundData = 'hasVerifiedBadge',line[line.find('Badge":'):line.find(',"id":')].lstrip('Badge":').replace('"\n','')
            accountsFound.append(foundData)
    fileManager.close()
    
    url = 'https://presence.roblox.com/v1/presence/last-online'
    json = {'userIds':[userID]}
    postHTTPData(url,json)

    fileManager = open('output.txt','r')
    for line in fileManager:
        if '"lastOnline"' in line:
            print('found last seen date')
            foundData = 'lastOnline',line[line.find('Online":'):line.find('"}]')].lstrip('Online":').replace('"\n','')
            accountsFound.append(foundData)

    return accountsFound

def writeData(skimmedData):
    fileManager = open('data.txt','a')
    fileManager.write(str(skimmedData).replace('[','').replace(']','\n'))
    fileManager.close()



