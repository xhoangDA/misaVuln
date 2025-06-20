import sys
import io
import json

json_data = """[
    {
        "self": "http://192.168.11.202:5043/rest/api/2/user?username=00006",
        "key": "JIRAUSER10118",
        "name": "00006",
        "emailAddress": "thuyen.le@vnresource.vn",
        "avatarUrls": {
            "48x48": "https://www.gravatar.com/avatar/ea926463a19a7c619a2bea5de0a4175e?d=mm&s=48",
            "24x24": "https://www.gravatar.com/avatar/ea926463a19a7c619a2bea5de0a4175e?d=mm&s=24",
            "16x16": "https://www.gravatar.com/avatar/ea926463a19a7c619a2bea5de0a4175e?d=mm&s=16",
            "32x32": "https://www.gravatar.com/avatar/ea926463a19a7c619a2bea5de0a4175e?d=mm&s=32"
        },
        "displayName": "Lê Xuân Thuyên",
        "active": true,
        "deleted": false,
        "timeZone": "Asia/Ho_Chi_Minh",
        "locale": "en_US"
    },
    {
        "self": "http://192.168.11.202:5043/rest/api/2/user?username=00038",
        "key": "JIRAUSER10120",
        "name": "00038",
        "emailAddress": "bao.tran@vnresource.vn",
        "avatarUrls": {
            "48x48": "https://www.gravatar.com/avatar/75ed07b82efef9584f6ef48c684af6c8?d=mm&s=48",
            "24x24": "https://www.gravatar.com/avatar/75ed07b82efef9584f6ef48c684af6c8?d=mm&s=24",
            "16x16": "https://www.gravatar.com/avatar/75ed07b82efef9584f6ef48c684af6c8?d=mm&s=16",
            "32x32": "https://www.gravatar.com/avatar/75ed07b82efef9584f6ef48c684af6c8?d=mm&s=32"
        },
        "displayName": "Trần Quốc Bảo",
        "active": true,
        "deleted": false,
        "timeZone": "Asia/Ho_Chi_Minh",
        "locale": "en_US"
    },
    {
        "self": "http://192.168.11.202:5043/rest/api/2/user?username=00084",
        "key": "JIRAUSER10116",
        "name": "00084",
        "emailAddress": "hien.pham@vnresource.vn",
        "avatarUrls": {
            "48x48": "https://www.gravatar.com/avatar/d1376c9230b2ede0c070492c39337204?d=mm&s=48",
            "24x24": "https://www.gravatar.com/avatar/d1376c9230b2ede0c070492c39337204?d=mm&s=24",
            "16x16": "https://www.gravatar.com/avatar/d1376c9230b2ede0c070492c39337204?d=mm&s=16",
            "32x32": "https://www.gravatar.com/avatar/d1376c9230b2ede0c070492c39337204?d=mm&s=32"
        },
        "displayName": "Phạm Văn Hiển",
        "active": true,
        "deleted": false,
        "timeZone": "Asia/Ho_Chi_Minh",
        "locale": "en_US"
    },
    {
        "self": "http://192.168.11.202:5043/rest/api/2/user?username=00090",
        "key": "JIRAUSER10401",
        "name": "00090",
        "emailAddress": "hung.le@vnresource.vn",
        "avatarUrls": {
            "48x48": "https://www.gravatar.com/avatar/10902f47a2ffe9cd7aaebb4c2ab60bee?d=mm&s=48",
            "24x24": "https://www.gravatar.com/avatar/10902f47a2ffe9cd7aaebb4c2ab60bee?d=mm&s=24",
            "16x16": "https://www.gravatar.com/avatar/10902f47a2ffe9cd7aaebb4c2ab60bee?d=mm&s=16",
            "32x32": "https://www.gravatar.com/avatar/10902f47a2ffe9cd7aaebb4c2ab60bee?d=mm&s=32"
        },
        "displayName": "Hùng Lê",
        "active": true,
        "deleted": false,
        "timeZone": "Asia/Ho_Chi_Minh",
        "locale": "en_US"
    },
    {
        "self": "http://192.168.11.202:5043/rest/api/2/user?username=00093",
        "key": "JIRAUSER10117",
        "name": "00093",
        "emailAddress": "hoang.huynh@vnresource.vn",
        "avatarUrls": {
            "48x48": "https://www.gravatar.com/avatar/ce5ef35bf555ee5b16c75e74fae91acb?d=mm&s=48",
            "24x24": "https://www.gravatar.com/avatar/ce5ef35bf555ee5b16c75e74fae91acb?d=mm&s=24",
            "16x16": "https://www.gravatar.com/avatar/ce5ef35bf555ee5b16c75e74fae91acb?d=mm&s=16",
            "32x32": "https://www.gravatar.com/avatar/ce5ef35bf555ee5b16c75e74fae91acb?d=mm&s=32"
        },
        "displayName": "Huỳnh Tấn Hoàng",
        "active": true,
        "deleted": false,
        "timeZone": "Asia/Ho_Chi_Minh",
        "locale": "en_US"
    },
    {
        "self": "http://192.168.11.202:5043/rest/api/2/user?username=00112",
        "key": "JIRAUSER10214",
        "name": "00112",
        "emailAddress": "phat.le@vnresource.net",
        "avatarUrls": {
            "48x48": "http://192.168.11.202:5043/secure/useravatar?avatarId=10503",
            "24x24": "http://192.168.11.202:5043/secure/useravatar?size=small&avatarId=10503",
            "16x16": "http://192.168.11.202:5043/secure/useravatar?size=xsmall&avatarId=10503",
            "32x32": "http://192.168.11.202:5043/secure/useravatar?size=medium&avatarId=10503"
        },
        "displayName": "Lê Minh Phát",
        "active": true,
        "deleted": false,
        "timeZone": "Asia/Ho_Chi_Minh",
        "locale": "en_US"
    },
    {
        "self": "http://192.168.11.202:5043/rest/api/2/user?username=00132",
        "key": "JIRAUSER10104",
        "name": "00132",
        "emailAddress": "na.trinh@vnresource.vn",
        "avatarUrls": {
            "48x48": "https://www.gravatar.com/avatar/913f7dea3e8f490d04fe2a0f09267190?d=mm&s=48",
            "24x24": "https://www.gravatar.com/avatar/913f7dea3e8f490d04fe2a0f09267190?d=mm&s=24",
            "16x16": "https://www.gravatar.com/avatar/913f7dea3e8f490d04fe2a0f09267190?d=mm&s=16",
            "32x32": "https://www.gravatar.com/avatar/913f7dea3e8f490d04fe2a0f09267190?d=mm&s=32"
        },
        "displayName": "Trịnh Thị Ly Na",
        "active": true,
        "deleted": false,
        "timeZone": "Asia/Ho_Chi_Minh",
        "locale": "en_US"
    },
    {
        "self": "http://192.168.11.202:5043/rest/api/2/user?username=00135",
        "key": "JIRAUSER10212",
        "name": "00135",
        "emailAddress": "toan.vo@vnresource.vn",
        "avatarUrls": {
            "48x48": "https://www.gravatar.com/avatar/b719e4df763558c21c5ffd730c35f8fa?d=mm&s=48",
            "24x24": "https://www.gravatar.com/avatar/b719e4df763558c21c5ffd730c35f8fa?d=mm&s=24",
            "16x16": "https://www.gravatar.com/avatar/b719e4df763558c21c5ffd730c35f8fa?d=mm&s=16",
            "32x32": "https://www.gravatar.com/avatar/b719e4df763558c21c5ffd730c35f8fa?d=mm&s=32"
        },
        "displayName": "Võ Đăng Toàn",
        "active": true,
        "deleted": false,
        "timeZone": "Asia/Ho_Chi_Minh",
        "locale": "en_US"
    },
    {
        "self": "http://192.168.11.202:5043/rest/api/2/user?username=00200",
        "key": "JIRAUSER10119",
        "name": "00200",
        "emailAddress": "anh.tran@vnresource.vn",
        "avatarUrls": {
            "48x48": "https://www.gravatar.com/avatar/fb2d1b722cb0ee39988e67f996d3532d?d=mm&s=48",
            "24x24": "https://www.gravatar.com/avatar/fb2d1b722cb0ee39988e67f996d3532d?d=mm&s=24",
            "16x16": "https://www.gravatar.com/avatar/fb2d1b722cb0ee39988e67f996d3532d?d=mm&s=16",
            "32x32": "https://www.gravatar.com/avatar/fb2d1b722cb0ee39988e67f996d3532d?d=mm&s=32"
        },
        "displayName": "Trần Thế Anh",
        "active": true,
        "deleted": false,
        "timeZone": "Asia/Ho_Chi_Minh",
        "locale": "en_US"
    },
    {
        "self": "http://192.168.11.202:5043/rest/api/2/user?username=00201",
        "key": "JIRAUSER10102",
        "name": "00201",
        "emailAddress": "dung.hoang@vnresource.vn",
        "avatarUrls": {
            "48x48": "https://www.gravatar.com/avatar/d669a3a0d11bfd199cadb75e0f8d3fb4?d=mm&s=48",
            "24x24": "https://www.gravatar.com/avatar/d669a3a0d11bfd199cadb75e0f8d3fb4?d=mm&s=24",
            "16x16": "https://www.gravatar.com/avatar/d669a3a0d11bfd199cadb75e0f8d3fb4?d=mm&s=16",
            "32x32": "https://www.gravatar.com/avatar/d669a3a0d11bfd199cadb75e0f8d3fb4?d=mm&s=32"
        },
        "displayName": "Hoàng Văn Dũng",
        "active": true,
        "deleted": false,
        "timeZone": "Asia/Ho_Chi_Minh",
        "locale": "en_US"
    },
    {
        "self": "http://192.168.11.202:5043/rest/api/2/user?username=00202",
        "key": "JIRAUSER10400",
        "name": "00202",
        "emailAddress": "tuan.pham@vnresource.vn",
        "avatarUrls": {
            "48x48": "https://www.gravatar.com/avatar/8340077750f2abe473835de6d90c6c6b?d=mm&s=48",
            "24x24": "https://www.gravatar.com/avatar/8340077750f2abe473835de6d90c6c6b?d=mm&s=24",
            "16x16": "https://www.gravatar.com/avatar/8340077750f2abe473835de6d90c6c6b?d=mm&s=16",
            "32x32": "https://www.gravatar.com/avatar/8340077750f2abe473835de6d90c6c6b?d=mm&s=32"
        },
        "displayName": "Tuấn Phạm",
        "active": true,
        "deleted": false,
        "timeZone": "Asia/Ho_Chi_Minh",
        "locale": "en_US"
    },
    {
        "self": "http://192.168.11.202:5043/rest/api/2/user?username=00208",
        "key": "JIRAUSER10404",
        "name": "00208",
        "emailAddress": "long.tran@vnresource.vn",
        "avatarUrls": {
            "48x48": "https://www.gravatar.com/avatar/6a3163b113b8b825cdcec8f866f9bdec?d=mm&s=48",
            "24x24": "https://www.gravatar.com/avatar/6a3163b113b8b825cdcec8f866f9bdec?d=mm&s=24",
            "16x16": "https://www.gravatar.com/avatar/6a3163b113b8b825cdcec8f866f9bdec?d=mm&s=16",
            "32x32": "https://www.gravatar.com/avatar/6a3163b113b8b825cdcec8f866f9bdec?d=mm&s=32"
        },
        "displayName": "Long Trần",
        "active": true,
        "deleted": false,
        "timeZone": "Asia/Ho_Chi_Minh",
        "locale": "en_US"
    },
    {
        "self": "http://192.168.11.202:5043/rest/api/2/user?username=00262",
        "key": "JIRAUSER10405",
        "name": "00262",
        "emailAddress": "anh.nguyendoan@vnresource.vn",
        "avatarUrls": {
            "48x48": "https://www.gravatar.com/avatar/06f42e0ed92d2e5d952a24f61b03c9bb?d=mm&s=48",
            "24x24": "https://www.gravatar.com/avatar/06f42e0ed92d2e5d952a24f61b03c9bb?d=mm&s=24",
            "16x16": "https://www.gravatar.com/avatar/06f42e0ed92d2e5d952a24f61b03c9bb?d=mm&s=16",
            "32x32": "https://www.gravatar.com/avatar/06f42e0ed92d2e5d952a24f61b03c9bb?d=mm&s=32"
        },
        "displayName": "Anh Nguyễn",
        "active": true,
        "deleted": false,
        "timeZone": "Asia/Ho_Chi_Minh",
        "locale": "en_US"
    },
    {
        "self": "http://192.168.11.202:5043/rest/api/2/user?username=00266",
        "key": "JIRAUSER10403",
        "name": "00266",
        "emailAddress": "huu.doan@vnresource.vn",
        "avatarUrls": {
            "48x48": "https://www.gravatar.com/avatar/68b59b8c47f2e98ff0f3151f75b6f3f2?d=mm&s=48",
            "24x24": "https://www.gravatar.com/avatar/68b59b8c47f2e98ff0f3151f75b6f3f2?d=mm&s=24",
            "16x16": "https://www.gravatar.com/avatar/68b59b8c47f2e98ff0f3151f75b6f3f2?d=mm&s=16",
            "32x32": "https://www.gravatar.com/avatar/68b59b8c47f2e98ff0f3151f75b6f3f2?d=mm&s=32"
        },
        "displayName": "Hữu Đoàn",
        "active": true,
        "deleted": false,
        "timeZone": "Asia/Ho_Chi_Minh",
        "locale": "en_US"
    },
    {
        "self": "http://192.168.11.202:5043/rest/api/2/user?username=00311",
        "key": "JIRAUSER10501",
        "name": "00311",
        "emailAddress": "trung.tong@vnresource.vn",
        "avatarUrls": {
            "48x48": "https://www.gravatar.com/avatar/be7ce6d3f6588882cf1d04de3865e589?d=mm&s=48",
            "24x24": "https://www.gravatar.com/avatar/be7ce6d3f6588882cf1d04de3865e589?d=mm&s=24",
            "16x16": "https://www.gravatar.com/avatar/be7ce6d3f6588882cf1d04de3865e589?d=mm&s=16",
            "32x32": "https://www.gravatar.com/avatar/be7ce6d3f6588882cf1d04de3865e589?d=mm&s=32"
        },
        "displayName": "Tống Thanh Trung",
        "active": true,
        "deleted": false,
        "timeZone": "Asia/Ho_Chi_Minh",
        "locale": "en_US"
    },
    {
        "self": "http://192.168.11.202:5043/rest/api/2/user?username=00318",
        "key": "JIRAUSER10208",
        "name": "00318",
        "emailAddress": "tung.tran@vnresource.net",
        "avatarUrls": {
            "48x48": "https://www.gravatar.com/avatar/d340cb67d6dfe9e7b075230a9cc2dfaf?d=mm&s=48",
            "24x24": "https://www.gravatar.com/avatar/d340cb67d6dfe9e7b075230a9cc2dfaf?d=mm&s=24",
            "16x16": "https://www.gravatar.com/avatar/d340cb67d6dfe9e7b075230a9cc2dfaf?d=mm&s=16",
            "32x32": "https://www.gravatar.com/avatar/d340cb67d6dfe9e7b075230a9cc2dfaf?d=mm&s=32"
        },
        "displayName": "Trần Duy Tùng",
        "active": true,
        "deleted": false,
        "timeZone": "Asia/Ho_Chi_Minh",
        "locale": "en_US"
    },
    {
        "self": "http://192.168.11.202:5043/rest/api/2/user?username=00330",
        "key": "JIRAUSER10101",
        "name": "00330",
        "emailAddress": "linh.tran@vnresource.vn",
        "avatarUrls": {
            "48x48": "http://192.168.11.202:5043/secure/useravatar?avatarId=10346",
            "24x24": "http://192.168.11.202:5043/secure/useravatar?size=small&avatarId=10346",
            "16x16": "http://192.168.11.202:5043/secure/useravatar?size=xsmall&avatarId=10346",
            "32x32": "http://192.168.11.202:5043/secure/useravatar?size=medium&avatarId=10346"
        },
        "displayName": "Trần Nhật Vũ Linh",
        "active": true,
        "deleted": false,
        "timeZone": "Asia/Ho_Chi_Minh",
        "locale": "en_US"
    },
    {
        "self": "http://192.168.11.202:5043/rest/api/2/user?username=00393",
        "key": "JIRAUSER10103",
        "name": "00393",
        "emailAddress": "tam.huynh@vnresource.vn",
        "avatarUrls": {
            "48x48": "http://192.168.11.202:5043/secure/useravatar?avatarId=10352",
            "24x24": "http://192.168.11.202:5043/secure/useravatar?size=small&avatarId=10352",
            "16x16": "http://192.168.11.202:5043/secure/useravatar?size=xsmall&avatarId=10352",
            "32x32": "http://192.168.11.202:5043/secure/useravatar?size=medium&avatarId=10352"
        },
        "displayName": "Huỳnh Đức Nhân Tâm",
        "active": true,
        "deleted": false,
        "timeZone": "Asia/Ho_Chi_Minh",
        "locale": "en_US"
    },
    {
        "self": "http://192.168.11.202:5043/rest/api/2/user?username=00420",
        "key": "JIRAUSER10108",
        "name": "00420",
        "emailAddress": "linh.doan@vnresource.net",
        "avatarUrls": {
            "48x48": "https://www.gravatar.com/avatar/3420b0bba76ae416fc277534119a182e?d=mm&s=48",
            "24x24": "https://www.gravatar.com/avatar/3420b0bba76ae416fc277534119a182e?d=mm&s=24",
            "16x16": "https://www.gravatar.com/avatar/3420b0bba76ae416fc277534119a182e?d=mm&s=16",
            "32x32": "https://www.gravatar.com/avatar/3420b0bba76ae416fc277534119a182e?d=mm&s=32"
        },
        "displayName": "Doãn Diệp Linh",
        "active": true,
        "deleted": false,
        "timeZone": "Asia/Ho_Chi_Minh",
        "locale": "en_US"
    },
    {
        "self": "http://192.168.11.202:5043/rest/api/2/user?username=00435",
        "key": "JIRAUSER10215",
        "name": "00435",
        "emailAddress": "vu.lethanh@vnresource.net",
        "avatarUrls": {
            "48x48": "https://www.gravatar.com/avatar/fc158a1a9f346359b3a466e2cbd81b1f?d=mm&s=48",
            "24x24": "https://www.gravatar.com/avatar/fc158a1a9f346359b3a466e2cbd81b1f?d=mm&s=24",
            "16x16": "https://www.gravatar.com/avatar/fc158a1a9f346359b3a466e2cbd81b1f?d=mm&s=16",
            "32x32": "https://www.gravatar.com/avatar/fc158a1a9f346359b3a466e2cbd81b1f?d=mm&s=32"
        },
        "displayName": "Lê Thanh Vũ",
        "active": true,
        "deleted": false,
        "timeZone": "Asia/Ho_Chi_Minh",
        "locale": "en_US"
    },
    {
        "self": "http://192.168.11.202:5043/rest/api/2/user?username=00437",
        "key": "JIRAUSER10109",
        "name": "00437",
        "emailAddress": "thu.phan@vnresource.net",
        "avatarUrls": {
            "48x48": "https://www.gravatar.com/avatar/a9821630d172ab40d9b5ce91352e80b2?d=mm&s=48",
            "24x24": "https://www.gravatar.com/avatar/a9821630d172ab40d9b5ce91352e80b2?d=mm&s=24",
            "16x16": "https://www.gravatar.com/avatar/a9821630d172ab40d9b5ce91352e80b2?d=mm&s=16",
            "32x32": "https://www.gravatar.com/avatar/a9821630d172ab40d9b5ce91352e80b2?d=mm&s=32"
        },
        "displayName": "Phan Thị Ngọc Thu",
        "active": true,
        "deleted": false,
        "timeZone": "Asia/Ho_Chi_Minh",
        "locale": "en_US"
    },
    {
        "self": "http://192.168.11.202:5043/rest/api/2/user?username=00438",
        "key": "JIRAUSER10406",
        "name": "00438",
        "emailAddress": "hiep.tran@vnresource.vn",
        "avatarUrls": {
            "48x48": "https://www.gravatar.com/avatar/41e18ee9b784aff3c6fd26f8429e8fa3?d=mm&s=48",
            "24x24": "https://www.gravatar.com/avatar/41e18ee9b784aff3c6fd26f8429e8fa3?d=mm&s=24",
            "16x16": "https://www.gravatar.com/avatar/41e18ee9b784aff3c6fd26f8429e8fa3?d=mm&s=16",
            "32x32": "https://www.gravatar.com/avatar/41e18ee9b784aff3c6fd26f8429e8fa3?d=mm&s=32"
        },
        "displayName": "Hiệp Trần",
        "active": true,
        "deleted": false,
        "timeZone": "Asia/Ho_Chi_Minh",
        "locale": "en_US"
    },
    {
        "self": "http://192.168.11.202:5043/rest/api/2/user?username=00477",
        "key": "JIRAUSER10115",
        "name": "00477",
        "emailAddress": "binh.le@vnresource.vn",
        "avatarUrls": {
            "48x48": "http://192.168.11.202:5043/secure/useravatar?avatarId=10340",
            "24x24": "http://192.168.11.202:5043/secure/useravatar?size=small&avatarId=10340",
            "16x16": "http://192.168.11.202:5043/secure/useravatar?size=xsmall&avatarId=10340",
            "32x32": "http://192.168.11.202:5043/secure/useravatar?size=medium&avatarId=10340"
        },
        "displayName": "Lê Thị Thanh Bình",
        "active": true,
        "deleted": false,
        "timeZone": "Asia/Ho_Chi_Minh",
        "locale": "en_US"
    },
    {
        "self": "http://192.168.11.202:5043/rest/api/2/user?username=00490",
        "key": "JIRAUSER10503",
        "name": "00490",
        "emailAddress": "hieu.tran@vnresource.org",
        "avatarUrls": {
            "48x48": "https://www.gravatar.com/avatar/12f6300210216b1f7f23d88c3d4ae5d9?d=mm&s=48",
            "24x24": "https://www.gravatar.com/avatar/12f6300210216b1f7f23d88c3d4ae5d9?d=mm&s=24",
            "16x16": "https://www.gravatar.com/avatar/12f6300210216b1f7f23d88c3d4ae5d9?d=mm&s=16",
            "32x32": "https://www.gravatar.com/avatar/12f6300210216b1f7f23d88c3d4ae5d9?d=mm&s=32"
        },
        "displayName": "Trần Công Hiếu ",
        "active": true,
        "deleted": false,
        "timeZone": "Asia/Ho_Chi_Minh",
        "locale": "en_US"
    },
    {
        "self": "http://192.168.11.202:5043/rest/api/2/user?username=00492",
        "key": "JIRAUSER10210",
        "name": "00492",
        "emailAddress": "hien.dinh@vnresource.org",
        "avatarUrls": {
            "48x48": "https://www.gravatar.com/avatar/ef1126bc908a5448126c2df51980c655?d=mm&s=48",
            "24x24": "https://www.gravatar.com/avatar/ef1126bc908a5448126c2df51980c655?d=mm&s=24",
            "16x16": "https://www.gravatar.com/avatar/ef1126bc908a5448126c2df51980c655?d=mm&s=16",
            "32x32": "https://www.gravatar.com/avatar/ef1126bc908a5448126c2df51980c655?d=mm&s=32"
        },
        "displayName": "Đinh Thiện Minh Hiền",
        "active": true,
        "deleted": false,
        "timeZone": "Asia/Ho_Chi_Minh",
        "locale": "en_US"
    },
    {
        "self": "http://192.168.11.202:5043/rest/api/2/user?username=00508",
        "key": "JIRAUSER10402",
        "name": "00508",
        "emailAddress": "thai.bui@vnresource.vn",
        "avatarUrls": {
            "48x48": "https://www.gravatar.com/avatar/97e3b7c91ade8149223ad7445254d845?d=mm&s=48",
            "24x24": "https://www.gravatar.com/avatar/97e3b7c91ade8149223ad7445254d845?d=mm&s=24",
            "16x16": "https://www.gravatar.com/avatar/97e3b7c91ade8149223ad7445254d845?d=mm&s=16",
            "32x32": "https://www.gravatar.com/avatar/97e3b7c91ade8149223ad7445254d845?d=mm&s=32"
        },
        "displayName": "Thái Bùi",
        "active": true,
        "deleted": false,
        "timeZone": "Asia/Ho_Chi_Minh",
        "locale": "en_US"
    },
    {
        "self": "http://192.168.11.202:5043/rest/api/2/user?username=00536",
        "key": "JIRAUSER10209",
        "name": "00536",
        "emailAddress": "sang.do@vnresource.org",
        "avatarUrls": {
            "48x48": "https://www.gravatar.com/avatar/6231fa5f329c28de5cd72dce21716652?d=mm&s=48",
            "24x24": "https://www.gravatar.com/avatar/6231fa5f329c28de5cd72dce21716652?d=mm&s=24",
            "16x16": "https://www.gravatar.com/avatar/6231fa5f329c28de5cd72dce21716652?d=mm&s=16",
            "32x32": "https://www.gravatar.com/avatar/6231fa5f329c28de5cd72dce21716652?d=mm&s=32"
        },
        "displayName": "Đỗ Trường Sang",
        "active": true,
        "deleted": false,
        "timeZone": "Asia/Ho_Chi_Minh",
        "locale": "en_US"
    },
    {
        "self": "http://192.168.11.202:5043/rest/api/2/user?username=00546",
        "key": "JIRAUSER10700",
        "name": "00546",
        "emailAddress": "thuong.hoang@vnresource.vn",
        "avatarUrls": {
            "48x48": "http://192.168.11.202:5043/secure/useravatar?avatarId=10344",
            "24x24": "http://192.168.11.202:5043/secure/useravatar?size=small&avatarId=10344",
            "16x16": "http://192.168.11.202:5043/secure/useravatar?size=xsmall&avatarId=10344",
            "32x32": "http://192.168.11.202:5043/secure/useravatar?size=medium&avatarId=10344"
        },
        "displayName": "Hoàng Văn Thường",
        "active": true,
        "deleted": false,
        "timeZone": "Asia/Ho_Chi_Minh",
        "locale": "en_US"
    },
    {
        "self": "http://192.168.11.202:5043/rest/api/2/user?username=00570",
        "key": "JIRAUSER10507",
        "name": "00570",
        "emailAddress": "minh.nguyendat@vnresource.org",
        "avatarUrls": {
            "48x48": "https://www.gravatar.com/avatar/d57c4add6a697042986b0223c97712f3?d=mm&s=48",
            "24x24": "https://www.gravatar.com/avatar/d57c4add6a697042986b0223c97712f3?d=mm&s=24",
            "16x16": "https://www.gravatar.com/avatar/d57c4add6a697042986b0223c97712f3?d=mm&s=16",
            "32x32": "https://www.gravatar.com/avatar/d57c4add6a697042986b0223c97712f3?d=mm&s=32"
        },
        "displayName": "Nguyễn Đạt Minh",
        "active": true,
        "deleted": false,
        "timeZone": "Asia/Ho_Chi_Minh",
        "locale": "en_US"
    },
    {
        "self": "http://192.168.11.202:5043/rest/api/2/user?username=00597",
        "key": "JIRAUSER10508",
        "name": "00597",
        "emailAddress": "hac.tran@vnresource.vn",
        "avatarUrls": {
            "48x48": "http://192.168.11.202:5043/secure/useravatar?avatarId=10336",
            "24x24": "http://192.168.11.202:5043/secure/useravatar?size=small&avatarId=10336",
            "16x16": "http://192.168.11.202:5043/secure/useravatar?size=xsmall&avatarId=10336",
            "32x32": "http://192.168.11.202:5043/secure/useravatar?size=medium&avatarId=10336"
        },
        "displayName": "Trần Phước Hạc",
        "active": true,
        "deleted": false,
        "timeZone": "Asia/Ho_Chi_Minh",
        "locale": "en_US"
    },
    {
        "self": "http://192.168.11.202:5043/rest/api/2/user?username=00608",
        "key": "JIRAUSER10114",
        "name": "00608",
        "emailAddress": "dung.tran@vnresource.org",
        "avatarUrls": {
            "48x48": "https://www.gravatar.com/avatar/df84701676826e590ef4475dc3d60674?d=mm&s=48",
            "24x24": "https://www.gravatar.com/avatar/df84701676826e590ef4475dc3d60674?d=mm&s=24",
            "16x16": "https://www.gravatar.com/avatar/df84701676826e590ef4475dc3d60674?d=mm&s=16",
            "32x32": "https://www.gravatar.com/avatar/df84701676826e590ef4475dc3d60674?d=mm&s=32"
        },
        "displayName": "Trần Mạnh Dũng",
        "active": true,
        "deleted": false,
        "timeZone": "Asia/Ho_Chi_Minh",
        "locale": "en_US"
    },
    {
        "self": "http://192.168.11.202:5043/rest/api/2/user?username=00624",
        "key": "JIRAUSER10111",
        "name": "00624",
        "emailAddress": "duy.ho@vnresource.net",
        "avatarUrls": {
            "48x48": "http://192.168.11.202:5043/secure/useravatar?avatarId=10341",
            "24x24": "http://192.168.11.202:5043/secure/useravatar?size=small&avatarId=10341",
            "16x16": "http://192.168.11.202:5043/secure/useravatar?size=xsmall&avatarId=10341",
            "32x32": "http://192.168.11.202:5043/secure/useravatar?size=medium&avatarId=10341"
        },
        "displayName": "Hồ Thanh Duy",
        "active": true,
        "deleted": false,
        "timeZone": "Asia/Ho_Chi_Minh",
        "locale": "en_UK"
    },
    {
        "self": "http://192.168.11.202:5043/rest/api/2/user?username=00652",
        "key": "JIRAUSER10106",
        "name": "00652",
        "emailAddress": "khai.tranngoc@vnresource.net",
        "avatarUrls": {
            "48x48": "http://192.168.11.202:5043/secure/useravatar?avatarId=10336",
            "24x24": "http://192.168.11.202:5043/secure/useravatar?size=small&avatarId=10336",
            "16x16": "http://192.168.11.202:5043/secure/useravatar?size=xsmall&avatarId=10336",
            "32x32": "http://192.168.11.202:5043/secure/useravatar?size=medium&avatarId=10336"
        },
        "displayName": "Trần Ngọc Khải",
        "active": true,
        "deleted": false,
        "timeZone": "Asia/Ho_Chi_Minh",
        "locale": "en_US"
    },
    {
        "self": "http://192.168.11.202:5043/rest/api/2/user?username=00658",
        "key": "JIRAUSER10105",
        "name": "00658",
        "emailAddress": "nhu.ton@vnresource.net",
        "avatarUrls": {
            "48x48": "http://192.168.11.202:5043/secure/useravatar?avatarId=10508",
            "24x24": "http://192.168.11.202:5043/secure/useravatar?size=small&avatarId=10508",
            "16x16": "http://192.168.11.202:5043/secure/useravatar?size=xsmall&avatarId=10508",
            "32x32": "http://192.168.11.202:5043/secure/useravatar?size=medium&avatarId=10508"
        },
        "displayName": "Tôn Hoàng Quỳnh Như",
        "active": true,
        "deleted": false,
        "timeZone": "Asia/Ho_Chi_Minh",
        "locale": "en_US"
    },
    {
        "self": "http://192.168.11.202:5043/rest/api/2/user?username=00670",
        "key": "JIRAUSER10504",
        "name": "00670",
        "emailAddress": "tuy.vu@vnresource.org",
        "avatarUrls": {
            "48x48": "https://www.gravatar.com/avatar/d65bfbcae93e0ff1d695ca0742259704?d=mm&s=48",
            "24x24": "https://www.gravatar.com/avatar/d65bfbcae93e0ff1d695ca0742259704?d=mm&s=24",
            "16x16": "https://www.gravatar.com/avatar/d65bfbcae93e0ff1d695ca0742259704?d=mm&s=16",
            "32x32": "https://www.gravatar.com/avatar/d65bfbcae93e0ff1d695ca0742259704?d=mm&s=32"
        },
        "displayName": "Vũ Văn Tuy",
        "active": true,
        "deleted": false,
        "timeZone": "Asia/Ho_Chi_Minh",
        "locale": "en_US"
    },
    {
        "self": "http://192.168.11.202:5043/rest/api/2/user?username=00686",
        "key": "JIRAUSER10211",
        "name": "00686",
        "emailAddress": "thuong.tran@vnresource.org",
        "avatarUrls": {
            "48x48": "https://www.gravatar.com/avatar/41cc301dcc382f82a3905985abce4105?d=mm&s=48",
            "24x24": "https://www.gravatar.com/avatar/41cc301dcc382f82a3905985abce4105?d=mm&s=24",
            "16x16": "https://www.gravatar.com/avatar/41cc301dcc382f82a3905985abce4105?d=mm&s=16",
            "32x32": "https://www.gravatar.com/avatar/41cc301dcc382f82a3905985abce4105?d=mm&s=32"
        },
        "displayName": "Trần Văn Hoài Thương",
        "active": true,
        "deleted": false,
        "timeZone": "Asia/Ho_Chi_Minh",
        "locale": "en_US"
    },
    {
        "self": "http://192.168.11.202:5043/rest/api/2/user?username=00687",
        "key": "JIRAUSER10216",
        "name": "00687",
        "emailAddress": "nhu.tran@vnresource.org",
        "avatarUrls": {
            "48x48": "https://www.gravatar.com/avatar/de4cfbea701c9eadcdfcfa296f88502a?d=mm&s=48",
            "24x24": "https://www.gravatar.com/avatar/de4cfbea701c9eadcdfcfa296f88502a?d=mm&s=24",
            "16x16": "https://www.gravatar.com/avatar/de4cfbea701c9eadcdfcfa296f88502a?d=mm&s=16",
            "32x32": "https://www.gravatar.com/avatar/de4cfbea701c9eadcdfcfa296f88502a?d=mm&s=32"
        },
        "displayName": "Trần Thị Quỳnh Như",
        "active": true,
        "deleted": false,
        "timeZone": "Asia/Ho_Chi_Minh",
        "locale": "en_US"
    },
    {
        "self": "http://192.168.11.202:5043/rest/api/2/user?username=00695",
        "key": "JIRAUSER10112",
        "name": "00695",
        "emailAddress": "luat.ta@vnresource.org",
        "avatarUrls": {
            "48x48": "http://192.168.11.202:5043/secure/useravatar?avatarId=10507",
            "24x24": "http://192.168.11.202:5043/secure/useravatar?size=small&avatarId=10507",
            "16x16": "http://192.168.11.202:5043/secure/useravatar?size=xsmall&avatarId=10507",
            "32x32": "http://192.168.11.202:5043/secure/useravatar?size=medium&avatarId=10507"
        },
        "displayName": "Tạ Minh Luật",
        "active": true,
        "deleted": false,
        "timeZone": "Asia/Ho_Chi_Minh",
        "locale": "en_US"
    },
    {
        "self": "http://192.168.11.202:5043/rest/api/2/user?username=00720",
        "key": "JIRAUSER10506",
        "name": "00720",
        "emailAddress": "bao.tranduy@vnresource.org",
        "avatarUrls": {
            "48x48": "https://www.gravatar.com/avatar/0234da343dfcb1d0de85c580c00608a3?d=mm&s=48",
            "24x24": "https://www.gravatar.com/avatar/0234da343dfcb1d0de85c580c00608a3?d=mm&s=24",
            "16x16": "https://www.gravatar.com/avatar/0234da343dfcb1d0de85c580c00608a3?d=mm&s=16",
            "32x32": "https://www.gravatar.com/avatar/0234da343dfcb1d0de85c580c00608a3?d=mm&s=32"
        },
        "displayName": "Trần Duy Bảo",
        "active": true,
        "deleted": false,
        "timeZone": "Asia/Ho_Chi_Minh",
        "locale": "en_US"
    },
    {
        "self": "http://192.168.11.202:5043/rest/api/2/user?username=00751",
        "key": "JIRAUSER10113",
        "name": "00751",
        "emailAddress": "truc.nguyen@vnresource.vn",
        "avatarUrls": {
            "48x48": "https://www.gravatar.com/avatar/70840e62f163822bf2c8866e20203e88?d=mm&s=48",
            "24x24": "https://www.gravatar.com/avatar/70840e62f163822bf2c8866e20203e88?d=mm&s=24",
            "16x16": "https://www.gravatar.com/avatar/70840e62f163822bf2c8866e20203e88?d=mm&s=16",
            "32x32": "https://www.gravatar.com/avatar/70840e62f163822bf2c8866e20203e88?d=mm&s=32"
        },
        "displayName": "Nguyễn Như Trúc",
        "active": true,
        "deleted": false,
        "timeZone": "Asia/Ho_Chi_Minh",
        "locale": "en_US"
    },
    {
        "self": "http://192.168.11.202:5043/rest/api/2/user?username=00755",
        "key": "JIRAUSER10500",
        "name": "00755",
        "emailAddress": "nhan.truongthi@vnresource.vn",
        "avatarUrls": {
            "48x48": "https://www.gravatar.com/avatar/9fdc9f0910858ab5cae7fcda63341a8f?d=mm&s=48",
            "24x24": "https://www.gravatar.com/avatar/9fdc9f0910858ab5cae7fcda63341a8f?d=mm&s=24",
            "16x16": "https://www.gravatar.com/avatar/9fdc9f0910858ab5cae7fcda63341a8f?d=mm&s=16",
            "32x32": "https://www.gravatar.com/avatar/9fdc9f0910858ab5cae7fcda63341a8f?d=mm&s=32"
        },
        "displayName": "Trương Thị Nhàn",
        "active": true,
        "deleted": false,
        "timeZone": "Asia/Ho_Chi_Minh",
        "locale": "en_US"
    },
    {
        "self": "http://192.168.11.202:5043/rest/api/2/user?username=00768",
        "key": "JIRAUSER10110",
        "name": "00768",
        "emailAddress": "quan.ly@vnresource.net",
        "avatarUrls": {
            "48x48": "https://www.gravatar.com/avatar/72cb223a8d52c4d21f82304b906001de?d=mm&s=48",
            "24x24": "https://www.gravatar.com/avatar/72cb223a8d52c4d21f82304b906001de?d=mm&s=24",
            "16x16": "https://www.gravatar.com/avatar/72cb223a8d52c4d21f82304b906001de?d=mm&s=16",
            "32x32": "https://www.gravatar.com/avatar/72cb223a8d52c4d21f82304b906001de?d=mm&s=32"
        },
        "displayName": "Lỷ Nhần Quắn",
        "active": true,
        "deleted": false,
        "timeZone": "Asia/Ho_Chi_Minh",
        "locale": "en_US"
    },
    {
        "self": "http://192.168.11.202:5043/rest/api/2/user?username=00816",
        "key": "JIRAUSER10213",
        "name": "00816",
        "emailAddress": "nhan.nguyenthanh@vnresource.org",
        "avatarUrls": {
            "48x48": "https://www.gravatar.com/avatar/05dcba4ff43d539c1361b6f275463182?d=mm&s=48",
            "24x24": "https://www.gravatar.com/avatar/05dcba4ff43d539c1361b6f275463182?d=mm&s=24",
            "16x16": "https://www.gravatar.com/avatar/05dcba4ff43d539c1361b6f275463182?d=mm&s=16",
            "32x32": "https://www.gravatar.com/avatar/05dcba4ff43d539c1361b6f275463182?d=mm&s=32"
        },
        "displayName": "Nguyễn Thành Nhân",
        "active": true,
        "deleted": false,
        "timeZone": "Asia/Ho_Chi_Minh",
        "locale": "en_US"
    },
    {
        "self": "http://192.168.11.202:5043/rest/api/2/user?username=00866",
        "key": "JIRAUSER10202",
        "name": "00866",
        "emailAddress": "quan.thaidongminh@vnresource.org",
        "avatarUrls": {
            "48x48": "https://www.gravatar.com/avatar/c4a39c422780f51e219d062093e65db5?d=mm&s=48",
            "24x24": "https://www.gravatar.com/avatar/c4a39c422780f51e219d062093e65db5?d=mm&s=24",
            "16x16": "https://www.gravatar.com/avatar/c4a39c422780f51e219d062093e65db5?d=mm&s=16",
            "32x32": "https://www.gravatar.com/avatar/c4a39c422780f51e219d062093e65db5?d=mm&s=32"
        },
        "displayName": "Thái Đồng Minh Quân",
        "active": true,
        "deleted": false,
        "timeZone": "Asia/Ho_Chi_Minh",
        "locale": "en_US"
    },
    {
        "self": "http://192.168.11.202:5043/rest/api/2/user?username=00889",
        "key": "JIRAUSER10502",
        "name": "00889",
        "emailAddress": "tuyen.lethikim@vnresource.org",
        "avatarUrls": {
            "48x48": "http://192.168.11.202:5043/secure/useravatar?avatarId=10341",
            "24x24": "http://192.168.11.202:5043/secure/useravatar?size=small&avatarId=10341",
            "16x16": "http://192.168.11.202:5043/secure/useravatar?size=xsmall&avatarId=10341",
            "32x32": "http://192.168.11.202:5043/secure/useravatar?size=medium&avatarId=10341"
        },
        "displayName": "LÊ THỊ KIM TUYỀN",
        "active": true,
        "deleted": false,
        "timeZone": "Asia/Ho_Chi_Minh",
        "locale": "en_US"
    },
    {
        "self": "http://192.168.11.202:5043/rest/api/2/user?username=00892",
        "key": "JIRAUSER10600",
        "name": "00892",
        "emailAddress": "dang.leminhhai@vnresource.org",
        "avatarUrls": {
            "48x48": "https://www.gravatar.com/avatar/c1ead4f78b3507c853faf56663e5fe25?d=mm&s=48",
            "24x24": "https://www.gravatar.com/avatar/c1ead4f78b3507c853faf56663e5fe25?d=mm&s=24",
            "16x16": "https://www.gravatar.com/avatar/c1ead4f78b3507c853faf56663e5fe25?d=mm&s=16",
            "32x32": "https://www.gravatar.com/avatar/c1ead4f78b3507c853faf56663e5fe25?d=mm&s=32"
        },
        "displayName": "Lê Minh Hải Đăng",
        "active": true,
        "deleted": false,
        "timeZone": "Asia/Ho_Chi_Minh",
        "locale": "en_US"
    },
    {
        "self": "http://192.168.11.202:5043/rest/api/2/user?username=00896",
        "key": "JIRAUSER10601",
        "name": "00896",
        "emailAddress": "hiep.nguyenhoang@vnresource.vn",
        "avatarUrls": {
            "48x48": "https://www.gravatar.com/avatar/0dcc25ddc8276c3960c46e443f1b0da1?d=mm&s=48",
            "24x24": "https://www.gravatar.com/avatar/0dcc25ddc8276c3960c46e443f1b0da1?d=mm&s=24",
            "16x16": "https://www.gravatar.com/avatar/0dcc25ddc8276c3960c46e443f1b0da1?d=mm&s=16",
            "32x32": "https://www.gravatar.com/avatar/0dcc25ddc8276c3960c46e443f1b0da1?d=mm&s=32"
        },
        "displayName": "Nguyễn Hoàng Hiệp",
        "active": true,
        "deleted": false,
        "timeZone": "Asia/Ho_Chi_Minh",
        "locale": "en_US"
    },
    {
        "self": "http://192.168.11.202:5043/rest/api/2/user?username=00907",
        "key": "JIRAUSER10301",
        "name": "00907",
        "emailAddress": "lekhanhhoang10112000@gmail.com",
        "avatarUrls": {
            "48x48": "https://www.gravatar.com/avatar/197c092ad7ff5fa0353a4d13d2f7184f?d=mm&s=48",
            "24x24": "https://www.gravatar.com/avatar/197c092ad7ff5fa0353a4d13d2f7184f?d=mm&s=24",
            "16x16": "https://www.gravatar.com/avatar/197c092ad7ff5fa0353a4d13d2f7184f?d=mm&s=16",
            "32x32": "https://www.gravatar.com/avatar/197c092ad7ff5fa0353a4d13d2f7184f?d=mm&s=32"
        },
        "displayName": "Lê Khánh Hoàng - 00907",
        "active": true,
        "deleted": false,
        "timeZone": "Asia/Ho_Chi_Minh",
        "locale": "en_US"
    },
    {
        "self": "http://192.168.11.202:5043/rest/api/2/user?username=00913",
        "key": "JIRAUSER10204",
        "name": "00913",
        "emailAddress": "hien.nguyenthu@vnresource.net",
        "avatarUrls": {
            "48x48": "https://www.gravatar.com/avatar/5e816a9210a0cffa3e0f48acc30e614d?d=mm&s=48",
            "24x24": "https://www.gravatar.com/avatar/5e816a9210a0cffa3e0f48acc30e614d?d=mm&s=24",
            "16x16": "https://www.gravatar.com/avatar/5e816a9210a0cffa3e0f48acc30e614d?d=mm&s=16",
            "32x32": "https://www.gravatar.com/avatar/5e816a9210a0cffa3e0f48acc30e614d?d=mm&s=32"
        },
        "displayName": "Nguyễn Thu Hiền",
        "active": true,
        "deleted": false,
        "timeZone": "Asia/Ho_Chi_Minh",
        "locale": "en_US"
    },
    {
        "self": "http://192.168.11.202:5043/rest/api/2/user?username=00919",
        "key": "JIRAUSER10107",
        "name": "00919",
        "emailAddress": "hai.daovan@vnresource.net",
        "avatarUrls": {
            "48x48": "http://192.168.11.202:5043/secure/useravatar?ownerId=JIRAUSER10107&avatarId=10602",
            "24x24": "http://192.168.11.202:5043/secure/useravatar?size=small&ownerId=JIRAUSER10107&avatarId=10602",
            "16x16": "http://192.168.11.202:5043/secure/useravatar?size=xsmall&ownerId=JIRAUSER10107&avatarId=10602",
            "32x32": "http://192.168.11.202:5043/secure/useravatar?size=medium&ownerId=JIRAUSER10107&avatarId=10602"
        },
        "displayName": "Đào Văn Hải",
        "active": true,
        "deleted": false,
        "timeZone": "Asia/Ho_Chi_Minh",
        "locale": "en_US"
    },
    {
        "self": "http://192.168.11.202:5043/rest/api/2/user?username=00931",
        "key": "JIRAUSER10207",
        "name": "00931",
        "emailAddress": "tram.lethingoc@vnresource.org",
        "avatarUrls": {
            "48x48": "https://www.gravatar.com/avatar/75805793818485e5fa5a7e1f8c9f75dd?d=mm&s=48",
            "24x24": "https://www.gravatar.com/avatar/75805793818485e5fa5a7e1f8c9f75dd?d=mm&s=24",
            "16x16": "https://www.gravatar.com/avatar/75805793818485e5fa5a7e1f8c9f75dd?d=mm&s=16",
            "32x32": "https://www.gravatar.com/avatar/75805793818485e5fa5a7e1f8c9f75dd?d=mm&s=32"
        },
        "displayName": "Lê Thị Ngọc Trâm",
        "active": true,
        "deleted": false,
        "timeZone": "Asia/Ho_Chi_Minh",
        "locale": "en_US"
    },
    {
        "self": "http://192.168.11.202:5043/rest/api/2/user?username=00939",
        "key": "JIRAUSER10505",
        "name": "00939",
        "emailAddress": "vinh.matan@vnresource.org",
        "avatarUrls": {
            "48x48": "https://www.gravatar.com/avatar/6b2e9b0761d95d888c28e110aeea70d7?d=mm&s=48",
            "24x24": "https://www.gravatar.com/avatar/6b2e9b0761d95d888c28e110aeea70d7?d=mm&s=24",
            "16x16": "https://www.gravatar.com/avatar/6b2e9b0761d95d888c28e110aeea70d7?d=mm&s=16",
            "32x32": "https://www.gravatar.com/avatar/6b2e9b0761d95d888c28e110aeea70d7?d=mm&s=32"
        },
        "displayName": "Mã Tấn Vĩnh",
        "active": true,
        "deleted": false,
        "timeZone": "Asia/Ho_Chi_Minh",
        "locale": "en_US"
    },
    {
        "self": "http://192.168.11.202:5043/rest/api/2/user?username=00941",
        "key": "JIRAUSER10205",
        "name": "00941",
        "emailAddress": "thuyen.phungthihong@vnresource.vn",
        "avatarUrls": {
            "48x48": "https://www.gravatar.com/avatar/25eb2c3bbeb68a8e9313f8ad6f85970b?d=mm&s=48",
            "24x24": "https://www.gravatar.com/avatar/25eb2c3bbeb68a8e9313f8ad6f85970b?d=mm&s=24",
            "16x16": "https://www.gravatar.com/avatar/25eb2c3bbeb68a8e9313f8ad6f85970b?d=mm&s=16",
            "32x32": "https://www.gravatar.com/avatar/25eb2c3bbeb68a8e9313f8ad6f85970b?d=mm&s=32"
        },
        "displayName": "Phùng Thị Hồng Thuyên",
        "active": true,
        "deleted": false,
        "timeZone": "Asia/Ho_Chi_Minh",
        "locale": "en_US"
    },
    {
        "self": "http://192.168.11.202:5043/rest/api/2/user?username=00942",
        "key": "JIRAUSER10509",
        "name": "00942",
        "emailAddress": "nhut.nguyenquoc@vnresource.org",
        "avatarUrls": {
            "48x48": "https://www.gravatar.com/avatar/4fe341e745a48b3cd75b73b9d15e158d?d=mm&s=48",
            "24x24": "https://www.gravatar.com/avatar/4fe341e745a48b3cd75b73b9d15e158d?d=mm&s=24",
            "16x16": "https://www.gravatar.com/avatar/4fe341e745a48b3cd75b73b9d15e158d?d=mm&s=16",
            "32x32": "https://www.gravatar.com/avatar/4fe341e745a48b3cd75b73b9d15e158d?d=mm&s=32"
        },
        "displayName": "Nguyễn Quốc Nhựt",
        "active": true,
        "deleted": false,
        "timeZone": "Asia/Ho_Chi_Minh",
        "locale": "en_US"
    },
    {
        "self": "http://192.168.11.202:5043/rest/api/2/user?username=00944",
        "key": "JIRAUSER10510",
        "name": "00944",
        "emailAddress": "thu.tranvuanh@vnresource.org",
        "avatarUrls": {
            "48x48": "http://192.168.11.202:5043/secure/useravatar?avatarId=10336",
            "24x24": "http://192.168.11.202:5043/secure/useravatar?size=small&avatarId=10336",
            "16x16": "http://192.168.11.202:5043/secure/useravatar?size=xsmall&avatarId=10336",
            "32x32": "http://192.168.11.202:5043/secure/useravatar?size=medium&avatarId=10336"
        },
        "displayName": "Trần Vũ Anh Thư",
        "active": true,
        "deleted": false,
        "timeZone": "Asia/Ho_Chi_Minh",
        "locale": "en_US"
    },
    {
        "self": "http://192.168.11.202:5043/rest/api/2/user?username=00947",
        "key": "JIRAUSER10206",
        "name": "00947",
        "emailAddress": "giang.nguyenthithu@vnresource.org",
        "avatarUrls": {
            "48x48": "https://www.gravatar.com/avatar/5f5d75e9190e62966a1f7a4bdfdd22a4?d=mm&s=48",
            "24x24": "https://www.gravatar.com/avatar/5f5d75e9190e62966a1f7a4bdfdd22a4?d=mm&s=24",
            "16x16": "https://www.gravatar.com/avatar/5f5d75e9190e62966a1f7a4bdfdd22a4?d=mm&s=16",
            "32x32": "https://www.gravatar.com/avatar/5f5d75e9190e62966a1f7a4bdfdd22a4?d=mm&s=32"
        },
        "displayName": "Nguyễn Thị Thu Giang",
        "active": true,
        "deleted": false,
        "timeZone": "Asia/Ho_Chi_Minh",
        "locale": "en_US"
    },
    {
        "self": "http://192.168.11.202:5043/rest/api/2/user?username=00949",
        "key": "JIRAUSER10201",
        "name": "00949",
        "emailAddress": "quan.maianh@vnresource.org",
        "avatarUrls": {
            "48x48": "https://www.gravatar.com/avatar/b289dda6a3b08af2a2591671527d21fe?d=mm&s=48",
            "24x24": "https://www.gravatar.com/avatar/b289dda6a3b08af2a2591671527d21fe?d=mm&s=24",
            "16x16": "https://www.gravatar.com/avatar/b289dda6a3b08af2a2591671527d21fe?d=mm&s=16",
            "32x32": "https://www.gravatar.com/avatar/b289dda6a3b08af2a2591671527d21fe?d=mm&s=32"
        },
        "displayName": "Mai Anh Quân",
        "active": true,
        "deleted": false,
        "timeZone": "Asia/Ho_Chi_Minh",
        "locale": "en_US"
    },
    {
        "self": "http://192.168.11.202:5043/rest/api/2/user?username=00956",
        "key": "JIRAUSER10203",
        "name": "00956",
        "emailAddress": "duy.trankhanh@vnresource.vn",
        "avatarUrls": {
            "48x48": "https://www.gravatar.com/avatar/a9a5fd9f999031f4b4021328a5bf34a3?d=mm&s=48",
            "24x24": "https://www.gravatar.com/avatar/a9a5fd9f999031f4b4021328a5bf34a3?d=mm&s=24",
            "16x16": "https://www.gravatar.com/avatar/a9a5fd9f999031f4b4021328a5bf34a3?d=mm&s=16",
            "32x32": "https://www.gravatar.com/avatar/a9a5fd9f999031f4b4021328a5bf34a3?d=mm&s=32"
        },
        "displayName": "Trần Khánh Duy",
        "active": true,
        "deleted": false,
        "timeZone": "Asia/Ho_Chi_Minh",
        "locale": "en_US"
    },
    {
        "self": "http://192.168.11.202:5043/rest/api/2/user?username=00957",
        "key": "JIRAUSER10200",
        "name": "00957",
        "emailAddress": "linh.tranngoc@vnresource.vn",
        "avatarUrls": {
            "48x48": "https://www.gravatar.com/avatar/47f25c7626ab41688c7891bec551aa81?d=mm&s=48",
            "24x24": "https://www.gravatar.com/avatar/47f25c7626ab41688c7891bec551aa81?d=mm&s=24",
            "16x16": "https://www.gravatar.com/avatar/47f25c7626ab41688c7891bec551aa81?d=mm&s=16",
            "32x32": "https://www.gravatar.com/avatar/47f25c7626ab41688c7891bec551aa81?d=mm&s=32"
        },
        "displayName": "Trần Ngọc Linh",
        "active": true,
        "deleted": false,
        "timeZone": "Asia/Ho_Chi_Minh",
        "locale": "en_US"
    },
    {
        "self": "http://192.168.11.202:5043/rest/api/2/user?username=A02-0004",
        "key": "JIRAUSER10300",
        "name": "A02-0004",
        "emailAddress": "dtduong@misa.com.vn",
        "avatarUrls": {
            "48x48": "https://www.gravatar.com/avatar/6b5808903247347ae129a1cfb09fd539?d=mm&s=48",
            "24x24": "https://www.gravatar.com/avatar/6b5808903247347ae129a1cfb09fd539?d=mm&s=24",
            "16x16": "https://www.gravatar.com/avatar/6b5808903247347ae129a1cfb09fd539?d=mm&s=16",
            "32x32": "https://www.gravatar.com/avatar/6b5808903247347ae129a1cfb09fd539?d=mm&s=32"
        },
        "displayName": "Đặng Thái Dương - A02-0004",
        "active": true,
        "deleted": false,
        "timeZone": "Asia/Ho_Chi_Minh",
        "locale": "en_US"
    },
    {
        "self": "http://192.168.11.202:5043/rest/api/2/user?username=admin",
        "key": "JIRAUSER10000",
        "name": "admin",
        "emailAddress": "misawebsite@software.misa.com.vn",
        "avatarUrls": {
            "48x48": "https://www.gravatar.com/avatar/e0a84704e02ee3fb45e427bd3d647e0a?d=mm&s=48",
            "24x24": "https://www.gravatar.com/avatar/e0a84704e02ee3fb45e427bd3d647e0a?d=mm&s=24",
            "16x16": "https://www.gravatar.com/avatar/e0a84704e02ee3fb45e427bd3d647e0a?d=mm&s=16",
            "32x32": "https://www.gravatar.com/avatar/e0a84704e02ee3fb45e427bd3d647e0a?d=mm&s=32"
        },
        "displayName": "admin",
        "active": true,
        "deleted": false,
        "timeZone": "Asia/Ho_Chi_Minh",
        "locale": "en_US"
    },
    {
        "self": "http://192.168.11.202:5043/rest/api/2/user?username=B-0997",
        "key": "JIRAUSER10100",
        "name": "B-0997",
        "emailAddress": "bhviet@software.misa.com.vn",
        "avatarUrls": {
            "48x48": "http://192.168.11.202:5043/secure/useravatar?ownerId=JIRAUSER10100&avatarId=10600",
            "24x24": "http://192.168.11.202:5043/secure/useravatar?size=small&ownerId=JIRAUSER10100&avatarId=10600",
            "16x16": "http://192.168.11.202:5043/secure/useravatar?size=xsmall&ownerId=JIRAUSER10100&avatarId=10600",
            "32x32": "http://192.168.11.202:5043/secure/useravatar?size=medium&ownerId=JIRAUSER10100&avatarId=10600"
        },
        "displayName": "Bạch Hoàng Việt",
        "active": true,
        "deleted": false,
        "timeZone": "Asia/Ho_Chi_Minh",
        "locale": "en_US"
    },
    {
        "self": "http://192.168.11.202:5043/rest/api/2/user?username=B06-0041",
        "key": "JIRAUSER10125",
        "name": "B06-0041",
        "emailAddress": "tnson@software.misa.com.vn",
        "avatarUrls": {
            "48x48": "https://www.gravatar.com/avatar/ebbb6313b16375145d50cb0793c84e44?d=mm&s=48",
            "24x24": "https://www.gravatar.com/avatar/ebbb6313b16375145d50cb0793c84e44?d=mm&s=24",
            "16x16": "https://www.gravatar.com/avatar/ebbb6313b16375145d50cb0793c84e44?d=mm&s=16",
            "32x32": "https://www.gravatar.com/avatar/ebbb6313b16375145d50cb0793c84e44?d=mm&s=32"
        },
        "displayName": "Trần Ngọc Sơn",
        "active": true,
        "deleted": false,
        "timeZone": "Asia/Ho_Chi_Minh",
        "locale": "en_US"
    },
    {
        "self": "http://192.168.11.202:5043/rest/api/2/user?username=B24-0020",
        "key": "JIRAUSER10121",
        "name": "B24-0020",
        "emailAddress": "ntkien@software.misa.com.vn",
        "avatarUrls": {
            "48x48": "https://www.gravatar.com/avatar/83029743ed23bfc4225bd258b5e9a63d?d=mm&s=48",
            "24x24": "https://www.gravatar.com/avatar/83029743ed23bfc4225bd258b5e9a63d?d=mm&s=24",
            "16x16": "https://www.gravatar.com/avatar/83029743ed23bfc4225bd258b5e9a63d?d=mm&s=16",
            "32x32": "https://www.gravatar.com/avatar/83029743ed23bfc4225bd258b5e9a63d?d=mm&s=32"
        },
        "displayName": "Nguyễn Trung Kiên",
        "active": true,
        "deleted": false,
        "timeZone": "Asia/Ho_Chi_Minh",
        "locale": "en_US"
    },
    {
        "self": "http://192.168.11.202:5043/rest/api/2/user?username=C10-0022",
        "key": "JIRAUSER10122",
        "name": "C10-0022",
        "emailAddress": "ntthuy@misa.com.vn",
        "avatarUrls": {
            "48x48": "http://192.168.11.202:5043/secure/useravatar?avatarId=10337",
            "24x24": "http://192.168.11.202:5043/secure/useravatar?size=small&avatarId=10337",
            "16x16": "http://192.168.11.202:5043/secure/useravatar?size=xsmall&avatarId=10337",
            "32x32": "http://192.168.11.202:5043/secure/useravatar?size=medium&avatarId=10337"
        },
        "displayName": "Nguyên Thanh Thủy",
        "active": true,
        "deleted": false,
        "timeZone": "Asia/Ho_Chi_Minh",
        "locale": "en_US"
    },
    {
        "self": "http://192.168.11.202:5043/rest/api/2/user?username=J-0002",
        "key": "JIRAUSER10124",
        "name": "J-0002",
        "emailAddress": "ththu@software.misa.com.vn",
        "avatarUrls": {
            "48x48": "https://www.gravatar.com/avatar/c1bd4571ccc93f9e7269442d7288181f?d=mm&s=48",
            "24x24": "https://www.gravatar.com/avatar/c1bd4571ccc93f9e7269442d7288181f?d=mm&s=24",
            "16x16": "https://www.gravatar.com/avatar/c1bd4571ccc93f9e7269442d7288181f?d=mm&s=16",
            "32x32": "https://www.gravatar.com/avatar/c1bd4571ccc93f9e7269442d7288181f?d=mm&s=32"
        },
        "displayName": "Chị Thu MISA",
        "active": true,
        "deleted": false,
        "timeZone": "Asia/Ho_Chi_Minh",
        "locale": "en_US"
    },
    {
        "self": "http://192.168.11.202:5043/rest/api/2/user?username=misaticket",
        "key": "JIRAUSER10126",
        "name": "misaticket",
        "emailAddress": "ticket@software.misa.com.vn",
        "avatarUrls": {
            "48x48": "https://www.gravatar.com/avatar/403768669953a03b299ebad1b46a1650?d=mm&s=48",
            "24x24": "https://www.gravatar.com/avatar/403768669953a03b299ebad1b46a1650?d=mm&s=24",
            "16x16": "https://www.gravatar.com/avatar/403768669953a03b299ebad1b46a1650?d=mm&s=16",
            "32x32": "https://www.gravatar.com/avatar/403768669953a03b299ebad1b46a1650?d=mm&s=32"
        },
        "displayName": "misaticket -VNR",
        "active": true,
        "deleted": false,
        "timeZone": "Asia/Ho_Chi_Minh",
        "locale": "en_US"
    },
    {
        "self": "http://192.168.11.202:5043/rest/api/2/user?username=ticket",
        "key": "JIRAUSER10123",
        "name": "ticket",
        "emailAddress": "ticket_app@software.misa.com.vn",
        "avatarUrls": {
            "48x48": "https://www.gravatar.com/avatar/b61db0619b8c09903cc7394f2596c9cc?d=mm&s=48",
            "24x24": "https://www.gravatar.com/avatar/b61db0619b8c09903cc7394f2596c9cc?d=mm&s=24",
            "16x16": "https://www.gravatar.com/avatar/b61db0619b8c09903cc7394f2596c9cc?d=mm&s=16",
            "32x32": "https://www.gravatar.com/avatar/b61db0619b8c09903cc7394f2596c9cc?d=mm&s=32"
        },
        "displayName": "Ticket",
        "active": true,
        "deleted": false,
        "timeZone": "Asia/Ho_Chi_Minh",
        "locale": "en_US"
    }
]
"""
data = json.loads(json_data)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Cách 2: Dùng vòng lặp for thông thường (dễ đọc hơn)
result = []
for item in data:
    extracted = {
        'key': item.get('key'),
        'name': item.get('name'),
        'displayName': item.get('displayName')
    }
    result.append(extracted)

with open('jira_processes/jira-users.json', mode='w', encoding='utf-8') as json_file:
    json.dump(result, json_file, indent=2, ensure_ascii=False)


# # Cách in an toàn với Unicode
# try:
#     print(json.dumps(result, indent=2, ensure_ascii=False))
# except UnicodeEncodeError:
#     # Fallback nếu không in được Unicode
#     print(json.dumps(result, indent=2, ensure_ascii=True))  # Chuyển sang ASCII escape