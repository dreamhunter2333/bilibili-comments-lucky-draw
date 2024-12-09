import base64
import json


def get_all_uid_with_name_comments(path: str):
    res = []
    with open(path, "r", ) as f:
        data = json.load(f)
        entries = data['log']['entries']

        for entry in entries:
            url = entry['request']['url']
            if not url.startswith('https://api.bilibili.com/x/v2/reply/wbi/main'):
                continue
            response = entry['response']
            if not response.get('content', {}).get('text'):
                continue
            text_response = response['content']["text"]
            if response['content'].get('encoding') == 'base64':
                json_response = json.loads(
                    base64.b64decode(text_response).decode('utf-8')
                )
            else:
                json_response = json.loads(text_response)
            for comment in json_response['data']['replies']:
                res.extend(process_comment(comment))
    return list(set(map(tuple, res)))


def process_comment(comment: dict):
    res = [[
        comment['member']['mid'], comment['member']
        ['uname'], comment['content']['message']
    ]]
    # 由于评论的回复可能会有多层，抽奖需求只需要一层
    # for reply in (comment.get('replies') or []):
    #     res.extend(process_comment(reply))
    return res


if __name__ == '__main__':
    res = get_all_uid_with_name_comments('www.bilibili.com.har')
    with open('tmp/res.json', 'w') as f:
        json.dump(res, f, ensure_ascii=False, indent=4)
