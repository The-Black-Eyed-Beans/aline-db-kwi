import api
import logger
import login
import requests
import sys

from faker import Faker
from faker.providers import internet, ssn, person, date_time, address, phone_number
from random import randint


def check_cli_args():
    return len(sys.argv) > 1 and sys.argv[1].isnumeric() and int(sys.argv[1]) > 0


# Initialize Faker variable
fake = Faker('en_US')
fake.add_provider(internet)
fake.add_provider(ssn)
fake.add_provider(person)
fake.add_provider(date_time)
fake.add_provider(address)
fake.add_provider(phone_number)

info = logger.get_info_logger()
debug = logger.get_debug_logger()
error = logger.get_error_logger()

# Grab the bearer key for use in the python script
bearer = login.get_bearer()
if bearer is None:
    error.error('Capture of Bearer Token failed. Exiting program.')
    exit(0)

# Create list variables for the enums used by the various microservices
genderTypes = ['MALE', 'FEMALE', 'OTHER', 'UNSPECIFIED']
appTypes = ['CHECKING', 'SAVINGS', 'CHECKING_AND_SAVINGS', 'CREDIT_CARD', 'LOAN']
transTypes = ["DEPOSIT", "WITHDRAWAL", "TRANSFER_IN", "TRANSFER_OUT", "PURCHASE", "PAYMENT", "REFUND", "VOID"]
methodTypes = ["ACH", "ATM", "CREDIT_CARD", "DEBIT_CARD", "APP"]

# Initialize a variable to later use in current scope
num = None

# Grab the number of applicants to add to the database. Only accepts an int greater than 0
while True:
    num = sys.argv[1] if check_cli_args() else input('Enter the number of applicants you would like to add: ')
    if num.isnumeric() and int(num) > 0:
        break
    info.log('Please enter a valid number greater than zero.')

debug.debug(str(num) + ' applicant(s) are being generated...')

for i in range(1, int(num) + 1):
    gender = genderTypes[randint(0, 3)]
    if gender == 'MALE':
        firstName = fake.first_name_male()
    elif gender == 'FEMALE':
        firstName = fake.first_name_female()
    elif gender == 'OTHER':
        firstName = fake.first_name()
    else:
        firstName = fake.first_name()

    address = fake.street_address()
    city = fake.city()
    state = fake.state()
    zipcode = fake.postalcode()

    value = {
        'firstName': firstName,
        'lastName': fake.last_name(),
        'dateOfBirth': str(fake.date_of_birth(minimum_age=18)),
        'gender': gender,
        'email': fake.email(),
        'phone': fake.numerify(text='(###) ###-####'),
        'socialSecurity': fake.ssn(),
        'driversLicense': fake.numerify(text='#########'),
        'income': randint(2500000, 7000000),
        'address': address,
        'city': city,
        'state': state,
        'zipcode': zipcode,
        'mailingAddress': address,
        'mailingCity': city,
        'mailingState': state,
        'mailingZipcode': zipcode
    }

    debug.debug('Applicant #' + str(i))
    try:
        response = requests.post(api.get_applicant_api(), json=value, headers={'Authorization': bearer})
    except Exception as ex:
        error.error('Error with creating applicant: ' + str(ex))
        error.error('Provided JSON: ' + str(value))

    if response.status_code in range(200, 300):
        debug.debug(response.json())

        appType = appTypes[randint(0, 4)]

        application = {
            'applicationType': appType,
            'noApplicants': True,
            'applicantIds': [response.json()['id']]
        }

        debug.debug('Application #' + str(i))
        try:
            app = requests.post(api.get_application_api(), json=application, headers={'Authorization': bearer})
        except Exception as ex:
            error.error('Error with creating application: ' + str(ex))
            error.error('Provided JSON: ' + str(application))

        if app.status_code in range(200, 300):
            debug.debug(app.json())

            userValue = {
                'role': 'member',
                'username': fake.user_name(),
                'password': fake.password(length=15, special_chars=True, digits=True, lower_case=True, upper_case=True),
                'membershipId': app.json()['createdMembers'][0]['membershipId'],
                'lastFourOfSSN': response.json()['socialSecurity'].split('-')[-1]
            }

            debug.debug('User #' + str(i))
            debug.debug(userValue)
            try:
                user = requests.post(api.get_user_api() + '/registration', json=userValue)
            except Exception as ex:
                error.error('Error with creating user: ' + str(ex))
                error.error('Provided JSON: ' + str(userValue))

            if user.status_code in range(200, 300):
                debug.debug(user.json())

                if 'createdAccounts' in app.json():
                    for j in range(0, len(app.json()['createdAccounts'])):
                        debug.debug('Transactions for Account #' + str(app.json()['createdAccounts'][j]['accountNumber']))
                        for k in range(1, 3):
                            transValue = None
                            merchantTransactions = [0, 4, 5, 6, 7]

                            transType = randint(0, 7)
                            if transType in merchantTransactions:
                                code = ''
                                for charAt in range(0, randint(5, 8)):
                                    code += fake.random_uppercase_letter()
                                name = fake.company()

                                trans = transTypes[transType]
                                method = methodTypes[randint(0, 4)]

                                description = fake.sentence(nb_words=10, variable_nb_words=True)
                                transValue = {
                                    'type': trans,
                                    'method': method,
                                    'amount': randint(20000, 200000),
                                    'merchantCode': code,
                                    'merchantName': name,
                                    'description': description,
                                    'accountNumber': app.json()['createdAccounts'][j]['accountNumber']
                                }
                            else:
                                trans = transTypes[transType]
                                method = methodTypes[randint(0, 4)]

                                transValue = {
                                    'type': trans,
                                    'method': method,
                                    'amount': randint(20000, 200000),
                                    'accountNumber': app.json()['createdAccounts'][j]['accountNumber']
                                }
                            # TODO: Add try-catch for requests.post()
                            try:
                                trans = requests.post(api.get_trans_api(), json=transValue, headers={'Authorization': bearer})
                            except Exception as ex:
                                error.error('Error with creating transaction: ' + str(ex))
                                error.error('Provided JSON: ' + str(transValue))
                            if trans.status_code in range(200, 300):
                                debug.debug(trans.json())
                            else:
                                error.error('Failed to create transaction. Status Code received: ' + str(trans.status_code))
            else:
                error.error('Failed to create user. Status Code received: ' + str(user.status_code))
        else:
            error.error('Failed to create application. Status Code received: ' + str(app.status_code))
    else:
        error.error('Failed to create applicant. Status Code received: ' + str(response.status_code))
    debug.debug('')
debug.debug('#####################################################################################################')
