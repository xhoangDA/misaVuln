import csv
import json
import re
import ast 
from collections import defaultdict
from typing import List, Dict, Any
from datetime import datetime
from jira_processes.jira_mapping import process_target_details
import requests

def normalize_service_name(service_name):
    """Normalize service_name field according to requirements"""
    if not service_name:
        return "Unknown"
    
    if service_name == "Unknown":
        return service_name
    
    if service_name.startswith("cpe:/a:"):
        # Extract service name from CPE format
        return service_name.replace("cpe:/a:", "")
    
    return service_name

def normalize_severity(severity):
    if severity == "info":
        return "Low"
    elif severity == "low":
        return "Low"
    elif severity == "med":
        return "Medium"
    elif severity == "high":
        return "High"
    elif severity == "critical":
        return "Critical"
    else: return "None"

def create_service_entry(service_name, port, protocol):
    """Create combined service field"""
    if not service_name:
        return "Unknown"
    return f"{port}/{protocol} - {service_name}"

def clean_hostnames(hostnames):
    """Convert hostnames array to clean string representation"""
    if not hostnames:
        return ""
    if isinstance(hostnames, str):
        # Handle string representation of array
        if hostnames.startswith('[') and hostnames.endswith(']'):
            try:
                hostnames = json.loads(hostnames.replace("'", '"'))
            except:
                hostnames = []
        else:
            return hostnames
    # Remove brackets and quotes, keep comma separation
    return str(hostnames).replace("[", "").replace("]", "").replace("'", "")

def get_cvss_value(item: Dict[str, Any]) -> str:
    """Determine the best CVSS value from available versions"""
    # Check CVSS4 first
    if item.get('cvss4_vector_string') and item.get('cvss4_base_score'):
        return f"{item['cvss4_vector_string']} - {item['cvss4_base_score']}"
    
    # Then check CVSS3
    if item.get('cvss3_vector_string') and item.get('cvss3_base_score'):
        return f"{item['cvss3_vector_string']} - {item['cvss3_base_score']}"
    
    # Finally check CVSS2
    if item.get('cvss2_vector_string') and item.get('cvss2_base_score'):
        return f"{item['cvss2_vector_string']} - {item['cvss2_base_score']}"
    
    # Return empty string if none available
    return ""

def extract_impact(data_field: str) -> str:
    """
    Trích xuất phần chuỗi bắt đầu từ "Impact: " trong field data
    Nếu không tìm thấy "Impact: " thì trả về chuỗi rỗng
    """
    if not isinstance(data_field, str):
        return ""
    
    impact_index = data_field.find("Impact: ")
    if impact_index == -1:
        return ""
    
    return data_field[impact_index:]

def format_target_detail(target_detail: list) -> str:
    """
    Chuyển đổi mảng target_detail thành chuỗi gạch đầu dòng để đưa vào issue jira
    
    Args:
        target_detail: Danh sách các service entry từ field target_detail
        
    Returns:
        Chuỗi formatted theo yêu cầu
    """
    if not target_detail:
        return ""
    
    result = []
    for entry in target_detail:
        # Thêm từng host entry
        result.append(f"\\t\\t+ {entry.strip()}")
    
    return "\n".join(result)

def process_and_group_data(data):
    """
    Process and group data according to all requirements including OS field handling
    """
    # First pass: normalize service names, create service field and CVSS value
    for item in data:
        item['service_name'] = normalize_service_name(item.get('service_name'))
        item['service'] = create_service_entry(
            item['service_name'],
            item.get('port', ''),
            item.get('protocol', '')
        )
        item['cvss'] = get_cvss_value(item)
            # Xử lý field data để lấy phần Impact
        if 'data' in item:
            item['data'] = extract_impact(item['data'])
    
    # Group by name and then by service_name
    grouped = defaultdict(lambda: defaultdict(list))
    os_values = defaultdict(set)  # To track unique OS values per name
    
    for item in data:
        item['severity'] = normalize_severity(item['severity'])
        name = item.get('name')
        if name is not None:
            service_name = item['service_name']
            grouped[name][service_name].append(item)
            if 'os' in item:
                os_values[name].add(item['os'])
    
    result = []

    for name, services in grouped.items():
        # Create base object with all fields from first item
        first_item = next(iter(services.values()))[0]
        merged = first_item.copy()
        # Handle OS field - combine unique values
        if name in os_values:
            unique_os = list(os_values[name])
            # Remove null or empty values in unique_os array
            cleaned_unique_os = list(filter(lambda x: x is not None and x != '', unique_os))
            if len(cleaned_unique_os) == 1:
                merged['os'] = cleaned_unique_os[0]
            else:
                merged['os'] = ", ".join(sorted(cleaned_unique_os))
        
        # Add our new fields
        merged['service'] = [item['service'] for items in services.values() for item in items]
        merged['target_detail'] = []

        # Process each service group
        for service_name, items in services.items():
            target_host_entries = []
            for item in items:
                target = item.get('target', '')
                name =  item.get('name', '')
                hostnames = clean_hostnames(item.get('hostnames', []))
                port_protocol = f"{item.get('port', '?')}/{item.get('protocol', '?')}" if item.get('port') or item.get('protocol') else '?/?'
                
                if target and hostnames and port_protocol:
                    entry = f"{port_protocol} - {target} - {hostnames}"
                elif target and hostnames:
                    entry = f"{target} - {hostnames}"
                elif target and port_protocol:
                    entry = f"{port_protocol} - {target}"
                elif hostnames and port_protocol:
                    entry = f"{port_protocol} - {hostnames}"
                elif target:
                    entry = target
                elif hostnames:
                    entry = hostnames
                elif port_protocol:
                    entry = port_protocol
                else:
                    continue
                
                target_host_entries.append(f"{service_name}: {entry}")

            if target_host_entries:
                merged['target_detail'] = merged['target_detail'] + target_host_entries

        # Remove only the specified fields
        fields_to_remove = { 'target', 'service_name', 'port', 'protocol', 'id', 'confirmed', 'comments', 'owner', 'easeofresolution', 'website', 'path', 'status_code', 'request', 'response', 'method', 'params', 'pname', 'query', 'policyviolations', 'external_id', 'cf_affected_software/os', 'cf_affected', 'host_id', 'host_description', 'mac', 'host_owned', 'host_creator_id', 'host_date', 'host_update_date', 'service_id', 'service_owned', 'version', 'service_date', 'service_update_date', 'service_parent_id', 'service_creator_id', 'cvss2_vector_string', 'cvss2_base_score', 'cvss3_vector_string', 'cvss3_base_score', 'cvss4_vector_string', 'cvss4_base_score', 'hostnames', 'service'}
        for field in fields_to_remove:
            if field in merged:
                del merged[field]
        
        result.append(merged)

    # Xử lý lại target_detail, chia hostname theo project dự án
    final_result = process_target_details(result)

    return final_result
    # return result

def create_jira_csv(json_file_path, csv_file_path):
    """
    Tạo file CSV theo template JIRA từ JSON output
    
    Args:
        json_file_path: Đường dẫn file JSON đầu vào
        csv_file_path: Đường dẫn file CSV đầu ra
    """
    # Đọc dữ liệu từ file JSON
    with open(json_file_path, 'r', encoding='utf-8') as f:
        json_data = json.load(f)
    
    # Xác định quý và năm hiện tại
    current_quarter = (datetime.now().month - 1) // 3 + 1
    current_year = datetime.now().year
    
    # Định nghĩa các cột trong CSV
    fieldnames = [
        "Summary", "Issue Type", "Status", "Project key", "Project name", "Priority", "Assignee", "Reporter", "Creator", "Component/s", "Custom field (Bộ phận phản ánh)", "Custom field (Ghi chú (Mô tả vấn đề))", "Custom field (Kênh hỗ trợ)", "Custom field (Loại hỗ trợ)", "Custom field (Loại lỗi)", "Custom field (Severity)", "Custom field (Thêm labels)", "Custom field (Độ khó)", "Custom field (Phân loại yêu cầu)"
    ]
    # Tạo file CSV
    with open(csv_file_path, 'w', encoding='utf-8-sig', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for item in json_data:
            # Tạo template cho trường mô tả vấn đề
            description_template = f"""Kính gửi Phòng QTHT,
Qua kết quả đánh giá an ninh TTDL Quý {current_quarter} năm {current_year}, Ban ANTT ghi nhận lỗ hổng có thông tin như sau:
\t- Name: {item.get('name', '')}
\t- CVSS: {item.get('cvss', '')}
\t- Related CVE: {item.get('cve', '')}
\t- Severity: {item.get('severity', '')}
\t- Description: {item.get('desc', '')}
\t- {item.get('data', '')}
\t- Affected OS detected: {item.get('os', '')}
\t- Affected services/hosts:
{format_target_detail(item.get('target_detail', ''))}
\t- Resolution: {item.get('resolution', '')}
Trân trọng!"""
            # Tạo row dữ liệu
            row = {
                "Project key": item.get('project_key', ''),
                "Project name":  item.get('project_name', ''),
                "Assignee":  item.get('assigned', ''),
                "Reporter": "B-1001",
                "Creator": "",
                "Issue Type": "Vấn đề của khách hàng",
                "Custom field (Kênh hỗ trợ)": "Khối sản xuất",
                "Custom field (Loại hỗ trợ)": "Lỗi phần mềm",
                "Custom field (Loại lỗi)" : "Lỗi an ninh",
                "Custom field (Độ khó)": "Trung bình",
                "Custom field (Phân loại yêu cầu)": "Bảo mật",
                "Custom field (Bộ phận phản ánh)": "TT PTPM",
                "Summary": item.get('name', ''),
                "Custom field (Ghi chú (Mô tả vấn đề))": description_template,
                "Custom field (Severity)": item.get('severity', ''),
                "Status": "Chờ xử lý",
                "Priority": "Trung bình" if item.get('severity', '').lower() in ['high', 'critical'] else "Thấp",
            }
            
            writer.writerow(row)


def csv_to_final_json(csv_file_path, json_file_path=None, indent=None):
    """
    Convert CSV to final JSON with all required transformations
    """
    # Read CSV
    with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        data = [row for row in csv_reader]
    
    # Convert string hostnames to actual arrays if needed
    for item in data:
        if 'hostnames' in item and isinstance(item['hostnames'], str):
            hostnames_str = item['hostnames'].strip()
            if hostnames_str.startswith('[') and hostnames_str.endswith(']'):
                try:
                    item['hostnames'] = json.loads(hostnames_str.replace("'", '"'))
                except json.JSONDecodeError:
                    item['hostnames'] = []
            else:
                item['hostnames'] = []
    
    # Process and group data
    processed_data = process_and_group_data(data)

    # Output or return
    if json_file_path is None:
        return processed_data
    
    with open(json_file_path, mode='w', encoding='utf-8') as json_file:
        json.dump(processed_data, json_file, indent=indent, ensure_ascii=False)
    
    print(f"Successfully processed and grouped {csv_file_path} to {json_file_path}")
    return processed_data

def json_to_csv(json_file_path, csv_file_path):
    """
    Chuyển đổi file JSON sang CSV
    
    Args:
        json_file_path (str): Đường dẫn file JSON đầu vào
        csv_file_path (str): Đường dẫn file CSV đầu ra
    """
    # Đọc dữ liệu từ file JSON
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    
    # Xác định tất cả các trường có trong dữ liệu
    fieldnames = set()
    for item in data:
        fieldnames.update(item.keys())
    fieldnames = sorted(fieldnames)
    
    # Ghi dữ liệu ra file CSV
    with open(csv_file_path, 'w', encoding='utf-8-sig', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    
    print(f"Đã chuyển đổi thành công {json_file_path} sang {csv_file_path}")

def json_to_csv_advanced(json_file_path, csv_file_path):
    """
    Chuyển đổi file JSON sang CSV với xử lý đặc biệt cho các trường phức tạp
    
    Args:
        json_file_path (str): Đường dẫn file JSON đầu vào
        csv_file_path (str): Đường dẫn file CSV đầu ra
    """
    # Đọc dữ liệu từ file JSON
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    
    # Xác định tất cả các trường có trong dữ liệu
    fieldnames = set()
    for item in data:
        fieldnames.update(item.keys())
    fieldnames = sorted(fieldnames)
    
    # Chuẩn bị dữ liệu cho CSV
    csv_data = []
    for item in data:
        csv_item = {}
        for field in fieldnames:
            if field in item:
                # Xử lý đặc biệt cho các trường phức tạp
                if field == 'target_detail' and isinstance(item[field], list):
                    # Chuyển mảng thành chuỗi phân cách bằng dấu |
                    csv_item[field] = " | ".join(item[field])
                elif field == 'service' and isinstance(item[field], list):
                    # Chuyển mảng thành chuỗi phân cách bằng dấu |
                    csv_item[field] = " | ".join(item[field])
                else:
                    csv_item[field] = item[field]
            else:
                csv_item[field] = ""
        csv_data.append(csv_item)
    
    # Ghi dữ liệu ra file CSV với encoding UTF-8
    with open(csv_file_path, 'w', encoding='utf-8-sig', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    
    # Sửa lỗi Unicode khi in thông báo
    try:
        print(f"Đã chuyển đổi thành công {json_file_path} sang {csv_file_path}")
    except UnicodeEncodeError:
        print(f"Da chuyen doi thanh cong {json_file_path} sang {csv_file_path}")
# Example usage
        

def create_jira_json(issues_data, json_file_path):
    # Mapping từ value sang id cho customfield_11801
    severity_mapping = {
        "Critical": {"id": "11805", "priority_id": "1"},
        "High": {"id": "11806", "priority_id": "2"},
        "Medium": {"id": "11807", "priority_id": "3"},
        "Low": {"id": "11808", "priority_id": "4"}
    }
    # Xác định quý và năm hiện tại
    current_quarter = (datetime.now().month - 1) // 3 + 1
    current_year = datetime.now().year

    # Template với các trường hard code
    base_template = {
        "update": {},
        "fields": {
            "issuetype": {"id": "10004"},  # Hard code
            "customfield_11001": {"id": "11202"},  # Hard code
            "customfield_11900": {"id": "11908"},  # Hard code
            "customfield_10331": {"id": "12200"},  # Hard code
            "customfield_11200": [{"id": "11400"}],  # Hard code
            "customfield_11208": {"id": "11412"},  # Hard code
            "customfield_11202": ["openvas"]  # Hard code
        }
    }

    issue_updates = []
    
    for issue_data in issues_data:
        # Tạo bản ghi mới từ template cơ bản
        new_issue = json.loads(json.dumps(base_template))  # Deep copy
        
        issue_description = f"""Kính gửi Phòng QTHT,\\r\\nQua kết quả đánh giá an ninh TTDL Quý {current_quarter} năm {current_year}, Ban ANTT ghi nhận lỗ hổng có thông tin như sau:\\r\\n\\t- Name: {issue_data.get('name', '')}\\r\\n\\t- CVSS: {issue_data.get('cvss', '')}\\r\\n\\t- Related CVE: {issue_data.get('cve', '')}\\r\\n\\t- Severity: {issue_data.get('severity', '')}\\r\\n\\t- Description: {issue_data.get('desc', '')}\\r\\n\\t- {issue_data.get('data', '')}\\r\\n\\t- Affected OS detected: {issue_data.get('os', '')}\\r\\n\\t- Affected services/hosts:\\r\\n{format_target_detail(issue_data.get('target_detail', ''))}\\r\\n\\t- Resolution: {issue_data.get('resolution', '')}\\r\\nTrân trọng!"""

        # Xử lý customfield_11801 dựa trên value
        severity_value = issue_data.get("severity")
        if severity_value in severity_mapping:
            severity_info = severity_mapping[severity_value]
            new_issue["fields"]["customfield_11801"] = {"id": severity_info["id"]}
            # Tự động set priority.id dựa trên severity
            new_issue["fields"]["priority"] = {"id": severity_info["priority_id"]}
        else:
            # Xử lý trường hợp value không hợp lệ
            new_issue["fields"]["customfield_11801"] = {"id": ""}
            new_issue["fields"]["priority"] = {"id": ""}
        
        # Cập nhật các trường khác từ dữ liệu đầu vào
        new_issue["fields"]["project"] = {"id": issue_data.get("project_id")}
        new_issue["fields"]["summary"] = issue_data.get("name")
        new_issue["fields"]["assignee"] = {"name": issue_data.get("assignee")}
        new_issue["fields"]["customfield_10206"] = issue_description
                
        issue_updates.append(new_issue)
    
        with open(json_file_path, mode='w', encoding='utf-8') as json_file:
            json.dump(issue_updates, json_file, indent=4, ensure_ascii=False)
    
    return {"issueUpdates": issue_updates}

def create_jira_issues(data_json, username, password):
    """
    Tạo issue trong JIRA từ dữ liệu JSON đã xử lý
    """
    # Đường dẫn đến API JIRA
    jira_api_url = "https://your-jira-instance/rest/api/2/issue/bulk"
    
    # Tạo yêu cầu POST đến JIRA
    headers = {
        "Content-Type": "application/json"
    }
    
    response = requests.post(jira_api_url, headers=headers, data=json.dumps(data_json), auth=(username, password))
    
    if response.status_code == 201:
        print("Issues created successfully.")
        return response.json()
    else:
        print(f"Failed to create issues: {response.status_code} - {response.text}")
        return None


if __name__ == "__main__":
    input_csv = "SR-Test.csv"
    output_json = "final_output.json"
    output_csv = "final_output.csv"
    json_file_path = "jira_import.json"

    data_json = csv_to_final_json(input_csv, output_json, indent=4)
    # json_to_csv(output_json, output_csv)
    # json_to_csv_advanced(output_json, output_csv)
    create_jira_csv('final_output.json', 'jira_import.csv')
    create_jira_json(data_json, json_file_path)