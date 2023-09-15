

import praw
import random
import requests


reddit = praw.Reddit(
    client_id='-kAZ7DdW2t5SVnKr97Duag',
    client_secret='KKs68KzfJEOU7nB18oMLZh2IQYqNdQ',
    user_agent='txuklamemes'
)


subreddit = reddit.subreddit('MemesESP')
random_post = random.choice(list(subreddit.new(limit=100)))  # Limita a los últimos 100 posts para mayor eficiencia


print('Título:', random_post.title)


if random_post.url.endswith(('.jpg', '.jpeg', '.png', '.gif', '.mp4')):
    response = requests.get(random_post.url)
    file_extension = random_post.url.split('.')[-1]
    file_name = f'random_post.{file_extension}'
    with open(file_name, 'wb') as file:
        file.write(response.content)        
else:
    print('El post no contiene una imagen o video.')