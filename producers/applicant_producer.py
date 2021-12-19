import login
import requests

from faker import Faker
from faker.providers import internet, ssn, person, date_time, address, phone_number
from random import randint

fake = Faker('en_US')
fake.add_provider(internet)
fake.add_provider(ssn)
fake.add_provider(person)
fake.add_provider(date_time)
fake.add_provider(address)
fake.add_provider(phone_number)

bearer = login.get_bearer()

genderTypes = ['MALE', 'FEMALE', 'OTHER', 'UNSPECIFIED']
appTypes = ['CHECKING', 'SAVINGS', 'CHECKING_AND_SAVINGS', 'CREDIT_CARD', 'LOAN']
transTypes = ["DEPOSIT", "WITHDRAWAL", "TRANSFER_IN", "TRANSFER_OUT", "PURCHASE", "PAYMENT", "REFUND", "VOID"]
methodTypes = ["ACH", "ATM", "CREDIT_CARD", "DEBIT_CARD", "APP"]

trans_ms = 'http://localhost:8073'
uw_ms = 'http://localhost:8071'
user_ms = 'http://localhost:8070'

num = ''

while True:
    num = input('Enter the number of applicants you would like to add: ')
    if num.isnumeric() and int(num) > 0:
        break
    print('Please enter a valid number greater than zero.')

for i in range(1, int(num) + 1):
    gender = genderTypes[randint(1, 4)-1]
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

    print('Applicant')
    response = requests.post(uw_ms + '/applicants', json=value, headers={'Authorization': bearer})
    print(response.json())

    appType = appTypes[randint(1, 5)-1]

    application = {
        'applicationType': appType,
        'noApplicants': True,
        'applicantIds': [response.json()['id']]
    }

    app = requests.post(uw_ms + '/applications', json=application, headers={'Authorization': bearer})
    print('Application')
    print(app.json())

    userValue = {
        'role': 'member',
        'username': fake.user_name(),
        'password': fake.password(length=15, special_chars=True, digits=True, lower_case=True, upper_case=True),
        'membershipId': app.json()['createdMembers'][0]['membershipId'],
        'lastFourOfSSN': response.json()['socialSecurity'].split('-')[-1]
    }

    print('User')
    # print(userValue)
    user = requests.post(user_ms + '/users/registration', json=userValue)
    print(user.json())

    if 'createdAccounts' in app.json():
        for j in range(0, len(app.json()['createdAccounts'])):
            print('Transactions for Account #' + str(app.json()['createdAccounts'][j]['accountNumber']))
            for k in range(1, 3):
                transValue = None
                merchantTransactions = [1, 5, 6, 7, 8]

                transType = randint(1, 8)
                if transType in merchantTransactions:
                    code = ''
                    for charAt in range(0, randint(5, 8)):
                        code += fake.random_uppercase_letter()
                    name = fake.company()

                    trans = transTypes[transType-1]
                    method = methodTypes[randint(1, 5)-1]

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
                    trans = transTypes[transType-1]
                    method = methodTypes[randint(1, 5)-1]

                    transValue = {
                        'type': trans,
                        'method': method,
                        'amount': randint(20000, 200000),
                        'accountNumber': app.json()['createdAccounts'][j]['accountNumber']
                    }
                # print(transValue)
                transaction = requests.post(trans_ms + '/transactions', json=transValue, headers={'Authorization': bearer})
                print(transaction.json())
    print()
