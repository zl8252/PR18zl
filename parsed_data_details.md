# Parsed Data

## data_days

data_days = [
    "2018.4.1"
    "2018.4.2"
    ...
]

## Subreddit

*_days = [
    [0] day0
    [1] day1
    ...
]

day0 = [
    [0] submission0
    [1] submission1
    ...
]

submission0 = [
       [0]  file_creationTime
       [1] subreddit
       [2] submission_title
       [3] submission_creationTime
       [4] submission_score
       [5] comments
]

comments = [
    [0] comment0
    [1] comment1
    ...
]

comment0 = [
    [0] level
    [1] creationTime
    [2] score
    [3] content
]