# RedditSubmissionLockTimer

This reddit bot wil allow you to lock the submission after given amount of time in the submission flair.

**Supported flair formats:**
- X Minutes
- X Hours

Where X is an integer value. The number needs to be at the front and the unit (Minutes or Hours) must be separated by 
single whitespace character.

Correct Examples:
- 15 Minutes
- 6 Hours
- 24 minutes
- 1 hour

Incorrect Examples (These will not work):
- Minutes 15 (The number comes later and not at front)
- 15Minutes (No space between the number and the unit)
- 7Hors (Typing mistake)
- 0.5 Minutes (Decimal is not supported)

Note: If the bot is stopped all the timers will be canceled. Also, the bot can't pick if the submission flair was 
changed by someone later. Only the flair at the creation of post will be considered.  
## Configuring the Bot
To configure the Bot create a yaml file called config.yaml. Following is the template for the yaml file.
```yaml
reddit_credentials:
  username: ''
  password: ''
  client_id: ''
  client_secret: ''
  user_agent: 'RedditSubmissionLockTimer (by u/is_fake_account)'

subreddit: ''
comment: |
  Hi u/{{author}}, the submission has been locked since the timer has expired. To open the submission again, please
  contact mods.

  Thank you for your patience!
```
Fill in the username, password, client_id, and client_secret accordingly. Same goes for the subreddit. Right now the bot only supports one subreddit. 

You can adjust the comment according to your needs to leave it as it is.

# Prerequisite 
To install all the Prerequisite, install all the packages from requirements.txt using command.

```commandline
pip3 install -r requirements.txt
```

# Help
For help, feel free to reach me out on reddit (u/is_fake_account)