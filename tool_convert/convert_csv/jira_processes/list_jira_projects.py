import sys
import io
import json

json_data = """[
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/11119",
        "id": "11119",
        "key": "FO",
        "name": "5FOOD",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10104",
            "id": "10104",
            "name": "Khối SP Bán lẻ",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/11403",
        "id": "11403",
        "key": "AIMS",
        "name": "AIAgentPlatform",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10108",
            "id": "10108",
            "name": "Viện Công nghệ",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/10129",
        "id": "10129",
        "key": "AIM",
        "name": "AMIS aiMarketing ",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10106",
            "id": "10106",
            "name": "Khối SP Doanh nghiệp",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/10115",
        "id": "10115",
        "key": "MISAIVAN",
        "name": "AMIS BHXH ",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?pid=10115&avatarId=10011",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&pid=10115&avatarId=10011",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&pid=10115&avatarId=10011",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&pid=10115&avatarId=10011"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10106",
            "id": "10106",
            "name": "Khối SP Doanh nghiệp",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/11307",
        "id": "11307",
        "key": "AMISCHAT",
        "name": "AMIS Chat",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10106",
            "id": "10106",
            "name": "Khối SP Doanh nghiệp",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/10114",
        "id": "10114",
        "key": "TIMESHEET",
        "name": "AMIS Chấm công",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?pid=10114&avatarId=10200",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&pid=10114&avatarId=10200",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&pid=10114&avatarId=10200",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&pid=10114&avatarId=10200"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10106",
            "id": "10106",
            "name": "Khối SP Doanh nghiệp",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/10112",
        "id": "10112",
        "key": "CRM",
        "name": "AMIS CRM ",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?pid=10112&avatarId=12519",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&pid=10112&avatarId=12519",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&pid=10112&avatarId=12519",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&pid=10112&avatarId=12519"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10106",
            "id": "10106",
            "name": "Khối SP Doanh nghiệp",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/10704",
        "id": "10704",
        "key": "CRMMB",
        "name": "AMIS CRM2 Mobile",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10106",
            "id": "10106",
            "name": "Khối SP Doanh nghiệp",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/10118",
        "id": "10118",
        "key": "TASK",
        "name": "AMIS Công việc ",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10106",
            "id": "10106",
            "name": "Khối SP Doanh nghiệp",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/10302",
        "id": "10302",
        "key": "MAGC",
        "name": "AMIS Ghi chép ",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10106",
            "id": "10106",
            "name": "Khối SP Doanh nghiệp",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/11126",
        "id": "11126",
        "key": "HRMMISA",
        "name": "AMIS HRM MISA",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10106",
            "id": "10106",
            "name": "Khối SP Doanh nghiệp",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/10600",
        "id": "10600",
        "key": "AMISKM",
        "name": "AMIS Khuyến mại ",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10106",
            "id": "10106",
            "name": "Khối SP Doanh nghiệp",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/10101",
        "id": "10101",
        "key": "MAKT",
        "name": "AMIS Kế toán ",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?pid=10101&avatarId=10009",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&pid=10101&avatarId=10009",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&pid=10101&avatarId=10009",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&pid=10101&avatarId=10009"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10106",
            "id": "10106",
            "name": "Khối SP Doanh nghiệp",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/10905",
        "id": "10905",
        "key": "MAKTAPI",
        "name": "AMIS Kế toán API",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10106",
            "id": "10106",
            "name": "Khối SP Doanh nghiệp",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/11135",
        "id": "11135",
        "key": "MAKTEDU",
        "name": "AMIS Kế toán EDU",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10106",
            "id": "10106",
            "name": "Khối SP Doanh nghiệp",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/10207",
        "id": "10207",
        "key": "HKD",
        "name": "AMIS Kế toán HKD ",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10102",
            "id": "10102",
            "name": "Khối NT Kế toán dịch vụ (ASP)",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/10909",
        "id": "10909",
        "key": "HKDM",
        "name": "AMIS Kế toán HKD Mobile",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10102",
            "id": "10102",
            "name": "Khối NT Kế toán dịch vụ (ASP)",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/11405",
        "id": "11405",
        "key": "HTX",
        "name": "AMIS Kế toán Hợp tác xã",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/10716",
        "id": "10716",
        "key": "MAK",
        "name": "AMIS kế toán Mobile",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10106",
            "id": "10106",
            "name": "Khối SP Doanh nghiệp",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/10303",
        "id": "10303",
        "key": "AMH",
        "name": "AMIS Mua hàng ",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10106",
            "id": "10106",
            "name": "Khối SP Doanh nghiệp",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/10304",
        "id": "10304",
        "key": "MAMXH",
        "name": "AMIS Mạng xã hội ",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10106",
            "id": "10106",
            "name": "Khối SP Doanh nghiệp",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/10601",
        "id": "10601",
        "key": "AMISMT",
        "name": "AMIS Mục tiêu",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10106",
            "id": "10106",
            "name": "Khối SP Doanh nghiệp",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/10901",
        "id": "10901",
        "key": "ASB",
        "name": "AMIS nền tảng kế toán dịch vụ",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10102",
            "id": "10102",
            "name": "Khối NT Kế toán dịch vụ (ASP)",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/11600",
        "id": "11600",
        "key": "ONEAI",
        "name": "AMIS OneAI",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10106",
            "id": "10106",
            "name": "Khối SP Doanh nghiệp",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/10209",
        "id": "10209",
        "key": "MAPH",
        "name": "AMIS Phòng họp ",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10106",
            "id": "10106",
            "name": "Khối SP Doanh nghiệp",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/10900",
        "id": "10900",
        "key": "MACORE",
        "name": "AMIS PL Core",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10106",
            "id": "10106",
            "name": "Khối SP Doanh nghiệp",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/10906",
        "id": "10906",
        "key": "MADB",
        "name": "AMIS PL Danh bạ",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10106",
            "id": "10106",
            "name": "Khối SP Doanh nghiệp",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/11303",
        "id": "11303",
        "key": "KHO",
        "name": "AMIS PL Kho",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10106",
            "id": "10106",
            "name": "Khối SP Doanh nghiệp",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/11308",
        "id": "11308",
        "key": "QTSX",
        "name": "AMIS PL Sản xuất ",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/10126",
        "id": "10126",
        "key": "AMPROCESS",
        "name": "AMIS Quy trình ",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10106",
            "id": "10106",
            "name": "Khối SP Doanh nghiệp",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/10117",
        "id": "10117",
        "key": "MINTAX",
        "name": "AMIS Thuế TNCN ",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?pid=10117&avatarId=10201",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&pid=10117&avatarId=10201",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&pid=10117&avatarId=10201",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&pid=10117&avatarId=10201"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10106",
            "id": "10106",
            "name": "Khối SP Doanh nghiệp",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/10116",
        "id": "10116",
        "key": "TTNS",
        "name": "AMIS Thông tin nhân sự ",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?pid=10116&avatarId=10202",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&pid=10116&avatarId=10202",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&pid=10116&avatarId=10202",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&pid=10116&avatarId=10202"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10106",
            "id": "10106",
            "name": "Khối SP Doanh nghiệp",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/10113",
        "id": "10113",
        "key": "PAYROLL",
        "name": "AMIS Tiền lương ",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10106",
            "id": "10106",
            "name": "Khối SP Doanh nghiệp",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/10208",
        "id": "10208",
        "key": "MATD",
        "name": "AMIS Tuyển dụng ",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10106",
            "id": "10106",
            "name": "Khối SP Doanh nghiệp",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/10124",
        "id": "10124",
        "key": "ASSET",
        "name": "AMIS Tài sản ",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10106",
            "id": "10106",
            "name": "Khối SP Doanh nghiệp",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/10305",
        "id": "10305",
        "key": "APVT",
        "name": "AMIS Văn Thư",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10106",
            "id": "10106",
            "name": "Khối SP Doanh nghiệp",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/10125",
        "id": "10125",
        "key": "WESIGN",
        "name": "AMIS WeSign ",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10106",
            "id": "10106",
            "name": "Khối SP Doanh nghiệp",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/11400",
        "id": "11400",
        "key": "AMISWF",
        "name": "AMIS Workflow",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10106",
            "id": "10106",
            "name": "Khối SP Doanh nghiệp",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/10911",
        "id": "10911",
        "key": "AMDH",
        "name": "AMIS Điều hành",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10106",
            "id": "10106",
            "name": "Khối SP Doanh nghiệp",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/10602",
        "id": "10602",
        "key": "AMISDG",
        "name": "AMIS Đánh giá",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10106",
            "id": "10106",
            "name": "Khối SP Doanh nghiệp",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/10910",
        "id": "10910",
        "key": "ASPM",
        "name": "ASP Mobile",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10106",
            "id": "10106",
            "name": "Khối SP Doanh nghiệp",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/10701",
        "id": "10701",
        "key": "STORE",
        "name": "Automation Sales",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10100",
            "id": "10100",
            "name": "Ban CNTT",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/11302",
        "id": "11302",
        "key": "AVAAMIS",
        "name": "AVA AMIS - NỘI BỘ",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10106",
            "id": "10106",
            "name": "Khối SP Doanh nghiệp",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/11101",
        "id": "11101",
        "key": "CUS",
        "name": "Customize",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10106",
            "id": "10106",
            "name": "Khối SP Doanh nghiệp",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/11134",
        "id": "11134",
        "key": "DBTOOL",
        "name": "DBTOOL",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10103",
            "id": "10103",
            "name": "Khối Sản xuất",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/11143",
        "id": "11143",
        "key": "EKTM",
        "name": "EMIS Thanh toán KDTM",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10107",
            "id": "10107",
            "name": "Khối SP Hành chính sự nghiệp",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/10714",
        "id": "10714",
        "key": "EM",
        "name": "eSign Mobile",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10106",
            "id": "10106",
            "name": "Khối SP Doanh nghiệp",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/11128",
        "id": "11128",
        "key": "QVA",
        "name": "General",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10103",
            "id": "10103",
            "name": "Khối Sản xuất",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/11132",
        "id": "11132",
        "key": "HCSNMONITO",
        "name": "HCSN Monitor",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10107",
            "id": "10107",
            "name": "Khối SP Hành chính sự nghiệp",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/11109",
        "id": "11109",
        "key": "HC",
        "name": "Healthcheck",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10103",
            "id": "10103",
            "name": "Khối Sản xuất",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/11131",
        "id": "11131",
        "key": "PE",
        "name": "Hóa đơn xăng dầu",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10106",
            "id": "10106",
            "name": "Khối SP Doanh nghiệp",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/11130",
        "id": "11130",
        "key": "HTDT",
        "name": "Hợp tác đối tác",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10103",
            "id": "10103",
            "name": "Khối Sản xuất",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/11123",
        "id": "11123",
        "key": "MIP",
        "name": "Internal Product SP nội bộ",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10100",
            "id": "10100",
            "name": "Ban CNTT",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/10705",
        "id": "10705",
        "key": "JPBANK",
        "name": "JetPay BankHub ",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10101",
            "id": "10101",
            "name": "JETPAY",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/11122",
        "id": "11122",
        "key": "JPMM",
        "name": "JETPAY MEMAS",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10101",
            "id": "10101",
            "name": "JETPAY",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/10715",
        "id": "10715",
        "key": "JPCTT",
        "name": "Jetpay Payment ",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10101",
            "id": "10101",
            "name": "JETPAY",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/10702",
        "id": "10702",
        "key": "JPTHP",
        "name": "JETPAY Thu học phí",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10101",
            "id": "10101",
            "name": "JETPAY",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/11107",
        "id": "11107",
        "key": "LS",
        "name": "Location Service",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10108",
            "id": "10108",
            "name": "Viện Công nghệ",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/11133",
        "id": "11133",
        "key": "EMS",
        "name": "mail Service",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10108",
            "id": "10108",
            "name": "Viện Công nghệ",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/11129",
        "id": "11129",
        "key": "AMIS",
        "name": "MISA AMIS 1.0",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10106",
            "id": "10106",
            "name": "Khối SP Doanh nghiệp",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/10131",
        "id": "10131",
        "key": "AMISV2",
        "name": "MISA AMIS 2.0",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10106",
            "id": "10106",
            "name": "Khối SP Doanh nghiệp",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/10902",
        "id": "10902",
        "key": "AMISMOBILE",
        "name": "MISA AMIS Mobile",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10106",
            "id": "10106",
            "name": "Khối SP Doanh nghiệp",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/11104",
        "id": "11104",
        "key": "MAI",
        "name": "MISA Artificial Intelligence",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10108",
            "id": "10108",
            "name": "Viện Công nghệ",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/10130",
        "id": "10130",
        "key": "ASP",
        "name": "MISA ASP ",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10102",
            "id": "10102",
            "name": "Khối NT Kế toán dịch vụ (ASP)",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/11105",
        "id": "11105",
        "key": "MAL",
        "name": "MISA Auditing Log Service",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10108",
            "id": "10108",
            "name": "Viện Công nghệ",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/10711",
        "id": "10711",
        "key": "AVA",
        "name": "MISA AVA platfrom",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10108",
            "id": "10108",
            "name": "Viện Công nghệ",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/10500",
        "id": "10500",
        "key": "MBO",
        "name": "MISA Bamboo online",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10107",
            "id": "10107",
            "name": "Khối SP Hành chính sự nghiệp",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/10103",
        "id": "10103",
        "key": "BAM",
        "name": "MISA Bamboo.Net 2020",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10107",
            "id": "10107",
            "name": "Khối SP Hành chính sự nghiệp",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/10205",
        "id": "10205",
        "key": "QLNS",
        "name": "MISA Bumas",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10107",
            "id": "10107",
            "name": "Khối SP Hành chính sự nghiệp",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/11305",
        "id": "11305",
        "key": "BUTW",
        "name": "MISA Bumas TW",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10106",
            "id": "10106",
            "name": "Khối SP Doanh nghiệp",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/11141",
        "id": "11141",
        "key": "QLNSV3",
        "name": "MISA Bumas V3",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?pid=11141&avatarId=12805",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&pid=11141&avatarId=12805",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&pid=11141&avatarId=12805",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&pid=11141&avatarId=12805"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10107",
            "id": "10107",
            "name": "Khối SP Hành chính sự nghiệp",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/10127",
        "id": "10127",
        "key": "CEGOV",
        "name": "MISA CeGov",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10107",
            "id": "10107",
            "name": "Khối SP Hành chính sự nghiệp",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/11116",
        "id": "11116",
        "key": "MCC",
        "name": "MISA Cloud Center",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10100",
            "id": "10100",
            "name": "Ban CNTT",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/11115",
        "id": "11115",
        "key": "CRM08",
        "name": "MISA CRM.NET 2008",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10106",
            "id": "10106",
            "name": "Khối SP Doanh nghiệp",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/10110",
        "id": "10110",
        "key": "CUK",
        "name": "MISA Cukcuk",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10104",
            "id": "10104",
            "name": "Khối SP Bán lẻ",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/10713",
        "id": "10713",
        "key": "MCP",
        "name": "MISA Customer Profile",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10100",
            "id": "10100",
            "name": "Ban CNTT",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/11136",
        "id": "11136",
        "key": "DVC",
        "name": "MISA DVC",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10107",
            "id": "10107",
            "name": "Khối SP Hành chính sự nghiệp",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/11300",
        "id": "11300",
        "key": "MECS",
        "name": "MISA eCommerce Service",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/11404",
        "id": "11404",
        "key": "MEP",
        "name": "MISA Education Program",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10100",
            "id": "10100",
            "name": "Ban CNTT",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/11500",
        "id": "11500",
        "key": "MEH",
        "name": "MISA eHospital",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10107",
            "id": "10107",
            "name": "Khối SP Hành chính sự nghiệp",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/10301",
        "id": "10301",
        "key": "STUD",
        "name": "MISA EMIS Học sinh",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10107",
            "id": "10107",
            "name": "Khối SP Hành chính sự nghiệp",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/10105",
        "id": "10105",
        "key": "FEE",
        "name": "MISA EMIS Khoản thu",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10107",
            "id": "10107",
            "name": "Khối SP Hành chính sự nghiệp",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/10903",
        "id": "10903",
        "key": "EMTT",
        "name": "MISA EMIS Kindergarten",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?pid=10903&avatarId=12700",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&pid=10903&avatarId=12700",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&pid=10903&avatarId=12700",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&pid=10903&avatarId=12700"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10109",
            "id": "10109",
            "name": "Khối NT Quản lý Giáo dục",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/10106",
        "id": "10106",
        "key": "EQUI",
        "name": "MISA EMIS Thiết bị",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10107",
            "id": "10107",
            "name": "Khối SP Hành chính sự nghiệp",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/10107",
        "id": "10107",
        "key": "LIBR",
        "name": "MISA EMIS Thư viện",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10107",
            "id": "10107",
            "name": "Khối SP Hành chính sự nghiệp",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/10108",
        "id": "10108",
        "key": "SCHE",
        "name": "MISA EMIS Thời khóa biểu",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10107",
            "id": "10107",
            "name": "Khối SP Hành chính sự nghiệp",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/11140",
        "id": "11140",
        "key": "EOF",
        "name": "MISA eOffice (TaskGo/TaskGov/...)",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10107",
            "id": "10107",
            "name": "Khối SP Hành chính sự nghiệp",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/10111",
        "id": "10111",
        "key": "ESHOP",
        "name": "MISA eShop",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10104",
            "id": "10104",
            "name": "Khối SP Bán lẻ",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/11402",
        "id": "11402",
        "key": "SHOPV2",
        "name": "MISA eShop v2",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10104",
            "id": "10104",
            "name": "Khối SP Bán lẻ",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/10121",
        "id": "10121",
        "key": "ES",
        "name": "MISA eSign ",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10106",
            "id": "10106",
            "name": "Khối SP Doanh nghiệp",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/10202",
        "id": "10202",
        "key": "FC",
        "name": "MISA Falcon 2023",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10107",
            "id": "10107",
            "name": "Khối SP Hành chính sự nghiệp",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/11112",
        "id": "11112",
        "key": "FORUM",
        "name": "MISA Forum",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10100",
            "id": "10100",
            "name": "Ban CNTT",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/10912",
        "id": "10912",
        "key": "GOLFHANDIC",
        "name": "MISA Golf",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10105",
            "id": "10105",
            "name": "Khối SP Cá nhân",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/10300",
        "id": "10300",
        "key": "MH",
        "name": "MISA Hotich",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10107",
            "id": "10107",
            "name": "Khối SP Hành chính sự nghiệp",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/10703",
        "id": "10703",
        "key": "IMS",
        "name": "MISA IMS",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10100",
            "id": "10100",
            "name": "Ban CNTT",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/11121",
        "id": "11121",
        "key": "INC",
        "name": "MISA Incident",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10103",
            "id": "10103",
            "name": "Khối Sản xuất",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/10719",
        "id": "10719",
        "key": "ISMAC",
        "name": "MISA ISMAC",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10100",
            "id": "10100",
            "name": "Ban CNTT",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/10707",
        "id": "10707",
        "key": "MK",
        "name": "MISA KYSO",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10106",
            "id": "10106",
            "name": "Khối SP Doanh nghiệp",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/10206",
        "id": "10206",
        "key": "LEKI",
        "name": "MISA Lekima",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10107",
            "id": "10107",
            "name": "Khối SP Hành chính sự nghiệp",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/10710",
        "id": "10710",
        "key": "MLP",
        "name": "MISA Lending ",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10101",
            "id": "10101",
            "name": "JETPAY",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/11117",
        "id": "11117",
        "key": "MLA",
        "name": "MISA License Agreement",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10108",
            "id": "10108",
            "name": "Viện Công nghệ",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/10201",
        "id": "10201",
        "key": "LOMAS",
        "name": "MISA Lomas",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10104",
            "id": "10104",
            "name": "Khối SP Bán lẻ",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/10000",
        "id": "10000",
        "key": "ME",
        "name": "MISA meInvoice hóa đơn đầu ra",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10106",
            "id": "10106",
            "name": "Khối SP Doanh nghiệp",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/10119",
        "id": "10119",
        "key": "MEINBOT",
        "name": "MISA meInvoice hóa đơn đầu vào",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10106",
            "id": "10106",
            "name": "Khối SP Doanh nghiệp",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/10102",
        "id": "10102",
        "key": "MIMO",
        "name": "MISA Mimosa 2022",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10107",
            "id": "10107",
            "name": "Khối SP Hành chính sự nghiệp",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/11142",
        "id": "11142",
        "key": "MM25",
        "name": "MISA Mimosa 2025",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10107",
            "id": "10107",
            "name": "Khối SP Hành chính sự nghiệp",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/10132",
        "id": "10132",
        "key": "MMO",
        "name": "MISA Mimosa Online",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?pid=10132&avatarId=13700",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&pid=10132&avatarId=13700",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&pid=10132&avatarId=13700",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&pid=10132&avatarId=13700"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10107",
            "id": "10107",
            "name": "Khối SP Hành chính sự nghiệp",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/11306",
        "id": "11306",
        "key": "MIMOX",
        "name": "MISA Mimosa X1",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10107",
            "id": "10107",
            "name": "Khối SP Hành chính sự nghiệp",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/10203",
        "id": "10203",
        "key": "SOTHUCHI",
        "name": "MISA MoneyKeeper",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10105",
            "id": "10105",
            "name": "Khối SP Cá nhân",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/11110",
        "id": "11110",
        "key": "MM",
        "name": "MISA Monitor",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10103",
            "id": "10103",
            "name": "Khối Sản xuất",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/11124",
        "id": "11124",
        "key": "MMA",
        "name": "MISA Monitoring Alerts",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10103",
            "id": "10103",
            "name": "Khối Sản xuất",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/10120",
        "id": "10120",
        "key": "MTAX",
        "name": "MISA mTax",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10106",
            "id": "10106",
            "name": "Khối SP Doanh nghiệp",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/11106",
        "id": "11106",
        "key": "MIN",
        "name": "MISA Notification",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10108",
            "id": "10108",
            "name": "Viện Công nghệ",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/10200",
        "id": "10200",
        "key": "OCM",
        "name": "MISA OCM ",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10104",
            "id": "10104",
            "name": "Khối SP Bán lẻ",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/10708",
        "id": "10708",
        "key": "MISAORDER",
        "name": "MISA ORDER",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10100",
            "id": "10100",
            "name": "Ban CNTT",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/11125",
        "id": "11125",
        "key": "ORG",
        "name": "MISA OrgInfo",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10108",
            "id": "10108",
            "name": "Viện Công nghệ",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/10204",
        "id": "10204",
        "key": "PANDA",
        "name": "MISA Panda.net 2021",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10107",
            "id": "10107",
            "name": "Khối SP Hành chính sự nghiệp",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/10709",
        "id": "10709",
        "key": "MSP",
        "name": "Misa Partner",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10100",
            "id": "10100",
            "name": "Ban CNTT",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/10718",
        "id": "10718",
        "key": "MPG",
        "name": "MISA Payment Gateway",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10104",
            "id": "10104",
            "name": "Khối SP Bán lẻ",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/11100",
        "id": "11100",
        "key": "PA",
        "name": "MISA Process Automation",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10100",
            "id": "10100",
            "name": "Ban CNTT",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/10122",
        "id": "10122",
        "key": "QLCB",
        "name": "MISA QLCB",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10107",
            "id": "10107",
            "name": "Khối SP Hành chính sự nghiệp",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/10104",
        "id": "10104",
        "key": "QLTS",
        "name": "MISA QLTS",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10107",
            "id": "10107",
            "name": "Khối SP Hành chính sự nghiệp",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/10123",
        "id": "10123",
        "key": "SLG",
        "name": "MISA Salagov",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10107",
            "id": "10107",
            "name": "Khối SP Hành chính sự nghiệp",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/10109",
        "id": "10109",
        "key": "SISAP",
        "name": "MISA SISAP",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10107",
            "id": "10107",
            "name": "Khối SP Hành chính sự nghiệp",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/10400",
        "id": "10400",
        "key": "SMEO",
        "name": "MISA SME 2022 trở về trước",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10106",
            "id": "10106",
            "name": "Khối SP Doanh nghiệp",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/10100",
        "id": "10100",
        "key": "SME",
        "name": "MISA SME 2023",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?pid=10100&avatarId=10001",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&pid=10100&avatarId=10001",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&pid=10100&avatarId=10001",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&pid=10100&avatarId=10001"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10106",
            "id": "10106",
            "name": "Khối SP Doanh nghiệp",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/10915",
        "id": "10915",
        "key": "STARTBOOKS",
        "name": "MISA StartBooks",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10106",
            "id": "10106",
            "name": "Khối SP Doanh nghiệp",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/11137",
        "id": "11137",
        "key": "MSUPPORT",
        "name": "MISA SUPPORT",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10100",
            "id": "10100",
            "name": "Ban CNTT",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/11145",
        "id": "11145",
        "key": "MSS",
        "name": "MISA Sync Service",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10108",
            "id": "10108",
            "name": "Viện Công nghệ",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/10128",
        "id": "10128",
        "key": "TASKGO",
        "name": "MISA TaskGo ",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10107",
            "id": "10107",
            "name": "Khối SP Hành chính sự nghiệp",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/11139",
        "id": "11139",
        "key": "JIRA",
        "name": "MISA TICKET",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10100",
            "id": "10100",
            "name": "Ban CNTT",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/11144",
        "id": "11144",
        "key": "MWS",
        "name": "MISA Web Socket",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10108",
            "id": "10108",
            "name": "Viện Công nghệ",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/10706",
        "id": "10706",
        "key": "WEBSITE",
        "name": "MISA Website",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10100",
            "id": "10100",
            "name": "Ban CNTT",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/11114",
        "id": "11114",
        "key": "MISACUSTOM",
        "name": "MISACustomize",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10106",
            "id": "10106",
            "name": "Khối SP Doanh nghiệp",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/10712",
        "id": "10712",
        "key": "MID",
        "name": "MISAID",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10100",
            "id": "10100",
            "name": "Ban CNTT",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/10700",
        "id": "10700",
        "key": "CRMMISA",
        "name": "MISAJSC CRM Nội bộ",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10106",
            "id": "10106",
            "name": "Khối SP Doanh nghiệp",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/11118",
        "id": "11118",
        "key": "MOP",
        "name": "Mobile Push Notification Service",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10108",
            "id": "10108",
            "name": "Viện Công nghệ",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/11301",
        "id": "11301",
        "key": "QLTC",
        "name": "Quản lý thi công",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?pid=11301&avatarId=10200",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&pid=11301&avatarId=10200",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&pid=11301&avatarId=10200",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&pid=11301&avatarId=10200"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10100",
            "id": "10100",
            "name": "Ban CNTT",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/11102",
        "id": "11102",
        "key": "SMSBRAND",
        "name": "SMS BRAND NAME",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10108",
            "id": "10108",
            "name": "Viện Công nghệ",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/11127",
        "id": "11127",
        "key": "SRE",
        "name": "SRE DevOps",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10103",
            "id": "10103",
            "name": "Khối Sản xuất",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/11103",
        "id": "11103",
        "key": "ARC",
        "name": "Technical Issues",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10103",
            "id": "10103",
            "name": "Khối Sản xuất",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/11120",
        "id": "11120",
        "key": "TSDR",
        "name": "Technical Request",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10103",
            "id": "10103",
            "name": "Khối Sản xuất",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/11111",
        "id": "11111",
        "key": "SA",
        "name": "Thiết kế kiến trúc",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10103",
            "id": "10103",
            "name": "Khối Sản xuất",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/10133",
        "id": "10133",
        "key": "UN",
        "name": "Uncategory",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10100",
            "id": "10100",
            "name": "Ban CNTT",
            "description": ""
        },
        "projectTypeKey": "software"
    },
    {
        "expand": "description,lead,url,projectKeys",
        "self": "https://jira-ticket.misa.vn/rest/api/2/project/11108",
        "id": "11108",
        "key": "VC",
        "name": "Vantage Customize",
        "avatarUrls": {
            "48x48": "https://jira-ticket.misa.vn/secure/projectavatar?avatarId=10324",
            "24x24": "https://jira-ticket.misa.vn/secure/projectavatar?size=small&avatarId=10324",
            "16x16": "https://jira-ticket.misa.vn/secure/projectavatar?size=xsmall&avatarId=10324",
            "32x32": "https://jira-ticket.misa.vn/secure/projectavatar?size=medium&avatarId=10324"
        },
        "projectCategory": {
            "self": "https://jira-ticket.misa.vn/rest/api/2/projectCategory/10106",
            "id": "10106",
            "name": "Khối SP Doanh nghiệp",
            "description": ""
        },
        "projectTypeKey": "software"
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