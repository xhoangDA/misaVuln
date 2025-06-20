import sys
import io
import json

json_data = """[
    {
        "expand": "description,lead,createdAt,createdBy,lastUpdatedAt,lastUpdatedBy,url,projectKeys",
        "self": "http://192.168.11.202:5043/rest/api/2/project/10100",
        "id": "10100",
        "key": "SOD",
        "name": "An ninh thông tin",
        "avatarUrls": {
            "48x48": "http://192.168.11.202:5043/secure/projectavatar?avatarId=10324",
            "24x24": "http://192.168.11.202:5043/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "http://192.168.11.202:5043/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "http://192.168.11.202:5043/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectTypeKey": "software",
        "archived": false
    },
    {
        "expand": "description,lead,createdAt,createdBy,lastUpdatedAt,lastUpdatedBy,url,projectKeys",
        "self": "http://192.168.11.202:5043/rest/api/2/project/10002",
        "id": "10002",
        "key": "EBM",
        "name": "EBM",
        "avatarUrls": {
            "48x48": "http://192.168.11.202:5043/secure/projectavatar?avatarId=10324",
            "24x24": "http://192.168.11.202:5043/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "http://192.168.11.202:5043/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "http://192.168.11.202:5043/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectTypeKey": "software",
        "archived": false
    },
    {
        "expand": "description,lead,createdAt,createdBy,lastUpdatedAt,lastUpdatedBy,url,projectKeys",
        "self": "http://192.168.11.202:5043/rest/api/2/project/10001",
        "id": "10001",
        "key": "HRM",
        "name": "HRM",
        "avatarUrls": {
            "48x48": "http://192.168.11.202:5043/secure/projectavatar?avatarId=10324",
            "24x24": "http://192.168.11.202:5043/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "http://192.168.11.202:5043/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "http://192.168.11.202:5043/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectTypeKey": "software",
        "archived": false
    },
    {
        "expand": "description,lead,createdAt,createdBy,lastUpdatedAt,lastUpdatedBy,url,projectKeys",
        "self": "http://192.168.11.202:5043/rest/api/2/project/10003",
        "id": "10003",
        "key": "LMS",
        "name": "LMS",
        "avatarUrls": {
            "48x48": "http://192.168.11.202:5043/secure/projectavatar?avatarId=10324",
            "24x24": "http://192.168.11.202:5043/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "http://192.168.11.202:5043/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "http://192.168.11.202:5043/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectTypeKey": "software",
        "archived": false
    },
    {
        "expand": "description,lead,createdAt,createdBy,lastUpdatedAt,lastUpdatedBy,url,projectKeys",
        "self": "http://192.168.11.202:5043/rest/api/2/project/10000",
        "id": "10000",
        "key": "UN",
        "name": "Uncategory",
        "avatarUrls": {
            "48x48": "http://192.168.11.202:5043/secure/projectavatar?avatarId=10324",
            "24x24": "http://192.168.11.202:5043/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "http://192.168.11.202:5043/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "http://192.168.11.202:5043/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectTypeKey": "software",
        "archived": false
    }
]
"""
data = json.loads(json_data)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Cách 2: Dùng vòng lặp for thông thường (dễ đọc hơn)
result = []
for item in data:
    extracted = {
        'id': item.get('id'),
        'key': item.get('key'),
        'name': item.get('name')
    }
    result.append(extracted)

with open('jira-projects.json', mode='w', encoding='utf-8') as json_file:
    json.dump(result, json_file, indent=2, ensure_ascii=False)


# # Cách in an toàn với Unicode
# try:
#     print(json.dumps(result, indent=2, ensure_ascii=False))
# except UnicodeEncodeError:
#     # Fallback nếu không in được Unicode
#     print(json.dumps(result, indent=2, ensure_ascii=True))  # Chuyển sang ASCII escape