import userChecker
import time


count = input('How many accounts do you want to scan?\n')
while count.isnumeric() == False:
    print('Whatever you said was not a digit... Try again!\n')
    count = input('How many accounts do you want to scan?\n')

userID = input('What ID do you want to start from?\n')

while userID.isnumeric() == False:
    print('Whatever you said was not a digit... :( \n')
    userID = input('What ID do you want to start from?\n')


userChecker.checker(int(userID),int(count))

print('\nAll done! :) This program was made by Nizzate on github!')
print("Please check the same directory as this executable for a 'List.txt'!")
time.sleep(5)
