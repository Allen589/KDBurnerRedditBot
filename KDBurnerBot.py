import praw
import config
import time
import os

def bot_login():
	r = praw.Reddit(username = config.username,
			password = config.password,
			client_id = config.client_id,
			client_secret = config.client_secret,
			user_agent = "My comment responder v0.1")

	return r

def run_bot(r, comments_replied_to):

	for comment in r.subreddit('NBA').comments(limit=10):
        # To prevent bot from replying to itself
		if "fuck KD" in comment.body and comment.id not in comments_replied_to and comment.author != r.user.me():
			comment.reply("KD is one of the greatest players of our generation.")
			comments_replied_to.append(comment.id)

			with open ("comments_replied_to.txt", "a") as f:
				f.write(comment.id + "\n")

    # Bot sleeps for 10 seconds
	time.sleep(10)

# To ensure that only one reply is given per comment, stores comments that were replied to in a list
def get_saved_comments():
	if not os.path.isfile("comments_replied_to.txt"):
		comments_replied_to = []
	else:
		with open("comments_replied_to.txt", "r") as f:
			comments_replied_to = f.read()
			comments_replied_to = comments_replied_to.split("\n")
			comments_replied_to = filter(None, comments_replied_to)

	return comments_replied_to

r = bot_login()
comments_replied_to = get_saved_comments()
print comments_replied_to

while True:
	run_bot(r, comments_replied_to)
