import ins as sninstagram
import pandas as pd
import time

hash_tags = ['beer', 'cocktails', 'whiskey', 'wine', 'scotch', 'trquila', 'rum', 'gin', 'homebrewing',
             'BarBattlestations', 'stopdrinking', 'drunk', 'liquor', 'vodta', 'brandy']

ins_s = []
limit = 50

df = pd.DataFrame()
print("*****************START*****************")
for query in hash_tags:
    i = 0
    try:
        print(f'Get {query} data')
        for ins in sninstagram.InstagramHashtagScraper(query).get_items():

            if i == limit:
                break

            ID = ins.id
            date = ins.date
            content = ins.content
            likes = ins.likes
            comments = ins.comments
            url = ins.url
            medium_url = ins.medium.fullUrl
            data = {
                'id': ID,
                'data': date,
                'content': content,
                'hashtag': query,
                'likes': likes,
                'comments': comments,
                'url': url,
                'medium_url': medium_url
            }
            df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
            i += 1
    except Exception as e:
        print(f'Error: Get {query} data')
        pass

df.to_csv(f'Instagram_{time.time()}.csv', encoding='utf_8_sig')
