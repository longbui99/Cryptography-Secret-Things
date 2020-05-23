from Crypto.Cipher import DES,AES,DES3
from Crypto.Hash import SHA1
from Crypto import Random
import time
import os
import datetime
class Algorithms:
    """
    Init method:
    Purpose: 
    - Constructor of Algorithms class, use to define some variable or constraint.
    Parameter: 
    + obj -> Class UI (User interface) for rendering
    """
    def __init__(self, obj):

        self.dataField = obj.mainObject
        self.ui = obj
        self.sha = SHA1.new()

        self.NONCECONSTRAINT = 16
        self.HASHCONSTRAINT = 20
        self.NAMEAPPCONSTRAINT = "SET"
        self.SPEEDCONSTRAINT = None

        self.keyContraint=(
            ("DES",8),
            ("AES",16),
            ("3DES",24)
        )
        
    """
    readDatafile method:
    Purpose: 
    - Read bytes of file, line by line, use to get list key what require for decode
    Parameter: 
    + url: The path direct to file includes key.
    """
    def readDataFile(self,url):
        lst = None
        try: 
            with open(url,'rb') as f:
                lst = f.read()
        except FileNotFoundError as f:
            raise f
        return lst.split(b'\r\n')

    """
    readBytesFile method:
    Purpose:
    - Read byte of file, use to get File (DECODE or ENCODE) data
    Parameter:
    + url: The path direct to file necessary
    + noncec: Flag, make sure that we can decode by only one way, save by encode
    """
    def readBytesFile(self,url, noncec=False):
        # prevHash, the Hash data in file saving by encode function, required to check security
        data,nonce,prevHash = None,None,None
        try:
            with open(url,'rb') as f:
                if noncec:
                    nonce=f.read(self.NONCECONSTRAINT)
                    prevHash=f.read(self.HASHCONSTRAINT)
                data=f.read()
            return (data,nonce,prevHash)
        except FileNotFoundError as f:
            raise f

    """
    writeBytesFile method:
    Purpose:
    - Write to data file, just only use to write encode file.
    Parameter:
    + data: Data of file had been encoded
    + url: Path to create a new encode file/folder to save
    + crypto: Type of cryptography (ENCODE or DECODE)
    + filePath: Path from the root folder select (if use folder func) to file
    """
    def writeBytesFile(self, data,url, crypto, filePath):
        # # Create file name
        fileName=self.nameFileAnalyst(filePath,crypto)
        # If folder is not exist, create new
        if not self.dataField[2]:
            for x in filePath.split("/")[:-1]:
                # print(x)
                if not os.path.exists(url+x):
                    os.makedirs(url+x)
                url = url +x+"/"
        try:
            with open(url+fileName,'wb') as f:
                f.write(data)
        except FileNotFoundError as f:
            raise f

    """
    checkPrefixActive method:
    Purpose: Verify the conditions are satisfied
    """
    def checkPrefixActive(self):
        # copy datafield to tple
        tple = self.dataField
        Alert = []
        c=True
        # Except case of True/False, if we had None what is inside data recieved.
        # Condition is unsatisfactory
        for index, obj in enumerate(tple):
            if obj==None:
                c = False
            Alert.append(self.ui.raiseError((index,obj)))
        # Call the showActiveConsole of User interface to render what we had been analyst
        self.ui.showActiveConsole(Alert)
        return c

# -----------------------------------------------------------------
    """
    getListKey method:
    Purpose: Get the list of key which is require to Cryptography
    Parameter:
    + listInput: List of path to file will be analyze
    """
    def getListKey(self, listInput):
        # dataField[4] is conditions tell us what we should do next, 
        # automatic key or read file 
        if self.dataField[4]:
            return self.automaticGenerateKey(listInput)
        else:
            return self.getListKeyFromFile(len(listInput))


    """
    automaticGenerateKey method:
    Purpose: Automatic generate key and write it to file
    Parameter:
    + listInput: List of path to file will be analyze
    """
    def automaticGenerateKey(self, listInput):
        keyLength = 8
        # First, we have to know length bytes of key
        for x in self.keyContraint:
            if x[0] == self.dataField[0]:
                keyLength = x[1]
        # Seccond, We generate a list with constructor (filename,Key)
        lst = [[  bytes(x.split('/')[-1],'utf8')  ,Random.get_random_bytes(keyLength)] for x in listInput]
        self.generateFileKey(lst)
        return lst

    """
    generateFileKey method:
    Purpose: Create file key and write list key to file
    Parameter:
    + lst: List (filename,key) had been generate by automaticGenerateKey method
    """
    def generateFileKey(self,lst):
        # Step by Step
        # Step 1, generate file name
        filename = self.NAMEAPPCONSTRAINT+"-KEY-"+datetime.datetime.now().strftime("%Y-%m-%d;%H-%M")+".bin"
        with open(self.dataField[5]+"/"+filename,'wb') as f:
            for x in lst[:-1]:
                # Step2 , encode string to bytes
                f.write(x[0]+b"=")
                # Step 2.1, write key data
                f.write(x[1])
                # Step 3, newline
                f.write(b'\r\n')
            f.write(lst[-1][0]+b"=")
            # Step 2.1, write key data
            f.write(lst[-1][1])

    """
    generateListKeyFromFile method:
    """
    def getListKeyFromFile(self,leng):
        listKey = self.readDataFile(self.dataField[5])
        if len(listKey) >1 and not len(listKey) == leng:
            raise ValueError("Number of keys are not same with number of Files");
        
        listK = []

        for i in range(0, len(listKey)):
            temp = []
            listKey[i] = listKey[i].split(b'=')
            if len(listKey[i]) == 1: continue
            filename = b"=".join(listKey[i][:-1])
            t,t1 = filename,listKey[i][-1]
            listK.append([t,t1])

        if len(listK) == 1:
            if listK[0][0].lower() == "all":
                listK = [["all",listK[0][1]]]
        # for index,x in enumerate(listK):
        #     print(index,",",x[0],",",len(x[1]))
        return listK

    def findKeyValue(self,url,crypto,listKey):
        fileName = url.split('/')[-1]
        obj = fileName
        response = None
        if not crypto:
            obj = fileName[0:-4]
        if len(listKey) == 1 and listKey[0][0] == "all":
            return listKey[0][1]
        for x in listKey:
            if bytes(obj,'utf8') == x[0]:
                return x[1]
        if response is None:
            raise ValueError(obj + " is not exists in "+url)

    def getListInput(self,typeInput):
        listInput =  None
        if typeInput:
            listInput = [self.dataField[3]]
        else:
            listInput = []
            for root,direct,files in os.walk(self.dataField[3]):
                for file in files:
                    if file == "desktop.ini": continue
                    url = (root.replace("\\","/")+"/"+file)
                    listInput.append(url)
        return listInput

    def nameFileAnalyst(self,url, Check):
        filenameFully = url.split('/')[-1]
        if Check:
            filenameFully=filenameFully+".bat"
        else:
            filenameFully = filenameFully.split('.')
            fileName = ".".join(filenameFully[:-2])
            fileEx = filenameFully[-2]
            filenameFully = fileName+"-Decode."+fileEx
        return filenameFully

    def getFunctionEncodeOrDecode(self):
        if self.dataField[0] is "DES":
            return self.DESAlgorithms
        elif self.dataField[0] is "3DES":
            return self.DES3Algorithms
        elif self.dataField[0] is "AES":
            return self.AESAlgorithms
        elif self.dataField[0] is "RSA":
            return self.RSAAlgorithms

    def generateListSizeFile(self, listInput):
        returnVal = []
        for x in listInput:
            returnVal.append((x,os.path.getsize(x)))
        return returnVal


    def runField(self):
        if not self.checkPrefixActive():
            return
        self.ui.displayHistory()
        self.ui.updateWorking(True)
        self.ui.controlProcessingFrame(True)
        # Get Algoritms and Type reading input
        crypto,typeInput = self.dataField[1],self.dataField[2]
        # Get reading input file
        listInput = self.getListInput(typeInput)

        self.ui.modifyProcessingList(False, self.generateListSizeFile(listInput))
        # Get reading input and duplicate^n
        listKey = None
        try:
            listKey = self.getListKey(listInput)
        except ValueError as v:
            self.ui.AlertConsole(v)
            return
        # Showing ui to user
        # Get type of algorithms should be use
        
        stepTime = startTime = time.time()
        func = self.getFunctionEncodeOrDecode()
        
        leng = len(self.dataField[3])+1
        lengK = len(listKey)
        lengI = len(listInput)
        self.ui.showFileandKey((lengI,lengK),True, str(0)+"/")
        Check = True

        self.ui.initActive()
        count = 1
        for url in listInput:
            # Read bytes file input`
            self.ui.updateAndTerminate(False,os.path.getsize(url)/self.SPEEDCONSTRAINT if self.SPEEDCONSTRAINT is not None else 0)
            response = None
            try:
                response = self.readBytesFile(url, False if crypto else True)
            except FileNotFoundError as f:
                self.ui.AlertConsole(str(f)[10:])
                self.ui.addHistory((crypto,False,url,datetime.datetime.now().strftime("%H:%M:%S>>")))
                return
            # Convert reponse data to type
            data,nonce,prevHash = response[0],response[1],response[2]
            # Start encode or decode
            # print("prevHash: ",prevHash)
            try:
                key = self.findKeyValue(url,crypto,listKey)
            except ValueError as e:
                self.ui.insertNotificationConsole((url,">> file not found in" + url), False)
                self.ui.addHistory((crypto,False,url,datetime.datetime.now().strftime("%H:%M:%S>>")))
                continue
            # print(key,",",len(key))
            try:
                (result,hashCompare) = func(data,key,nonce,crypto,prevHash)
            except ValueError as e:
                self.ui.AlertConsole( "File <<" + url.split('/')[-1]  +">>, ValueError: " + str(e) + "")
                self.ui.addHistory((crypto,False,url,datetime.datetime.now().strftime("%H:%M:%S>>")))
                return
            # Writeback to file
            # # Start write output symetric
            try:
                self.writeBytesFile(result,self.dataField[6],crypto,url if typeInput else url[leng:])
            except FileNotFoundError as f:
                self.ui.AlertConsole(str(f)[10:])
                self.ui.addHistory((crypto,False,url,datetime.datetime.now().strftime("%H:%M:%S>>")))
                return
            # Update history to user
            self.ui.addHistory((crypto,True,url,datetime.datetime.now().strftime("%H:%M:%S>>")))
            # # Start write output hash one way
            avtime = time.time()-stepTime
            self.ui.insertNotificationConsole((url," :: has been verified" if hashCompare else " ::  has been changed"),hashCompare)

            self.SPEEDCONSTRAINT = os.path.getsize(url)/ avtime +1E-10
            stepTime=time.time()
            self.ui.showFileandKey((lengI,lengK),True, str(count)+"/")
            self.ui.modifyProcessingList(True)
            count=count+1

        self.ui.updateAndTerminate(True)

        self.ui.showFileandKey((lengI,lengK),  True )
        if not crypto:
            if Check:
                # If same 100%, raise OK to user
                self.ui.AlertConsole("-  Hash verify all files  ", False)
            else:
                # If does not same 100%, raise Error to user
                self.ui.AlertConsole("Please becareful, you files had been changed")
        self.ui.AlertConsole("-  Time: {time:.5f}".format(time=time.time()-startTime),boo=True)
        self.ui.updateWorking(False)
        
 
    def DESAlgorithms(self,data,key,nonce,cryp,prevHash):
        #Action is the algorithms of DES Crypto library
        # print(len(key))
        action= DES.new(key,mode=DES.MODE_EAX,nonce=nonce)
        # action= DES.new(key,mode=DES.MODE_CBC)#,nonce=nonce)
        #Get result, can be encode or decode
        result = action.encrypt(data) if cryp else action.decrypt(data)
        # Check if value is same or not
        Check  = True
        if cryp:
            sha = SHA1.new()
            sha.update(data)
            # result = action.nonce + sha.digest() + result
            result = sha.digest() + result
        else:
            sha = SHA1.new()
            sha.update(result)
            if sha.digest() == prevHash:
                Check= True
            else:
                Check= False
        # Read key
        return (result,Check)
        
    def AESAlgorithms(self,data,key,nonce,cryp,prevHash):
        # Action in the algorithms of AES Crypto library
        action = AES.new( key,mode=AES.MODE_EAX,nonce=nonce)
        #Get result, can be decode or encode
        result = None
        Check = True
        if cryp:
            result = action.encrypt(data)
            sha = SHA1.new()
            sha.update(data)
            result = action.nonce + sha.digest() + result
            # print("ENCODE nonce:",action.nonce)
            # print("ENCODE hash:", sha.digest())
        else:
            result = action.decrypt(data)
            sha = SHA1.new()
            sha.update(result)
            # print("ENCODE nonce:",nonce)
            # print("ENCODE hash:", sha.digest())
            if sha.digest() == prevHash:
                Check=True
            else:
                Check=False
        return (result,Check)

    def DES3Algorithms(self,data,key,nonce,cryp,prevHash):
        action  = DES3.new(key,mode=DES3.MODE_EAX,nonce=nonce)
        result = action.encrypt(data) if cryp else action.decrypt(data)
        # Check if value is same or not
        Check  = True
        if cryp:
            sha = SHA1.new()
            sha.update(data)
            result = action.nonce + sha.digest() + result
        else:
            sha = SHA1.new()
            sha.update(result)
            if sha.digest() == prevHash:
                Check= True
            else:
                Check= False
        # Read key
        return (result,Check)
    
