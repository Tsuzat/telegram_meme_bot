def get_args_for_meme(msg):
    msg = msg.split()
    subreddit = None
    method = None

    for content in msg:
        if 'r-' == content[:2]:
            subreddit = content[2:]

        if 'm-' == content[:2]:
            method = content[2:]

    return subreddit, method


if __name__ == "__main__":
    pass