import unittest
import library

NUM_CORPUS = '''
On the 5th of May every year, Mexicans celebrate Cinco de Mayo. This tradition
began in 1845 (the twenty-second anniversary of the Mexican Revolution), and
is the 1st example of a national independence holiday becoming popular in the
Western Hemisphere. (The Fourth of July didn't see regular celebration in the
US until 15-20 years later.) It is celebrated by 77.9% of the population--
trending toward 80.                                                                
'''

class TestCase(unittest.TestCase):

    # Helper function
    def assert_extract(self, text, extractors, *expected):
        actual = [x[1].group(0) for x in library.scan(text, extractors)]
        self.assertEquals(str(actual), str([x for x in expected]))

    # First unit test; prove that if we scan NUM_CORPUS looking for mixed_ordinals,
    # we find "5th" and "1st".
    def test_mixed_ordinals(self):
        self.assert_extract(NUM_CORPUS, library.mixed_ordinals, '5th', '1st')

    # Second unit test; prove that if we look for integers, we find four of them.
    def test_integers(self):
        self.assert_extract(NUM_CORPUS, library.integers, '1845', '15', '20', '80')

    # Third unit test; prove that if we look for integers where there are none, we get no results.
    def test_no_integers(self):
        self.assert_extract("no integers", library.integers)

    # Prove to work for many numbers some wit comma-separated groupings
    def test_integers_with_commas(self):
        self.assert_extract("123,456,789, 324,567 23478", library.integers, '123,456,789', '324,567', '23478')

    # Prove to work for simple iso8601 date
    def test_iso8601_date(self):
        self.assert_extract("I was born on 2015-07-25.", library.dates_iso8601, '2015-07-25')

    # Prove not to match if month is above 12
    def test_iso8601_ivalid_month_not_matched(self):
        self.assert_extract("I was born on 2015-13-25.", library.dates_iso8601)

    # Prove not to match if month is 0
    def test_iso8601_ivalid_month_not_matched2(self):
        self.assert_extract("I was born on 2015-00-25.", library.dates_iso8601)

    # Prove not to match if date is 0
    def test_iso8601_ivalid_date_not_matched2(self):
        self.assert_extract("I was born on 2015-07-00.", library.dates_iso8601)

    # Prove not to match date time with invalid hour (24)
    def test_iso8601_date_time_invalid_hour(self):
        self.assert_extract("I was born on 2018-06-22 24:22:19.123.", library.dates_iso8601)

    # Prove not to match date time with invalid minute (60)
    def test_iso8601_date_time_invalid_minute(self):
        self.assert_extract("I was born on 2018-06-22 22:60:19.123.", library.dates_iso8601)

    # Prove not to match date time with invalid second (60)
    def test_iso8601_date_time_invalid_second(self):
        self.assert_extract("I was born on 2018-06-22 22:22:60.123.", library.dates_iso8601)

    # Prove it work for date with time up to ms precision
    def test_iso8601_date_time_with_ms_precion(self):
        self.assert_extract("I was born on 2018-06-22 18:22:19.123.", library.dates_iso8601, '2018-06-22 18:22:19.123')

    # Prove it work for date with time up to s precision
    def test_iso8601_date_time_with_s_precision(self):
        self.assert_extract("I was born on 2018-06-22 18:22:19.", library.dates_iso8601, '2018-06-22 18:22:19')

    # Prove it work for date with time up to minute precision
    def test_iso8601_date_time_with_min_precision(self):
        self.assert_extract("I was born on 2018-06-22 18:22.", library.dates_iso8601, '2018-06-22 18:22')

    # Prove it work for date with time up to ms precision with Z timezone
    def test_iso8601_date_time_with_ms_precion_zulu(self):
        self.assert_extract("I was born on 2018-06-22 18:22:19.123Z.", library.dates_iso8601, '2018-06-22 18:22:19.123Z')

    # Prove it work for date with time up to s precision with Z timezone
    def test_iso8601_date_time_with_s_precision_zulu(self):
        self.assert_extract("I was born on 2018-06-22 18:22:19Z.", library.dates_iso8601, '2018-06-22 18:22:19Z')

    # Prove it work for date with time up to minute precision with Z timezone
    def test_iso8601_date_time_with_min_precision_zulu(self):
        self.assert_extract("I was born on 2018-06-22 18:22Z.", library.dates_iso8601, '2018-06-22 18:22Z')

    # Prove it work for date with time up to ms precision with 3 letter timezone
    def test_iso8601_date_time_with_ms_precion_letter_timezone(self):
        self.assert_extract("I was born on 2018-06-22 18:22:19.123MDT.", library.dates_iso8601, '2018-06-22 18:22:19.123MDT')

    # Prove it work for date with time up to s precision with 3 letter timezone
    def test_iso8601_date_time_with_s_precision_letter_timezone(self):
        self.assert_extract("I was born on 2018-06-22 18:22:19MDT.", library.dates_iso8601, '2018-06-22 18:22:19MDT')

    # Prove it work for date with time up to minute precision with 3 letter timezone
    def test_iso8601_date_time_with_min_precision_letter_timezone(self):
        self.assert_extract("I was born on 2018-06-22 18:22MDT.", library.dates_iso8601, '2018-06-22 18:22MDT')

    # Prove it work for date with time up to ms precision with offset
    def test_iso8601_date_time_with_ms_precion_offset(self):
        self.assert_extract("I was born on 2018-06-22 18:22:19.123-0800.", library.dates_iso8601, '2018-06-22 18:22:19.123-0800')

    # Prove it work for date with time up to s precision with offset
    def test_iso8601_date_time_with_s_precision_offset(self):
        self.assert_extract("I was born on 2018-06-22 18:22:19-0800.", library.dates_iso8601, '2018-06-22 18:22:19-0800')

    # Prove it work for date with time up to minute precision with offset
    def test_iso8601_date_time_with_min_precision_offset(self):
        self.assert_extract("I was born on 2018-06-22 18:22-0800.", library.dates_iso8601, '2018-06-22 18:22-0800')

    # Prove it work for date with time up to ms precision with T separator
    def test_iso8601_date_time_T_separator_with_ms_precision(self):
        self.assert_extract("I was born on 2018-06-22T18:22:19.123.", library.dates_iso8601, '2018-06-22T18:22:19.123')

    # Prove it work for date with time up to s precision with T separator
    def test_iso8601_date_time_T_separator_with_s_precision(self):
        self.assert_extract("I was born on 2018-06-22T18:22:19.", library.dates_iso8601, '2018-06-22T18:22:19')

    # Prove it work for date with time up to minute precision with T separator
    def test_iso8601_date_time_T_separator_with_min_precision(self):
        self.assert_extract("I was born on 2018-06-22T18:22.", library.dates_iso8601, '2018-06-22T18:22')

    # Prove it work for date with time up to ms precision with T separator and Z timezone
    def test_iso8601_date_time_T_separator_with_ms_precion_zulu(self):
        self.assert_extract("I was born on 2018-06-22T18:22:19.123Z.", library.dates_iso8601, '2018-06-22T18:22:19.123Z')

    # Prove it work for date with time up to s precision with T separator and Z timezone
    def test_iso8601_date_time_T_separator_with_s_precision_zulu(self):
        self.assert_extract("I was born on 2018-06-22T18:22:19Z.", library.dates_iso8601, '2018-06-22T18:22:19Z')

    # Prove it work for date with time up to minute precision with T separator and Z timezone
    def test_iso8601_date_time_T_separator_with_min_precision_zulu(self):
        self.assert_extract("I was born on 2018-06-22T18:22Z.", library.dates_iso8601, '2018-06-22T18:22Z')

    # Prove it work for date with time up to ms precision with T separator and 3 letter timezone
    def test_iso8601_date_time_T_separator_with_ms_precion_letter_timezone(self):
        self.assert_extract("I was born on 2018-06-22T18:22:19.123MDT.", library.dates_iso8601, '2018-06-22T18:22:19.123MDT')

    # Prove it work for date with time up to s precision with T separator and 3 leter timezone
    def test_iso8601_date_time_T_separator_with_s_precision_letter_timezone(self):
        self.assert_extract("I was born on 2018-06-22T18:22:19MDT.", library.dates_iso8601, '2018-06-22T18:22:19MDT')

    # Prove it work for date with time up to minute precision with T separator and 3 leter timezone
    def test_iso8601_date_time_T_separator_with_min_precision_letter_timezone(self):
        self.assert_extract("I was born on 2018-06-22T18:22MDT.", library.dates_iso8601, '2018-06-22T18:22MDT')

    # Prove it work for date with time up to ms precision with T separator and offset
    def test_iso8601_date_time_T_separator_with_ms_precion_offset(self):
        self.assert_extract("I was born on 2018-06-22T18:22:19.123-0800.", library.dates_iso8601, '2018-06-22T18:22:19.123-0800')

    # Prove it work for date with time up to s precision with T separator and offset
    def test_iso8601_date_time_T_separator_with_s_precision_offset(self):
        self.assert_extract("I was born on 2018-06-22T18:22:19-0800.", library.dates_iso8601, '2018-06-22T18:22:19-0800')

    # Prove it work for date with time up to minute precision with T separator and offset
    def test_iso8601_date_time_T_separator_with_min_precision_offset(self):
        self.assert_extract("I was born on 2018-06-22T18:22-0800.", library.dates_iso8601, '2018-06-22T18:22-0800')

    # Prove it work for multiple iso8601 dates in different formats
    def test_iso8601_date_multiple(self):
        self.assert_extract("Many dates: 2018-06-22T18:22-0800, 2018-06-22T18:22:19.123MDT, 2018-06-22 18:22:19, 2017-05-22 bla bla",
                            library.dates_iso8601,
                            "2018-06-22T18:22-0800",
                            "2018-06-22T18:22:19.123MDT",
                            "2018-06-22 18:22:19",
                            "2017-05-22")

    # Prove it works for date with string month
    def test_date_with_string_month(self):
        self.assert_extract('I was born on 25 Jan 2017.', library.dates_string_month, '25 Jan 2017')

    # Prove it works for date with string month with comma after month
    def test_date_with_string_month_with_comma(self):
        self.assert_extract('I was born on 25 Jan, 2017.', library.dates_string_month, '25 Jan, 2017')

    # Prove it works for date with string month for multiple dates in different formats
    def test_date_with_string_month_multiple(self):
        self.assert_extract('I was born on 25 Jan, 2017 and my sister is born on 21 Feb 2013.',
                            library.dates_string_month,
                            '25 Jan, 2017',
                            "21 Feb 2013")


if __name__ == '__main__':
    unittest.main()
