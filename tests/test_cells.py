import pandas as pd

import os
import unittest


from .helpers import register_test


@register_test('Challenge 1')
class TestDictionary(unittest.TestCase):

    def test_value(self):
        self.assertEquals(1, self.cell.output, "Make sure you return a value")

        
@register_test('Find the top referrers')
class TestReferralCounts(unittest.TestCase):

    def setUp(self):
        self.df = self.cell.output
    
    def test_email_verified(self):
        email_verified_index = self.df['email_verified'] == True
        self.assertEquals(0, len(self.df[~email_verified_index]),
                         "I found some emails that weren't verified, are you sure you limited it by verified only?")
    
    def test_referral_counts(self):
        top_referrer_index = self.df['referral_count'] >= 5
        self.assertEquals(0, len(self.df[~top_referrer_index]),
                         "I found some referral counts that were less than 5. Check your condition.")
    
    def test_total(self):
        self.assertEquals(len(self.df), len(self.df.loc[(self.df.referral_count >= 5) & (self.df.email_verified == True)]), 
                          "Whoops I received a different count than I expected, make sure the last line "
                          "is the entire resulting DataFrame (not just the head)")


@register_test('Update users')
class TestUpdateUsers(unittest.TestCase):

    def setUp(self):
        self.df = self.cell.output

    def test_kim_deal(self):
        # Such a Pixie
        self.assertEquals(
            self.df.at['kimberly', 'last_name'],
            'Deal',
            'Are you sure you updated the last name of kimberly@yahoo.com to "Deal"?'
        )

    def test_jeffrey_with_one_f(self):
        self.assertTrue(
            'jefrey' in self.df.index,
            'Did you rename the username jeffrey to jefrey?'
        )

        self.assertTrue(
            'jeffrey' not in self.df.index,
            'Did you forget to remove the old user name of jeffrey?'
        )


@register_test('Verified email list')
class TestVerifiedEmailList(unittest.TestCase):

    def setUp(self):
        self.df = self.cell.output

    def _get_expected(self):
        users = pd.read_csv(os.path.join('data', 'users.csv'), index_col=0)
        users.dropna(inplace=True)
        return users.loc[
            users.email_verified == True,
            ['first_name', 'last_name', 'email']
        ].sort_values(['last_name', 'first_name'])

    def test_has_na(self):
        self.assertEquals(
            sum(self.df.last_name.isna()),
            0,
            "Looks like there are still rows with last names missing. Drop them!"
        )

    def test_columns(self):
        expected = self._get_expected()
        self.assertEquals(
            len(self.df.columns),
            len(expected.columns),
            "Please only return the following columns: {}".format(
                ', '.join(expected.columns))
        )

    def test_email_verified(self):
        expected = self._get_expected()
        self.assertEquals(
            len(self.df),
            len(expected),
            "Ensure that you are only including users with verified emails"
        )

    def test_title_cased(self):
        self.assertEquals(
            sum(self.df.first_name.str.islower()),
            0,
            "Make sure you title case the first names, there are still some lower case versions"
        )

    def test_sort(self):
        expected = self._get_expected()
        msg = "Check your sort, it should be last name and then first name"
        self.assertEquals(
            self.df.iloc[0, 0],
            expected.iloc[0, 0],
            msg
        )
        self.assertEquals(
            self.df.iloc[-1, 0],
            expected.iloc[-1, 0],
            msg
        )