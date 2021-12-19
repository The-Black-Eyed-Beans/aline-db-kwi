import login
import requests

from faker import Faker
from faker.providers import bank, company, address

fake = Faker('en_US')
fake.add_provider(bank)
fake.add_provider(company)
fake.add_provider(address)

bearer = login.get_bearer()

bank_ms = 'http://localhost:8083'

num = ''

while True:
    num = input('Enter the number of banks you would like to add: ')
    if num.isnumeric() and int(num) > 0:
        break
    print('Please enter a valid number greater than zero.')

for i in range(1, int(num) + 1):
    bank = {
        'routingNumber': fake.numerify(text='#########'),
        'address': fake.street_address(),
        'city': fake.city(),
        'state': fake.state(),
        'zipcode': fake.postalcode()
    }

    print('Bank')
    response = requests.post(bank_ms + '/banks', json=bank, headers={'Authorization': bearer})
    print(response.json())

    branchValue = {
        'name': fake.company(),
        'phone': fake.numerify(text='(###) ###-####'),
        'address': bank['address'],
        'city': bank['city'],
        'state': bank['state'],
        'zipcode': bank['zipcode'],
        'bankID': response.json()['id']
    }

    print('Branch')
    branch = requests.post(bank_ms + '/branches', json=branchValue, headers={'Authorization': bearer})
    print(branch.json())

    print()
