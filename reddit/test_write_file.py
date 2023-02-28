import os

def testFunc():
    with open('./test.txt','a') as f: 
        f.write('text file writing')
    f.close()

testFunc()