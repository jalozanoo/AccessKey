# AccessKey v1.0.1 
# This version encrypt all information in a safe way so that if someone wants to acces to this information must 
# to decrypt all the document when the passwords are safe.
# A backward is in the case where the key_file file would lost. In this case it would be neccesary to decrypt and
# restore the file by others ways and AccesKey will be capable to run but without acces to the saved passwords. 
# Program to give or save keys needed to acces to several platforms
# Created by Jhonatan Lozano
from print_msm import *
from generation_code import *

from parse import *
from Crypto.Cipher import AES
from Crypto.Util import Counter
from cryptography.fernet import Fernet
from Crypto.Random import get_random_bytes
import os
import time
import json
import msvcrt
import hashlib


class User:
    pass
    def __init__(self):
        self.overall_password = ''
        self.access_code = False

    def change_password(self,file_controller):
        setattr(user,'overall_password',start())
        setattr(user,'access_code',True)
        password_encrypted = hashlib.sha256(str(getattr(user,'overall_password')).encode()).hexdigest()
        file_controller.cryptographing_file('d',"pwd")
        file_controller.write_file_pwd(password_encrypted,str(getattr(user,'access_code')))
        file_controller.cryptographing_file('e',"pwd")
        succes()
        

    def access_step(self,pass_list,file_controller):
        if not pass_list:
            setattr(user,'overall_password',start())
            setattr(user,'access_code',True)
            password_encrypted = hashlib.sha256(str(getattr(user,'overall_password')).encode()).hexdigest()
            file_controller.cryptographing_file('d',"pwd")
            file_controller.write_file_pwd(password_encrypted,str(getattr(user,'access_code')))
            file_controller.cryptographing_file('e',"pwd")
            succes()
            return -1
        else:
            key_msm = parse("{key}@{created}\n", pass_list[0]) 
            if key_msm['created'] == 'True':
                if input_password(key_msm['key']) == True:
                    return 1
                else:
                    quit()
            else:
                start()

class Accesskey:
    pass
    def __init__(self,id,user,password,flag):
        self.id = id
        self.user = user
        self.password = password
        self.flag = flag
        self.path_access = '.accesskey/services/logins'

    def crypto_data(self,key,msm,ct_rx,flag):
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

    def load_Dictionary(self):
        count = 0
        D = {}
        password = []
        f = open(self.path_access, "r")
        for x in f:
            password.append(x)
            key_msm = parse("{key}@{msm}\n", password[count])
            if key_msm['msm'] != 'True':
                msm_cryp = self.crypto_data(key_msm['key'].encode(),None,key_msm['msm'].encode(),False)
                D_item = json.loads(msm_cryp.decode())
                D.update(D_item)           
            count = count+1
        password.clear()
        f.close()
        return D

    def create_acces(self,file_controller):
        D = {self.id:self.user+'/'+self.password+'/'+str(self.flag)}
        D_str = json.dumps(D).encode('utf-8')
        key = Fernet.generate_key()
        access_encrypted = self.crypto_data(key,D_str,None,True)
        file_controller.write_file(key.decode(),access_encrypted.decode())

    def show_acces(self,file_controller):
        D = self.load_Dictionary()
        file_controller.cryptographing_file('e',"acc")
        print_sorted_list(list(D.keys()), D, columns=4)
        D.clear()

class File_manager:
    pass
    def __init__(self):
        self.path_access = '.accesskey/services/logins'
        self.path_pass = '.accesskey/services/password'
        self.path_key = '.accesskey/services/key_file'
        if os.path.exists(self.path_key):
            key_file = open(self.path_key,'r')
            key = key_file.read().split('\n')
            key_file.close()
            self.key_to_edit_file =''.join(key).encode()
        else:
            self.key_to_edit_file = get_random_bytes(16).hex().encode()
    
    def write_file(self,msm_key,msm):
        f = open(self.path_access, "a")
        f.write(msm_key+"@"+msm+"\n")
        f.close()
    
    def read_file(self):
        f = open(self.path_access, "r")
        list=[] 
        for x in f:
            list.append(x)
        f.close()
        return list
    
    def write_file_pwd(self,msm_key,msm):
        f = open(self.path_pass, "w")
        f.write(msm_key+"@"+msm+"\n")
        f.close()
    
    def read_file_pwd(self):
        f = open(self.path_pass, "r")
        list=[] 
        for x in f:
            list.append(x)
        f.close()
        return list

    def cryptographing_file(self,mode,opt):
        key = getattr(self,'key_to_edit_file')
        if mode == 'd':
            iv = Counter.new(128)
            crypto = AES.new(key,AES.MODE_CTR,counter=iv)
            crypt_file = crypto.decrypt
            self.encrypt_decrypt_methode(crypt_file,opt)
        elif mode == 'e':
            iv = Counter.new(128)
            crypto = AES.new(key,AES.MODE_CTR,counter=iv)
            key_file = open(self.path_key,"w+")
            key_file.write(key.decode())
            key_file.close()
            crypt_file = crypto.encrypt
            self.encrypt_decrypt_methode(crypt_file,opt)
        else:
            error_msm(1)
            quit()
    
    def encrypt_decrypt_methode(self,crypt_file,opt,block_size=16):
        if(opt == "pwd"):
            with open(self.path_pass, "r+b") as accesskey_info:
                pre_encryption = accesskey_info.read(block_size)
                while pre_encryption:
                    encrypted = crypt_file(pre_encryption)
                    if len(pre_encryption) != len(encrypted):
                        raise ValueError('')
                    accesskey_info.seek(-len(pre_encryption),1)
                    accesskey_info.write(encrypted)
                    pre_encryption = accesskey_info.read(block_size)
                accesskey_info.close()
        else:
            try:
                with open(self.path_access, "r+b") as accesskey_info:
                    pre_encryption = accesskey_info.read(block_size)
                    while pre_encryption:
                        encrypted = crypt_file(pre_encryption)
                        if len(pre_encryption) != len(encrypted):
                            raise ValueError('')
                        accesskey_info.seek(-len(pre_encryption),1)
                        accesskey_info.write(encrypted)
                        pre_encryption = accesskey_info.read(block_size)
                    accesskey_info.close()
            except FileNotFoundError:
                path = getattr(file_controller,'path_access')
                os.makedirs(os.path.dirname(path), exist_ok=True)
                if not os.path.exists(path):
                    open(path, "w").close()
                with open(self.path_access, "r+b") as accesskey_info:
                    pre_encryption = accesskey_info.read(block_size)
                    while pre_encryption:
                        encrypted = crypt_file(pre_encryption)
                        if len(pre_encryption) != len(encrypted):
                            raise ValueError('')
                        accesskey_info.seek(-len(pre_encryption),1)
                        accesskey_info.write(encrypted)
                        pre_encryption = accesskey_info.read(block_size)
                    accesskey_info.close()


file_controller = File_manager()
user = User()
edit_acces = Accesskey(None,None,None,None)

while 1:
    if os.path.exists(getattr(file_controller,'path_pass')):
        if os.path.exists(getattr(file_controller,'path_key')):
            file_controller.cryptographing_file('d',"pwd")
        while 1:
            try:
                pass_list = file_controller.read_file_pwd()
            except UnicodeDecodeError:
                file_controller.cryptographing_file('d',"pwd")
            pass_list = file_controller.read_file_pwd()
            file_controller.cryptographing_file('e',"pwd")
            continue_flag = user.access_step(pass_list,file_controller)
            if continue_flag == 1:
                break
        break
    else:
        path = getattr(file_controller,'path_pass')
        os.makedirs(os.path.dirname(path), exist_ok=True)
        if not os.path.exists(path):
            open(path, "w").close()


if continue_flag != 1:
    error_msm(5)
    quit()

while 1:
    os.system("cls")
    menu_general()
    opt = int(input())
    if opt == 1:
        save_new_data = data_to_save()
        if save_new_data != -1:
            file_controller.cryptographing_file('d',"acc")
            setattr(edit_acces,'id',save_new_data[0])
            setattr(edit_acces,'user',save_new_data[1])
            setattr(edit_acces,'password',save_new_data[2])
            setattr(edit_acces,'flag',save_new_data[3])
            edit_acces.create_acces(file_controller)
            file_controller.cryptographing_file('e',"acc")
            print("Nuevo acceso almacenado exitosamente.\n")
            time.sleep(3)
        else:
            continue
        
    elif opt == 2:
        file_controller.cryptographing_file('d',"acc")
        edit_acces.show_acces(file_controller)
        print("Presione una tecla para continuar...")
        msvcrt.getch()

    elif opt == 3:
        if (warning_msm(1) == True):
            user.change_password(file_controller)

    elif opt == 4:
        quit()
    else:
        not_succes('Ingrese las siguientes opciones: 1, 2, 3 o 4')
        time.sleep(3)
        continue
