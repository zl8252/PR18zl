import praw
import re
import time
import subprocess


def create_submission_file(subreddit, submission, folder_name, file_name):
    subreddit_name = subreddit.display_name
    submission_title = submission.title

    file = open("./../data/reddit/{}/{}/{}".format(subreddit_name, folder_name, file_name), mode='w')

    # saves some meta information
    file.write("File created at: {}\n".format(int(time.time())))
    file.write("Subreddit: {}\n".format(subreddit_name))
    file.write("Submission title: {}\n".format(submission_title))
    file.write("Submission created utc: {}\n".format(int(submission.created_utc)))
    file.write("Submission score: {}\n".format(submission.score))
    file.write("comments: (level\tcreated_utc\tcomment_score\tcomment_body)\n")
    file.write("\n")

    return file


def create_daily_discussion_bitcoin_file(subreddit, submission):
    subreddit_name = subreddit.display_name
    submission_title = submission.title

    file_name = time.strftime("%Y-%m-%d")

    file = open("./../data/reddit/daily_discussion_bitcoin/{}.txt".format(file_name), mode='w')

    # saves some meta information
    file.write("File created at: {}\n".format(int(time.time())))
    file.write("Subreddit: {}\n".format(subreddit_name))
    file.write("Submission title: {}\n".format(submission_title))
    file.write("Submission created utc: {}\n".format(int(submission.created_utc)))
    file.write("Submission score: {}\n".format(submission.score))
    file.write("comments: (level\tcreated_utc\tcomment_score\tcomment_body)\n")
    file.write("\n")

    return file


def create_daily_discussion_cryptoCurrency_file(subreddit, submission):
    subreddit_name = subreddit.display_name
    submission_title = submission.title

    file_name = time.strftime("%Y-%m-%d")

    file = open("./../data/reddit/daily_discussion_cryptocurrency/{}.txt".format(file_name), mode='w')

    # saves some meta information
    file.write("File created at: {}\n".format(int(time.time())))
    file.write("Subreddit: {}\n".format(subreddit_name))
    file.write("Submission title: {}\n".format(submission_title))
    file.write("Submission created utc: {}\n".format(int(submission.created_utc)))
    file.write("Submission score: {}\n".format(submission.score))
    file.write("comments: (level\tcreated_utc\tcomment_score\tcomment_body)\n")
    file.write("\n")

    return file


def save_comment(file, level, comment):
    created_utc = comment.created_utc
    body = comment.body
    score = comment.score

    # removes new lines from body
    body = body.replace("\n", "")
    # converts timstamp to int
    created_utc = int(created_utc)

    line = "{}\t{}\t{}\t{}\n".format(level, created_utc, score, body)

    file.write(line)


def save_comments(file, depth, comments):
    if depth > 10:
        return

    for comment in comments:

        # if comment is not comment (eg. MoreComments) skip it
        if str(type(comment)) != "<class 'praw.models.reddit.comment.Comment'>":
            continue

        save_comment(file, depth, comment)

        sub_comments = comment.replies
        if len(sub_comments) != 0:
            save_comments(file, depth + 1, sub_comments)


def save_submission(subreddit, submission, folder_name, submission_number):
    print("Saving submission")
    print("subreddit: ", subreddit.display_name)
    print("submission: ", submission.title)
    print()

    # creates filename
    file_name = folder_name
    file_name = file_name + "_" + str(submission_number) + ".txt"

    file = create_submission_file(subreddit, submission, folder_name,  file_name)

    top_level_comments = submission.comments

    save_comments(file, 0, top_level_comments)


def save_subreddit(subreddit):
    # creates folder
    folder_name = time.strftime("%Y-%m-%d")

    subprocess.Popen(["mkdir", "./../data/reddit/{}/{}".format(
        subreddit.display_name,
        folder_name)])

    for i, submission in enumerate(subreddit.top(limit=10, time_filter="day")):
        save_submission(subreddit, submission, folder_name, i)


reddit = praw.Reddit(
    client_id='d1zDAi-7oKQNLA',
    client_secret='cbG0scpKkc03-IGAI147zBrWVSk',
    username='zl8252',
    password='7*DlI#JGzb4rBE$p',
    user_agent='podatkovno_rudarjenje',
)

print("User: ", reddit.user.me())
print("Is read only: ", reddit.read_only)
print()

print("Saving data")
print()

# Bitcoin ------
print("/r/bitcoin ----------\n")
subreddit = reddit.subreddit("Bitcoin")
save_subreddit(subreddit)

# Btc -----
print("/r/btc ----------\n")
subreddit = reddit.subreddit("btc")
save_subreddit(subreddit)

# BTC News -----
print("/r/BTCNews ----------\n")
subreddit = reddit.subreddit("BTCNews")
save_subreddit(subreddit)

# CryptoCurrency -----
print("/r/CryptoCurrency ----------\n")
subreddit = reddit.subreddit("CryptoCurrency")
save_subreddit(subreddit)

# BitcoinMarkets -----
print("/r/BitcoinMarkets ----------\n")
subreddit = reddit.subreddit("BitcoinMarkets")
save_subreddit(subreddit)

# Bitcoin daily discussion -----
print("Saving Bitcoin daily discussion")

bitcoin_subreddit = reddit.subreddit("Bitcoin")

# finds the correct submission
bitcoin_daily_discussion_submission = None

for submission in bitcoin_subreddit.hot(limit=20):
    if bool(re.match("Daily Discussion*", submission.title)):
        bitcoin_daily_discussion_submission = submission
        break

if bitcoin_daily_discussion_submission is None:
    print("Could not find Bitcoin daily discussion")
    exit(1)

bitcoin_daily_discussion_file = create_daily_discussion_bitcoin_file(bitcoin_subreddit,
                                                                     bitcoin_daily_discussion_submission)

save_comments(bitcoin_daily_discussion_file, 0, bitcoin_daily_discussion_submission.comments)

print("Saved Bitcoin daily discussion")

# CryptoCurrency daily discussion -----
print("Saving CryptoCurrency daily discussion")

cryptoCurrency_subreddit = reddit.subreddit("CryptoCurrency")

# finds the correct submission
cryptoCurrency_daily_discussion_submission = None

for submission in cryptoCurrency_subreddit.hot(limit=20):
    if bool(re.match("Daily General Discussion*", submission.title)):
        cryptoCurrency_daily_discussion_submission = submission
        break

if cryptoCurrency_daily_discussion_submission is None:
    print("Could not find CryptoCurrency daily discussion")
    exit(1)

cryptoCurrency_daily_discussion_file = create_daily_discussion_cryptoCurrency_file(cryptoCurrency_subreddit,
                                                                                   cryptoCurrency_daily_discussion_submission)

save_comments(cryptoCurrency_daily_discussion_file, 0, cryptoCurrency_daily_discussion_submission.comments)

print("Saved CryptoCurrency daily discussion")
