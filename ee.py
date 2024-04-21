from decouple import config
user="engn"
password="1234"
user = config(user, default='')
password = config(password, default='')

print(user, password)

