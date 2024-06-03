import sys
import ins as sninstagram
sys.path.append("..")
import tool

hash_tags = ['beer', 'cocktails', 'whiskey', 'wine', 'scotch', 'trquila', 'rum', 'gin', 'homebrewing',
             'BarBattlestations', 'stopdrinking', 'drunk', 'liquor', 'vodta', 'brandy']

Datas = []
limit = 50

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
            Datas.append(data)
            i += 1
    except BaseException as e:
        print(f'Error: Get {query} data')
        continue

connect = tool.connect_NoSQL('Instagram')
tool.insert_data(connect, Datas)
