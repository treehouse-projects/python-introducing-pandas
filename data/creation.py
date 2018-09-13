import random
import datetime
import pandas as pd
from faker import Faker
from faker.providers.internet import Provider

class CashBoxUserProvider(Provider):
    MIN_DATE = datetime.date(2018, 1, 1)
    MAX_DAYS = (datetime.date.today() - MIN_DATE).days

    _username_formats = (
        '{first_letter}{last_name}',
        '{first_name}',
        '{last_name}',
        '{first_name}.{last_name}'
        '{first_name}{random_number}',
        '{last_name}{random_number}',
    )

    _username_last_safe_formats = tuple(f for f in _username_formats
                                        if 'last_name' not in f)

    def username(self, first_name, last_name):
        if last_name:
            formatter = self.random_element(self._username_formats)
        else:
            formatter = self.random_element(self._username_last_safe_formats)
        return formatter.format(
            first_name=first_name.lower(),
            last_name=last_name.lower(),
            first_letter=first_name[0].lower(),
            random_number=self.random_number(digits=4)
        )

    def signup_date(self):
        return self.MIN_DATE + datetime.timedelta(
            days=random.randint(0, self.MAX_DAYS))

    def email(self, first_name, last_name):
        username = self.username(first_name, last_name)
        domain = self.random_element({
            self.generator.free_email_domain(): 0.9,
            self.generator.domain_name(): 0.1
        })
        return '@'.join([username, domain])

    def email_verified(self):
        return self.random_element({
            True: 0.8,
            False: 0.2
        })

    def last_name_or(self, or_value):
        return self.random_element({
            self.generator.last_name(): 0.9,
            or_value: 0.1
        })

    def user_dict(self):
        first_name = self.generator.first_name()
        # Randomly have last names
        last_name = self.last_name_or("")
        username = self.username(first_name, last_name)
        return {
            username: {
                'first_name': first_name,
                'last_name': last_name,
                'email': self.email(first_name, last_name),
                'email_verified': self.email_verified(),
                'signup_date': self.signup_date(),
                'referral_count': self.random_int(0, 7),
                'balance': (self.random_number(digits=4) / 100)
            }
        }


fake = Faker()
fake.add_provider(CashBoxUserProvider)

# Let's keep our usernames unique
user_row_dict = {}
for _ in range(500):
    # Last one wins
    user_row_dict.update(fake.user_dict())

users = pd.DataFrame.from_dict(user_row_dict, orient='index')

sent_records = []
for _ in range(998):
    sender = users.sample(1).index[0]
    receiver = users.sample(1).index[0]
    amount = fake.random_number(digits=4) / 100
    sent_records.append((sender, receiver, amount))

transactions = pd.DataFrame.from_records(sent_records,
                                         columns=['sender', 'receiver', 'amount'])

# Create requests that appear to be fulfilled
request_records = []
for _ in range(214):
    transaction = transactions.sample(1)
    request_records.append(
        (
            transaction.receiver.iloc[0],
            transaction.sender.iloc[0],
            transaction.amount.iloc[0]
        )
    )

# And now unfulfilled requests
for _ in range(99):
    from_user = users.sample(1).index[0]
    to_user = users.sample(1).index[0]
    amount = fake.random_number(digits=4) / 100
    request_records.append((from_user, to_user, amount))

requests = pd.DataFrame.from_records(request_records,
                                     columns=['from_user', 'to_user', 'amount'])

if __name__ == '__main__':
    users.to_csv('data/users.csv')
    transactions.to_csv('data/transactions.csv')
    requests.to_csv('data/requests.csv')