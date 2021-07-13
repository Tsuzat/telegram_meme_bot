def get_args_for_meme(msg):
    msg = msg.strip("/meme").strip().split()
    subreddit = None
    method = None

    for content in msg:
        if 'r-' in content:
            subreddit = content.strip('r-').strip()

        if 'm-' in content:
            method = content.strip('m-').strip()

    return subreddit, method


if __name__ == "__main__":
    pass