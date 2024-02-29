import requests
import os
import time
def checker(userID,count):
    originalUserID = userID
    while userID <= (originalUserID+count)-1:
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
        fileManager = open('output.txt','w',encoding='utf8')
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
        print('Some weird unicode encoding error happened. Your output file may or may not be affected. (Can affect data compilation!)')   


def skimHTTPData(userID):
    fileManager = open('output.txt','r',encoding='utf8')
    
    accountsFound = []
    usernameInt = 0
    for line in fileManager:
        #print(line)
        if '@' in line:
            usernameInt += 1
            if usernameInt == 5:
                print('Found username.')
                #print(line)
                foundData = 'username',line[line.find('@')+1:-1].replace('"\n','')
                accountsFound.append(foundData)

        if '<div data-profileuserid=' in line:
            print('Found user ID.')
            foundData = 'userID',line[line.find('"')+1:line.find('"')*2].replace('"\n','')
            accountsFound.append(foundData)

        if 'data-friendscount=' in line:
            print('Found friend count.')
            foundData = 'friends',line[line.find('"')+1:line.find('"')*2].replace('"\n','')
            accountsFound.append(foundData)
        
        if 'data-followerscount=' in line:
            print('Found follower count.')
            foundData = 'followers',line[line.find('"')+1:line.find('"')*2].replace('"\n','')
            accountsFound.append(foundData)
        
        if 'data-followingscount=' in line:
            print('Found following count.')
            foundData = 'following',line[line.find('"')+1:line.find('"')*2].replace('"\n','')
            accountsFound.append(foundData)
    
    fileManager.close()
    url = 'https://users.roblox.com/v1/users/'+str(userID)
    getHTTPData(url)
    
    fileManager = open('output.txt','r',encoding='utf8')
    for line in fileManager:
        if '"created"' in line:
            print('Found join date.')
            foundData = 'created',line[line.find('"created":'):line.find('","is')].replace('"\n','').lstrip('"created":')
            accountsFound.append(foundData)
        if 'ned":true' in line:
            print('BANNED USER FOUND!!!')
            accountsFound.append(line)
            #accountsFound.append(userID)
        elif 'ned":false' in line:
            print('Not banned.')
            foundData = 'isBanned',line[line.find('Banned":'):line.find(',"exter')].lstrip('Banned":').replace('"\n',''),'username',line[line.find('name":'):line.find(',"dis')].lstrip('name":').replace('"\n','')
            accountsFound.append(foundData)
        if '"hasVerifiedBadge"' in line:
            print('Found verification status. (Not email verificaion!!!)')
            foundData = 'hasVerifiedBadge',line[line.find('Badge":'):line.find(',"id":')].lstrip('Badge":').replace('"\n','')
            accountsFound.append(foundData)
    #print(accountsFound)
    fileManager.close()
    
    url = 'https://presence.roblox.com/v1/presence/last-online'
    json = {'userIds':[userID]}
    postHTTPData(url,json)

    fileManager = open('output.txt','r')
    for line in fileManager:
        if '"lastOnline"' in line:
            print('Found last seen date.')
            foundData = 'lastOnline',line[line.find('Online":'):line.find('"}]')].lstrip('Online":').replace('"\n','')
            accountsFound.append(foundData)
    return accountsFound
'''
    url = 'https://catalog.roblox.com/v1/users/'+str(userID)+'/bundles?limit=100&sortOrder=Asc'
    getHTTPData(url)
    
    fileManager = open('output.txt','r',encoding='utf8')
    for line in fileManager:
        print(line)
        if 'iBot' in line:
            print('FOUND IBOT ACCOUNT!!!')
            foundData = 'iBot','True'
            accountsFound.append(foundData)
    fileManager.close()'''

    

def writeData(skimmedData):
    fileManager = open('List.txt','a')
    fileManager.write(str(skimmedData).replace('[','').replace(']','\n'))
    fileManager.close()
    os.remove('output.txt')



