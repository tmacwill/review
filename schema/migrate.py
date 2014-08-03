import os

path = os.path.dirname(os.path.realpath(__file__)) + '/'
migrations_path = path + '/migrations/'
data_path = path + '/data/'

# start with a fresh database
os.system("mysql -uroot -e 'drop database review' >/dev/null 2>&1")
os.system("mysql -uroot -e 'create database review'")

# run all migrations in order
migrations = [i for i in sorted(os.listdir(migrations_path), key=lambda e: int(e.split('.')[0]))]
for file in migrations:
    os.system("mysql -uroot review < " + migrations_path + file)

# populate data
data = os.listdir(data_path)
for file in data:
    os.system("mysql -uroot review < " + data_path + file)
