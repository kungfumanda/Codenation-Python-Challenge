import json
import requests
import hashlib

#requests encrypted json

response = requests.get("https://api.codenation.dev/v1/challenge/dev-ps/generate-data", params={'token' : '818b986d93fdc81e8149924cfe70241aec2aed3f'})
answer = response.json()


#decrypt the encrypted message

def decrypt(encrypted, key):
    decrypted = ""
    for letter in encrypted:
        i = ord(letter)
        if letter.isalpha():
            i -= key
            if i > ord('z'):
                i -= 26
            elif i < ord('a'):
                i += 26
            decrypted += chr(i)
        else:
            decrypted += letter
    return decrypted
message = decrypt(answer['cifrado'].lower(), answer['numero_casas'])
answer['decifrado'] = message


#generates sha1 digest

digest = hashlib.sha1(message.encode()).hexdigest()
answer['resumo_criptografico'] = digest



#sends answer

with open("answer.json", "w") as write_file:
    json.dump(answer, write_file)
write_file.close()

multipart_form_data = {
    'name': "answer"
    ''
}
url = "https://api.codenation.dev/v1/challenge/dev-ps/submit-solution?token=818b986d93fdc81e8149924cfe70241aec2aed3f"
file = { 'answer' : open('answer.json','rb')}

final= requests.post(url, files=file)