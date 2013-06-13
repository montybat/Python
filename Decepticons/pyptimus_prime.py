from hashlib import md5
from hashlib import sha256
from hashlib import sha1
from hashlib import sha224
from hashlib import sha384
from hashlib import sha512
from base64 import standard_b64encode
import os

#Time to defeat Megatron once and for all
#
#Step 1: create attack dictionaries with various encryptions
#Step 2: create attack lists from these dictionaries
#Step 2: create target list (decepticon, encrypted_password)
#Step 3: attack the target list

# defines and opens the attack dictionary
attack_dic_filename = "./attack_dictionaries/attack_dictionary.txt"

attack_dic_file = open(attack_dic_filename, 'a')

attack_dic_file_read = open(attack_dic_filename, 'r')

# defines and opens other files
dictionary_fn = "british-english.txt"
dictionary_f = open(dictionary_fn, 'r')
dictionary_fn_2 = "british-english-copy.txt"
dictionary_f_2 = open(dictionary_fn_2, 'r')
target_fn = "big_guy.txt"
salt = "saltysaltgoodness" 

def create_attack_dictionaries():
    print "\n---------Writing Attack Dictionaries----------\n"
    for word in dictionary_f:
        # creates the encrypted strings
        md5_encrypted_string = md5(word.rstrip() + salt).hexdigest()
        sha256_encrypted_string = sha256(word.rstrip() + salt).hexdigest()
        base64_md5_encrypted_string = standard_b64encode(md5(word.rstrip() + salt).hexdigest())
        base64_sha256_encrypted_string = standard_b64encode(sha256(word.rstrip() + salt).hexdigest())
        sha1_encrypted_string = sha1(word.rstrip() + salt).hexdigest()
        sha224_encrypted_string = sha224(word.rstrip() + salt).hexdigest()
        sha384_encrypted_string = sha384(word.rstrip() + salt).hexdigest()

                
      
        # writes them to file
        attack_dic_file.write("{};{}\n".format(word.rstrip(), md5_encrypted_string))
        attack_dic_file.write("{};{}\n".format(word.rstrip(), sha256_encrypted_string))
        attack_dic_file.write("{};{}\n".format(word.rstrip(), base64_md5_encrypted_string))
        attack_dic_file.write("{};{}\n".format(word.rstrip(), base64_sha256_encrypted_string))
        attack_dic_file.write("{};{}\n".format(word.rstrip(), sha1_encrypted_string))
        attack_dic_file.write("{};{}\n".format(word.rstrip(), sha224_encrypted_string))
        attack_dic_file.write("{};{}\n".format(word.rstrip(), sha384_encrypted_string))
    print "\n---------Done with Attack Dictionaries----------\n"


        


def check_if_dictionaries_exist(attack_dic_filename):
    print "\n---------Checking Attack Dictionary Status----------\n"
    try:
        file_size = os.path.getsize(attack_dic_filename)
        print "{} is {} bytes large.".format(attack_dic_filename, file_size)
    except:
        print "\t {} does not exist!".format(file)

def create_attack_list(attack_dictionary):
    attack_list = []
    for line in attack_dictionary:
        (plaintext, encrypted) = line.split(";")
        attack_list.append((plaintext, encrypted.rstrip()))
    return attack_list

def create_targets_list(target_fn):
    target_list = []
    for line in open(target_fn, 'r'):
        (user, uid, encrypted_password) = line.rstrip().split(":")
        target_list.append((user, encrypted_password))
    return target_list            

def attack_target_list(target_list, attack_list):
    for target in target_list:
        (user, target_password) = target

        for word in attack_list:
            (attack_word_plaintext, attack_word_encrypted) = word
            if target_password == attack_word_encrypted:
                print "Decepticon password identified! user:{}\tpassword:{}".format(user, attack_word_plaintext)


            
### program starts running here   #####

# first checks if attack dictionaries exist        
check_if_dictionaries_exist(attack_dic_filename)

#prompts to recreate
print "\n Would you like to recreate the attack dictionaries?"
yes_or_no = raw_input("\nYes or No: ")
if yes_or_no.lower() in "yes ok sure":
    create_attack_dictionaries()


# creates the attack lists from the dictionary files
attack_list = create_attack_list(attack_dic_file_read)

#returns a list of targetes and encrypted passwords based on name of user and hashed text file
identified_target_list = create_targets_list(target_fn)

#tries to match text from attack list to target list
print "Decoding Decepticon passwords...."
attack_target_list(identified_target_list, attack_list)



print "Done."

# closes files
attack_dic_file.close()

    