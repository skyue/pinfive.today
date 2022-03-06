#!/usr/local/bin/python3
import requests
import sys

TOKEN = '' # 填写你的token
API_URL = 'https://pinfive.today/get_seq/' + TOKEN
FILE = '/your/backup/file.md' # 填写你的备份文件地址，最好是markdown文件

def backup_text(min_seq, max_seq):
    r = requests.get(API_URL)
    last_seq = r.json()['publish_seq']

    min_seq = min_seq if min_seq else int(last_seq)
    max_seq = max_seq if max_seq else int(last_seq)
    
    if min_seq > max_seq:
        return 'min_seq必须小于max_seq'

    text = ''
    for i in range(min_seq, max_seq+1):
        r = requests.get(API_URL, params={'seq': i})
        json = r.json()
        seq_text = '## {publish_date}（第 {publish_seq} 期）\n\n'.format(publish_date=json['publish_time'][:10], publish_seq=json['publish_seq'])
        for link in json['links']:
            link_text = '''
### {title}
来源：[{domain}]({url}) 标签： {tags}

{note}


'''.format(
            title = link['title'],
            domain = link['url'].split('/')[2],
            url = link['url'],
            note = link['note'],
            tags = '#' + ' #'.join(link['tags'])
        )
            seq_text = seq_text + link_text
        text = text + seq_text
    return text
    

if __name__ == '__main__':
    try:
        min_seq = '0' if len(sys.argv) != 2 else sys.argv[1]
        if not min_seq.isdigit():
            print('\nmin_seq必须是数字\n')
        else:
            min_seq = int(min_seq)
            text = backup_text(min_seq, 0)
            with open(FILE, 'a') as f:
                f.write(text)
            print('\ndone\n')
    except Exception as e:
        print(sys.argv)
        print(e)
