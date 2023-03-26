
from cryptography.fernet import Fernet

def crypto(key,msm,ct_rx,flag):

    cipher = Fernet(key)

    if flag == True: 
        encryptor = cipher.encrypt(msm)
        return encryptor
    elif flag == False:
        decryptor = cipher.decrypt(ct_rx)
        return decryptor
    else:
        print("Fatal error. Closing AccessKey...")
        quit()



