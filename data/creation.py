import pandas as pd

from faker import Faker
from faker.providers.internet import Provider

class CashBoxUserProvider(Provider):

    _username_formats = (
        '{first_letter}{last_name}',
        '{first_name}',
        '{last_name}',
        '{first_name}.{last_name}'
        '{first_name}{random_number}',
        '{last_name}{random_number}',
    )

    def username(self, first_name, last_name):
        formatter = self.random_element(self._username_formats)
        return formatter.format(
            first_name=first_name.lower(),
            last_name=last_name.lower(),
            first_letter=first_name[0].lower(),
            random_number=self.random_number(digits=4)
        )

    def user_dict(self):
        first_name = self.generator.first_name()
        last_name = self.generator.last_name()
        username = self.username(first_name, last_name)
        return {
            username: {
                'first_name': first_name,
                'last_name': last_name,
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