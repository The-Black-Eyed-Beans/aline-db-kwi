import api
import logger
import login
import requests
import sys

from faker import Faker
from faker.providers import bank, company, address


def check_cli_args():
    return len(sys.argv) > 1 and sys.argv[1].isnumeric() and int(sys.argv[1]) > 0


fake = Faker('en_US')
fake.add_provider(bank)
fake.add_provider(company)
fake.add_provider(address)

info = logger.get_info_logger()
debug = logger.get_debug_logger()
error = logger.get_error_logger()

bearer = login.get_bearer()

# Initialize a variable to later use in current scope
num = None

# Grab the number of applicants to add to the database. Only accepts an int greater than 0
while True:
    num = sys.argv[1] if check_cli_args() else input('Enter the number of banks you would like to add: ')
    if num.isnumeric() and int(num) > 0:
        break
    info.log('Please enter a valid number greater than zero.')

debug.debug(str(num) + ' bank(s) are being generated...')

for i in range(1, int(num) + 1):
    bank = {
        'routingNumber': fake.numerify(text='#########'),
        'address': fake.street_address(),
        'city': fake.city(),
        'state': fake.state(),
        'zipcode': fake.postalcode()
    }

    debug.debug('Bank #' + str(i))
    try:
        response = requests.post(api.get_bank_api(), json=bank, headers={'Authorization': bearer})
    except Exception as ex:
        error.error('Error with creating bank: ' + str(ex))
        error.error('Provided JSON: ' + str(bank))

    if response.status_code in range(200, 300):
        debug.debug(response.json())

        branchValue = {
            'name': fake.company(),
            'phone': fake.numerify(text='(###) ###-####'),
            'address': bank['address'],
            'city': bank['city'],
            'state': bank['state'],
            'zipcode': bank['zipcode'],
            'bankID': response.json()['id']
        }

        debug.debug('Branch #' + str(i))
        try:
            branch = requests.post(api.get_branch_api(), json=branchValue, headers={'Authorization': bearer})
        except Exception as ex:
            error.error('Error with creating branch: ' + str(ex))
            error.error('Provided JSON: ' + str(branchValue))

        if branch.status_code in range(200, 300):
            debug.debug(branch.json())
        else:
            error.error('Failed to create branch. Status Code received: ' + str(branch.status_code))
    else:
        error.error('Failed to create bank. Status Code received: ' + str(response.status_code))
    debug.debug('')
debug.debug('#####################################################################################################')
