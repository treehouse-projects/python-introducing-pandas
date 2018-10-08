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