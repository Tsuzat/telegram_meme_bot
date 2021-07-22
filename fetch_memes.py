import requests
import json
import random
from decouple import config


def get_request(sub_reddit="dankmemes", topic="hot", limit="50"):
    # load header from json
    with open('headers.json', 'r') as f:
        # print("loading headers.json...")
        headers = json.load(f)

    # trying to get request
    req = requests.get(f'https://oauth.reddit.com/r/{sub_reddit}/{topic}', headers=headers, params={'limit': limit})

    if req.ok:  # request ok then return it
        # print("Used stored token")

        if len(req.json()['data']['children']) > 0:
            return req
        else:
            raise Exception("No Related Post found")

    else:  # token expires, let it request for new token

        # print("token expired")

        # note that CLIENT_ID refers to 'personal use script' and SECRET_TOKEN to 'token'
        auth = requests.auth.HTTPBasicAuth(config('client_id'), config('client_secret'))

        # here we pass our login method (password), username, and password
        data = {'grant_type': 'password',
                'username': config('user'),
                'password': config('password'),
                }

        # setup our header info, which gives reddit a brief description of our app
        headers = {'User-Agent': 'memebot'}

        # send our request for an OAuth token
        res = requests.post('https://www.reddit.com/api/v1/access_token',
                            auth=auth, data=data, headers=headers)

        # convert response to JSON and pull access_token value
        TOKEN = res.json()['access_token']

        # add authorization to our headers dictionary
        headers['Authorization'] = f"bearer {TOKEN}"

        with open('headers.json', 'w') as f:
            json.dump(headers, f)

        # print("New headers dumped")

        req = requests.get(f'https://oauth.reddit.com/r/{sub_reddit}/{topic}', headers=headers, params={'limit': limit})

        if req.ok:  # request ok then return it
            print("Used stored token")
            # checking for posts
            if len(req.json()['data']['children']) > 0:
                return req
            else:
                raise Exception("No Related Post found")


def send_meme(subreddit="dankmemes", method="hot"):
    try:  # try to get data
        req = get_request(sub_reddit=subreddit or "dankmemes", topic=method or "hot")
        json_data = req.json()
        posts = json_data['data']['children']
        post = random.choice(posts)
        data = post['data']
        return data

    except Exception as e:  # return None otherwise
        print("EXCEPTION:", e)
        return None


if __name__ == "__main__":
    pass
