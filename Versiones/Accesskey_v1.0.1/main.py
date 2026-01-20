# AccessKey v1.0.1 
# This version encrypt all information in a safe way so that if someone wants to acces to this information must 
# to decrypt all the document when the passwords are safe.
# A backward is in the case where the key_file file would lost. In this case it would be neccesary to decrypt and
# restore the file by others ways and AccesKey will be capable to run but withous acces to the saved passwords. 
# Program to give or save keys needed to acces to several platforms
# Created by Jhonatan Lozano

from parse import *
from print_msm import *
from generation_code import *
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

    def change_password(self):
        return 1

    def access_step(self,pass_list,file_controller):
        if not pass_list:
            setattr(user,'overall_password',start())
            setattr(user,'access_code',True)
            password_encrypted = hashlib.sha256(str(getattr(user,'overall_password')).encode()).hexdigest()
            file_controller.cryptographing_file('d')
            file_controller.write_file(password_encrypted,str(getattr(user,'access_code')))
            succes()
            return -1
        else:
            key_msm = parse("{key}@{created}\n", pass_list[0]) 
            if key_msm['created'] == 'True':
                if input_password(key_msm['key']) == True:
                    return 1
                else:
                    print('opcion para solicitar cambio de clave. Pensado para siguiente versión')
            else:
                start()

class Accesskey:
    pass
    def __init__(self,id,user,password,flag):
        self.id = id
        self.user = user
        self.password = password
        self.flag = flag

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
        f = open("password", "r")
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
        file_controller.cryptographing_file('e')
        print_sorted_list(list(D.keys()), D, columns=4)
        D.clear()

class File_manager:
    pass
    def __init__(self):
        if os.path.exists('key_file'):
            key_file = open('key_file','r')
            key = key_file.read().split('\n')
            key_file.close()
            self.key_to_edit_file =''.join(key).encode()
        else:
            self.key_to_edit_file = get_random_bytes(16).hex().encode()

    def write_file(self,msm_key,msm):
        f = open("password", "a")
        f.write(msm_key+"@"+msm+"\n")
        f.close()
    
    def read_file(self):
        f = open("password", "r")
        list=[] 
        for x in f:
            list.append(x)
        f.close()
        return list

    def cryptographing_file(self,mode):
        key = getattr(self,'key_to_edit_file')
        if mode == 'd':
            iv = Counter.new(128)
            crypto = AES.new(key,AES.MODE_CTR,counter=iv)
            crypt_file = crypto.decrypt
            self.encrypt_decrypt_methode(crypt_file)
        elif mode == 'e':
            iv = Counter.new(128)
            crypto = AES.new(key,AES.MODE_CTR,counter=iv)
            key_file = open("key_file","w+")
            key_file.write(key.decode())
            key_file.close()
            crypt_file = crypto.encrypt
            self.encrypt_decrypt_methode(crypt_file)
        else:
            print('Error durante encripción. Cerrando AccessKey v.1.0.1\n')
            quit()
    
    def encrypt_decrypt_methode(self,crypt_file,block_size=16):
        with open("password", "r+b") as accesskey_info:
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
    if os.path.exists('password'):
        if os.path.exists('key_file'):
            file_controller.cryptographing_file('d')
        while 1:
            try:
                pass_list = file_controller.read_file()
            except UnicodeDecodeError:
                file_controller.cryptographing_file('d')
            pass_list = file_controller.read_file()
            file_controller.cryptographing_file('e')
            continue_flag = user.access_step(pass_list,file_controller)
            if continue_flag == 1:
                menu_general()
                break
        break
    else:
        f = open("password", "x")
        f.close()

if continue_flag != 1:
    print('Error al iniciar. Cerrando AccessKey v.1.0.1\n')
    quit()

while 1:
    menu_general()
    opt = int(input())
    if opt == 1:
        save_new_data = data_to_save()
        file_controller.cryptographing_file('d')
        setattr(edit_acces,'id',save_new_data[0])
        setattr(edit_acces,'user',save_new_data[1])
        setattr(edit_acces,'password',save_new_data[2])
        setattr(edit_acces,'flag',save_new_data[3])
        edit_acces.create_acces(file_controller)
        file_controller.cryptographing_file('e')
        print("Nuevo acceso almacenado exitosamente.\n")
        time.sleep(3)
        
    elif opt == 2:
        file_controller.cryptographing_file('d')
        edit_acces.show_acces(file_controller)
        print("Presione una tecla para continuar...")
        msvcrt.getch()

    elif opt == 3:
        quit()
    else:
        not_succes('Ingrese las siguientes opciones: 1, 2 o 3')
        time.sleep(2)
        continue
