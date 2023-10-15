import requests
import time
import secrets

def send_req(message):
    # time.sleep(0.3)
    requests.post("http://localhost:5000/connect", json={"data": message},headers = {'Content-type': 'application/json'})
    
def generate_key():
    ''' genearate key '''
    return secrets.token_hex(6)

# import re
# output="D:\Ganga\Arjun_Project\static\\files\\abc.txt"
# pat=re.search("[a-zA-z0-9]+[.]txt$", output)
# print(pat.group(0))