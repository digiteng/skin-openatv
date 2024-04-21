from decouple import config

user = config('user', default='')
password = config('password', default='')

print(user, password)

