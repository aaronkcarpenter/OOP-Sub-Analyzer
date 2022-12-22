import os

def testFunc():
    with open('./test.txt','a') as f: 
        f.write('stuff shitty booty girl')
    f.close()

testFunc()