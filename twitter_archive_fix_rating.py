import pandas as pd
import os
import requests
import numpy as np


def clean_rating(df, pattern = '(\d+(\.\d+)?\/\d+)'):
    '''
temp1: column 0 extract the full ratings from "(\d+(\.\d+)?\/\d+)"
        column 1 extract the partial pattern from "(\.\d+)?"
        Therefore, we only keep column 0
temp2: still having multiindexing issue, so we unstack it
       and rename the 0, 1, 2 to 'first_match', 'second_match' and 'third_match'
temp3: conditional selecting from temp2, only contains multi-rating data (33 entries),
       which means second match is not missing value.

After investigating the temp3, we find out these are 33 out 2356 tweets
extracting more than one ratings from these texts. Among these multi-rating tweets,
we find out when the first rating is not having denominator of 10, it shows the first extraction is not a rating for a dog,
for example, 7/11 (representing the convinent store) and 24/7 (representing all the time).
So we could make the second match as the valid rating

Firstly, I will find the dataset (temp4) for these twitter texts having extracted more than one 'rating',
but the first match is not having the denominator of 10. Restoring the indexes as 'index_first_match_invalid'.
I went back to temp2 to replace the invalid first match as the valid second match by indinxing 'index_first_match_invalid'.

Secondly, after we exclude the data with indexes of 'index_first_match_invalid' and the rest data in temp3 are the ones having multi valid ratings.
I stored these indexes as 'index_multi_match_valid'.
I will drop them from the temp2 dataset by indexing, since having two or more ratings is violate the rule of one record for one tweet.

temp5: After replacing the first_match as second_match for 'index_first_match_invalid' and dropping the data for 'index_first_match_invalid'
       temp5 contains one rating for each record.

twitter_archive_with_additional_rating: twitter_archive joining the temp5 will make one more column 'rating' on twitter_archive dataset
                                        and dropping the records having the missing value on the new column 'rating', then drop the 342th and 516th records.

Since I manually went through the rating, found some texts did not contain a proper rating, but got extracted from the regex pattern
For example, in the 342th tweet, the text is '@docmisterio account started on 11/15/15'. We could tell 11/15 got extracted to rating, but it actually a date.
Another example, in the 516th tweet, the text is 'Meet Sam. She smiles 24/7 &amp; secretly aspires to be a reindeer. \nKeep Sam smiling by clicking and sharing this link',
which there is no actually rating but '24/7' got extracted. So I drop these texts without anything ratings, but something else got extracted like a date, 24/7, etc...

Finally, I overwrite the 'rating_numerator' and 'rating_denominator' using the column 'rating' we extratced from text, and then drop the column 'rating' and rename to dataset as 'twitter_archive'

    '''
    temp1 = df.text.str.extractall(pattern)

    temp2 = temp1[[0]]
    temp2 = temp2.unstack()
    temp2.columns = temp2.columns.get_level_values(1)
    temp2 = temp2.rename(columns = {0:'first_match',
                               1:'second_match',
                               2: 'third_match'})

    temp3 = temp2[temp2.second_match.notnull()]

    temp4 = temp3[temp3['first_match'].str.split('/', expand = True)[1] != '10'][['second_match']]
    index_first_match_invalid = temp4['second_match'].index

    index_multi_match_valid = list(set(temp3.index) - set(index_first_match_invalid))
    index_multi_match_valid = np.sort(index_multi_match_valid)

    temp5 = temp2.drop(index_multi_match_valid)
    temp5.loc[index_first_match_invalid, 'first_match'] = temp5['second_match']
    temp5 = temp5[['first_match']]
    temp5 = temp5.rename(columns = {'first_match': 'rating'})

    twitter_archive_with_additional_rating = df.join(temp5)
    twitter_archive_with_additional_rating = twitter_archive_with_additional_rating[twitter_archive_with_additional_rating.rating.notnull()]
    twitter_archive_with_additional_rating = twitter_archive_with_additional_rating.drop([342, 516])

    twitter_archive_with_additional_rating['rating_numerator'] = twitter_archive_with_additional_rating['rating'].str.split('/', expand = True)[0].astype(float)
    twitter_archive_with_additional_rating['rating_denominator'] = twitter_archive_with_additional_rating['rating'].str.split('/', expand = True)[1].astype(float)

    twitter_archive = twitter_archive_with_additional_rating.drop('rating', axis = 1)

    return twitter_archive
