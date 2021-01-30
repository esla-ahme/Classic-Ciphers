#Caeser 
def caeser(inputText,cKey): 
    if(isinstance(cKey,str)):
      print("key for caesar cipher must be int") 
      exit(1);  
    
    cipher_text = "" 
    inputText = str.lower(inputText)
    for i in range(len(inputText)): 
        cipher_text += chr((ord(inputText[i]) + cKey - 97) % 26 + 97)   
    return  cipher_text 

def run_caesar():
  for i in [3,6,12]:
    filename = open("./caesar/cipher_for_key_"+str(i),'w')
    
    with open("./caesar/caesar_plain.txt") as f:
        for line in f.readlines():
          filename.write(caeser(line,i)+'\n'+'.txt')
##run_caesar()
####################


#Playfair


#helper functions 


def playfair(inputText,cKey):
  if(isinstance(cKey,str)==False):
      print("key for playfair must be string") 
      exit(1); 

  cKey=cKey.replace(" ", "")
  cKey=cKey.upper()
  cKey =cKey.replace("J", "I")


  cipher_matrix_1d=[]
  for c in cKey: #storing key
      if c not in cipher_matrix_1d:
           cipher_matrix_1d.append(c)
  
  for i in range(65,91): #storing other character
      if chr(i) not in cipher_matrix_1d:
          if (i==74) and chr(73) not in cipher_matrix_1d:
              cipher_matrix_1d.append("I")
          elif (i==74):
            pass 
          else:
              cipher_matrix_1d.append(chr(i))
  
  locationDict = {}
  k=0
  cipher_matrix_2d=[[0 for i in range(5)] for j in range(5)]
  for i in range(0,5):
      for j in range(0,5):
          cipher_matrix_2d[i][j]=cipher_matrix_1d[k]
          locationDict[cipher_matrix_1d[k]] = [i,j]
          k+=1
  
  inputText=inputText.upper()
  inputText=inputText.replace(" ", "")
  inputText=inputText.replace("\n", "")
  inputText=inputText.replace("J", "I")
  i=0
  for s in range(0,len(inputText)+1,2):
      if s<len(inputText)-1:
          if inputText[s]==inputText[s+1]:
              inputText=inputText[:s+1]+'X'+inputText[s+1:]
  
  if len(inputText)%2!=0:
      inputText=inputText[:]+'X'
  
  cipher_text =""
  while i<len(inputText):
    loc=locationDict[inputText[i]]
    loc1=locationDict[inputText[i+1]]
    if loc[1]==loc1[1]:
        cipher_text += cipher_matrix_2d[(loc[0]+1)%5][loc[1]]+cipher_matrix_2d[(loc[0]+1)%5][loc[1]]
    elif loc[0]==loc1[0]:
        cipher_text += cipher_matrix_2d[loc[0]][(loc[1]+1)%5]+cipher_matrix_2d[loc1[0]][(loc1[1]+1)%5]
    else:
        cipher_text += cipher_matrix_2d[loc[0]][loc1[1]]+cipher_matrix_2d[loc1[0]][loc[1]]
    i=i+2        

  return cipher_text


def run_playfair():
  for i in ["rats","archangel"]:
    filename = open("./playfair/cipher_for_key_"+str(i),'w')
    
    with open("./playfair/playfair_plain.txt") as f:
        for line in f.readlines():
          filename.write(playfair(line,i)+'\n')
##run_playfair()
####################


#Hill 

def intializeMatrix(key,keyLen): 
  k = 0
  keyMatrix = [[0] * keyLen for i in range(keyLen)] 
  for i in range(keyLen):  
    for j in range(keyLen): 
      keyMatrix[i][j] = key[k]  
      k += 1
      

  return keyMatrix 


# Following function encrypts the message 
def encrypt(messageVector,keyMatrix,keyLen): 
  cipherMatrix= [[0] for i in range(keyLen)] 
  s=""
  for i in range(keyLen):   
    for j in range(1): 
      cipherMatrix[i][j] = 0
      for x in range(keyLen): 
        cipherMatrix[i][j] += (keyMatrix[i][x] * messageVector[x][j]) 
      cipherMatrix[i][j] = cipherMatrix[i][j] % 26
      s+=(chr(cipherMatrix[i][j]+65))
  return s

def HillCipher(inputText, key): 

  if(not isinstance(key,list) or not all(isinstance(x, int) for x in key)  ):
    print("key for hill cipher must be 1d list of integers the algoritm will transform it for you") 
    exit(1);  
	
  keyLen = len(key)
  if (keyLen != 4 and keyLen != 9)  :
    print("only 2*2 and 3*3 matrices are supported") 
    exit(1);  

  if keyLen == 4:
     keyLen = 2
  else:
     keyLen = 3 



  keyMatrix = intializeMatrix(key,keyLen) 
  inputText = inputText.upper()
  inputText = inputText.replace(" ","")
  inputText = inputText.replace("\n","")
  
  if (len(inputText)%keyLen ==1 and keyLen == 3):
    inputText +=(inputText[-1]*2)
  
  elif (len(inputText)%keyLen == 2 or len(inputText)%keyLen ==1):
    inputText +=inputText[-1]

  

  CipherText =""
  for itr in range(0,len(inputText),keyLen):
    subMsg = inputText[itr:itr+keyLen]
    

    plainVector = [[0] for i in range(keyLen)] 

    for i in range(keyLen): 
      plainVector[i][0] = ord(subMsg[i]) % 65
    
    CipherText+=encrypt(plainVector,keyMatrix,keyLen) 
  
  return CipherText

def run_HillCipher():
  filename = open("./Hill/cipher_for_key_2x2", 'w')  
  with open("./Hill/hill_plain_2x2.txt") as f:
      for line in f.readlines():
        filename.write(HillCipher(line,[5,17,8,3])+'\n')
  filename.close()
  filename = open("./Hill/cipher_for_key_3x3",'w')  
  with open("./Hill/hill_plain_3x3.txt") as f:
      for line in f.readlines():
        filename.write(HillCipher(line,[2,4,12,9,1,6,7,5,3])+'\n')
  filename.close()
##run_HillCipher()

##############

def vigenere(inputText,key,mode=True):
  inputText = inputText.replace(" ",'')
  inputText = inputText.replace("\n",'')
  inputText = inputText.upper()
  key = key.replace(" ",'')
  key = key.replace("\n",'')
  key = key.upper()
  
  inputLen = len(inputText)

  if mode :
    key = key + inputText[:inputLen-len(key)]
  else:  
    key = (key * (inputLen//len(key)) + key[:inputLen%len(key)])
  cipher_text = ''

  for i in range(len(inputText)): 
    x = (ord(inputText[i]) +ord(key[i])) % 26
    x += ord('A')
    cipher_text+=chr(x) 
  
  return cipher_text

def run_vigenere():
  filename = open("./Vigenere/cipher_for_key_pie", 'w')  
  with open("./Vigenere/vigenere_plain.txt") as f:
      for line in f.readlines():
        filename.write(vigenere(line,"pie",False)+'\n')
  filename.close()
  filename = open("./Vigenere/cipher_for_key_aether", 'w')  
  with open("./Vigenere/vigenere_plain.txt") as f:
      for line in f.readlines():
        filename.write(vigenere(line,"aether",True)+'\n')
  filename.close()
##run_vigenere()
###############

def vernam(inputText, key):
  cipherText = ""
  i = 0
  for char in inputText:
    cipherText += chr((ord(char)%65 ^ ord(key[i])%65)+65)
    if i == len(key):
      i = 0
  return cipherText
                      
def run_vernam():
  filename = open("./Vernam/cipher_for_key_SPARTANS", 'w')  
  with open("./Vernam/vernam_plain.txt") as f:
      for line in f.readlines():
        filename.write(vernam(line,"SPARTANS")+'\n')
  filename.close()
##run_vernam()
###############
 
if __name__ == "__main__":
  while True:
    msg = input("Enter Plain Text: ")
    print("Enter encryprtion algorithm number or 0 to exit" )
    code = int(input("""
    1- Caesar
    2- Playfair
    3- Hill
    4- Vernam
    5- Vigenere
    """))
    if code == 0:
      exit(1)
    elif code == 1:
      key = int(input("enter key [Number]: "))
      print(caeser(msg,key))
    elif code == 2:
      key = input("enter key [Word]: ")
      print(playfair(msg,key))
    elif code == 3:
      key = input("Enter key matrix as a sequense of numbers saperated by spaces, Note only 2x2 or 3x3 matrix supported")
      key = key.split(" ")
      key = [int(i) for i in key] 
      print(HillCipher(msg,key))
    elif code == 5:
      key = input("enter key [Word]: ")
      mode = input("for auto mode enter y: ")
      if mode == "y":
        mode =True
      else:
        mode = False
      print(vigenere(msg,key,mode))
    elif code == 4:
      key = input("enter key [Word]: ")
      print(vernam(msg,key))
