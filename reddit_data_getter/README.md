# Reddit Data Getter

Uses "PRAW" to obtain reddit data.

[PRAW](https://github.com/praw-dev/praw)  
[PRAW documentation](http://praw.readthedocs.io/en/latest/index.html#)  


## What is saved

### Submissions

Creates a file for first 10 top submissions with time_filter="day".  
For each of these submissions it saves most of top comments up to level 10.

**Subreddits:**

* /r/Bitcoin
* /r/btc
* /r/BTCNews
* /r/CryptoCurrency
* /r/BitcoinMarkets

### Daily discussion

Saved daily discussion submissions for subreddits:

* /r/Bitcoin
* /r/CryptoCurrency