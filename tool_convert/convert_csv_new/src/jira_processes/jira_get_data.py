import sys
import io
import json
import requests
from time import sleep
from src.utils.constants import JIRAConstants, DirectoryDefault

def list_projects(url,  username, password):
    """
    Liệt kê tất cả các project trong Jira
    Args:
        url (str): Địa chỉ URL của Jira
        username (str): Thông tin username xác thực tới Jira
        password (str): Thông tin password xác thực tới Jira
    Returns:
        list: Danh sách các project
    """
    response = requests.get(f"{url}{JIRAConstants.PROJECTS_ENDPOINT}", auth=(username, password))
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Lỗi khi lấy dữ liệu: {response.status_code} - {response.text}")
        return []
    
def save_projects_to_file(projects_json, file_path = DirectoryDefault.JIRA_PROJECTS_JSON):
    data = json.loads(projects_json)
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

    with open(file_path, mode='w', encoding='utf-8') as json_file:
        json.dump(result, json_file, indent=2, ensure_ascii=False)

def list_users(url, username, password):
    """
    Liệt kê tất cả các người dùng trong Jira
    Args:
        url (str): Địa chỉ URL của Jira
        username (str): Thông tin username xác thực tới Jira
        password (str): Thông tin password xác thực tới Jira
    Returns:
        list: Danh sách các người dùng
    """
    all_users = []
    start_at = 0
    max_results = 1000  # Số bản ghi tối đa mỗi request
    has_more = True
    
    while has_more:
        try:
            response = requests.get(f"{url}{JIRAConstants.USER_SEARCH_ENDPOINT}?username=.&maxResults=1000&includeInactive=true&startAt={start_at}", auth=(username, password))
            response.raise_for_status()  # Kiểm tra lỗi HTTP
            
            users = response.json()
            if not users:  # Không còn user nào
                has_more = False
                break
                
            all_users.extend(users)
            
            # Nếu số user nhận được ít hơn max_results, có thể đã hết user
            if len(users) < max_results:
                has_more = False
            else:
                start_at += max_results
                
            # Tránh rate limiting
            sleep(0.2)
            
        except requests.exceptions.RequestException as e:
            print(f"Lỗi khi lấy dữ liệu: {e}")
            break
    return all_users

def save_user_to_file(users_json, file_path = DirectoryDefault.JIRA_USERS_JSON):
    data = json.loads(users_json)
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    result = []
    for item in data:
        extracted = {
            'key': item.get('key'),
            'name': item.get('name'),
            'displayName': item.get('displayName')
        }
        result.append(extracted)

    with open(file_path, mode='w', encoding='utf-8') as json_file:
        json.dump(result, json_file, indent=4, ensure_ascii=False)
