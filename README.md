# Twitter Analysis
## by Murong (Sophie) Cui

## Introduction
> The dataset that I will be wrangling (and analyzing and visualizing) is the tweet archive of Twitter user @dog_rates, also known as WeRateDogs. WeRateDogs is a Twitter account that rates people's dogs with a humorous comment about the dog. These ratings almost always have a denominator of 10. The numerators, though? Almost always greater than 10. 11/10, 12/10, 13/10, etc. Why? Because "they're good dogs Brent." WeRateDogs has over 4 million followers and has received international media coverage.

>WeRateDogs downloaded their Twitter archive and sent via email exclusively for me to use in this project. This archive contains basic tweet data (tweet ID, timestamp, text, etc.) for all 5000+ of their tweets as they stood on August 1, 2017. More on this soon.

## Data Source
>1. The WeRateDogs Twitter archive.<br>
 'twitter-archive-enhanced.csv'

> 2. The tweet image predictions, i.e., what breed of dog (or other object, animal, etc.) is present in each tweet according to a neural network. <br>
 url = https://d17h27t6h515a5.cloudfront.net/topher/2017/August/599fd2ad_image-predictions/image-predictions.tsv
> 3. Each tweet's retweet count and favorite ("like") count at minimum, and any additional data you find interesting. Using the tweet IDs in the WeRateDogs Twitter archive, query the Twitter API for each tweet's JSON data using Python's Tweepy library and store each tweet's entire set of JSON data in a file called tweet_json.txt file. Each tweet's JSON data should be written to its own line. Then read this .txt file line by line into a pandas DataFrame with (at minimum) tweet ID, retweet count, and favorite count.

## Data Wrangling
### Enhanced Twitter archive
>The WeRateDogs Twitter \archive contains basic tweet data for all 5000+ of their tweets, but not everything. One column the archive does contain though: each tweet's text, which I used to extract rating, dog name, and dog "stage" (i.e. doggo, floofer, pupper, and puppo) to make this Twitter archive "enhanced." Of the 5000+ tweets, I have filtered for tweets with ratings only (there are 2356).

>I extracted this data programmatically, but I didn't do a very good job. The ratings probably aren't all correct. Same goes for the dog names and probably dog stages (see below for more information on these) too.

>Dog Status:
- doggo:
  - A biger pupper, usually order. This label does not stop a doggo from behaving like a pupper.
  - A pupper that appears to have its life in order. Probably understands taxes and whatnot.
- pupper:
  - A small doggo, usually younger. Can be equally, if not more mature than more doggos.
  - A doggo that is inexperienced, unfamiliar, or in any way unprepared for the responsibilities associated woth being a doggo.
- puppo:
  - A transitional phase between pupper and doggo. Easily understood as the dog equivalent of a teenager.
  - A dog with a mixed bag of both pupper so doggo tendencies.
- blep:
  - A extremely subtle act that occurs without the knowledge of the one who slips. The act includes one's tongue protruding ever so slightly from the mouth, usually just noticeable enough that it attracts the attention it deserves. Can last betwwen three seconds and four days.
- snoot:
  - The nose of a dog. Usually found in places the dog may not fit. The location of the snoot may hint at where the dog's interest lies.
- floof:
  - Any dog really. However, this label is commonly given to dogs with seemingly excess fur. Comical amounts of fur on a dog will certainly earn the dog this generic name.
  - Dog fur. The term holds ture whether the fur is still on the dog, or if it has been shed off.


1. check each column for missing value<br>
 From the heatmap for missing values, we could tell that columns of `in_reply_to_status_id`, `in_reply_to_user_id`, `retweeted_status_id`, `retweeted_status_user_id`, `retweeted_status_timestamp`, and `expanded_urls`. Among the total 2356 rows, the `in_reply_to_status_id` and `in_reply_to_user_id` share the same 2278 missing values since there are both t relatived to the act of in-reply. Similar to retweeting, `retweeted_status_id`,`retweeted_status_user_id` and `retweeted_status_timestam` share the same pattern for 2175 missing values. `expanded_urls` has 59 missing values. Considering that we only want original ratings (no retweets) that have images. I will drop the columns mentioned above.

2. Erroneous numberic variable <br>
  `rating_numerator` and `rating_denominator` are numberic variables.

 The ratings are not all extracted correctly. So I tried to extract the ratings from the text from the pattern `'(\d+\/\d+)'` and these are 33 rows having multiple "ratings". Obvious, not all the multiple extractions are the correct ratings.

   - Scenario 1:  some tweets contain the picture having more than one dogs, so there are multiple ratings for multiple dogs.<br>
 ex: These two pups just met and have instantly bonded. Spectacular scene. Mesmerizing af. 10/10 and 7/10 for blue dog.<br>
     - Solution: I will drop these rows since it will against each row represents one rating.

   - Scenario 2: the pattern `'(\d+\/\d+)'` matches date, location, etc, but not rating. <br>
  ex: After so many requests, this is Bretagne. She was the last surviving `9/11` search dog, and our second ever 14/10. RIP <br>
  ex: This is Darrel. He just robbed a `7/11` and is in a high speed police chase. Was just spotted by the helicopter 10/10 <br>
  ex: This is an Albanian 3 `1/2` legged  Episcopalian. Loves well-polished hardwood flooring. Penis on the collar. 9/10<br>
     - Solution: dropping the wrong extraction, keep the correct dog rating.

3. Columns `doggo`, `floofer`, `pupper`, `puppo`  <br>
  These four columns represents what kind dogstage (doggo, floofer, pupper, puppo). There are two values in doggo column, 'doggo' means the dogstage is doggo, 'None' means the dogstage is not doggo, Similar to doggo column, floofer, pupper and puppo follow the same pattern

      - solution: mapping the 'none' to 0, mapping the stage to 1.

4. Name misextraction<br>
   The column `name` is extracted from the twitter text. Some of the name are misextracted like 'a', 'None', 'the' ....
   - Solution: I find all the name starting lower case letter or None, and set them to missing value (np.nan)

5. timestamp<br>
   The column `timestamp` is object, not timedate datatype.
   I will convert the datetype to timedate.

6. source <br>
  The column of source contains the whole tage of html. For example, the source in the first row is `<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>`. we could extract the address `http://twitter.com/download/iphone`.

### Image predictions
> One more cool thing: I ran every image in the WeRateDogs Twitter archive through a neural network that can classify breeds of dogs*. The results: a table full of image predictions (the top three only) alongside each tweet ID, image URL, and the image number that corresponded to the most confident prediction (numbered 1 to 4 since tweets can have up to four images).

> So for the last row in that table:
 - tweet_id is the last part of the tweet URL after "status/" https://twitter.com/dog_rates/status/889531135344209921
 - p1 is the algorithm's #1 prediction for the image in the tweet → golden retriever
 - p1_conf is how confident the algorithm is in its #1 prediction → 95%
 - p1_dog is whether or not the #1 prediction is a breed of dog → TRUE
 - p2 is the algorithm's second most likely prediction → Labrador retriever
 - p2_conf is how confident the algorithm is in its #2 prediction → 1%
 - p2_dog is whether or not the #2 prediction is a breed of dog → TRUE
etc.

1. Check whether each rows represents one tweet. Check

2. Missing values: there are no missing value

3. names of p1, p2, p3 are a little messy.
4. Duplicated pictures <br>

## Data Analysis
#### Question 1:  What are the top 20 breeds got posted on twitter, and the popularity metrics for the top 20 breeds (avg rating, avg favorite count, avg retweet count)
![Alt text](pic/top20.png?raw=true)
![Alt text](pic/top30.png?raw=true)
![Alt text](pic/top30retweet.png?raw=true)
#### Question 2: Twitter Analyics -- Twitter account development

From the number of tweets posted on the @WeRateDog account, these is a peak around end of 2015, then the posts decrease next several months, and then gets relatively stational post number after April 2016. <br>

For number of favorites, we could tell the favorites increase from Jan 2016 to June 2017, and get a shape drop after June 2017.<br>
![Alt text](pic/q2.1.png?raw=true)
![Alt text](pic/q2.2.png?raw=true)
![Alt text](pic/q2.3.png?raw=true)
#### Q3: What are popular names people would get to their dog ?

The most common name people gave to their dogs are Copper, Charlie and Oliver, Then Tucker, lucy, Penny are the second tier.
![Alt text](pic/top10name.png?raw=true)
