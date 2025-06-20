import csv
import json
import re
import ast 
from collections import defaultdict
from typing import List, Dict, Any
from datetime import datetime

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

def format_affected_services(target_detail: list) -> str:
    """
    Chuyển đổi target_detail thành chuỗi affected_services_host theo định dạng đơn giản
    
    Args:
        target_detail: Danh sách các service entry từ field target_detail
        
    Returns:
        Chuỗi formatted theo yêu cầu
    """
    if not target_detail:
        return ""
    
    result = []
    for entry in target_detail:
        if not isinstance(entry, str):
            continue
            
        # Tìm vị trí dấu : cuối cùng
        last_colon_index = entry.rfind(':')
        if last_colon_index == -1:
            continue
            
        # Tách service_name (từ đầu đến dấu : cuối cùng)
        service_name = entry[:last_colon_index].strip()
        
        # Phần còn lại là hosts_part (từ dấu : cuối cùng đến hết)
        hosts_part = entry[last_colon_index + 1:].strip()
        
        # Làm sạch hosts_part (bỏ dấu ngoặc vuông và dấu ngoặc kép)
        hosts_list = []
        if hosts_part.startswith('[') and hosts_part.endswith(']'):
            try:
                # Thử parse bằng json nếu có định dạng JSON hợp lệ
                hosts_list = json.loads(hosts_part)
            except json.JSONDecodeError:
                # Fallback: xử lý thủ công nếu không phải JSON chuẩn
                hosts_part = hosts_part[1:-1]  # Bỏ dấu ngoặc vuông
                hosts_list = [h.strip(' "\'') for h in hosts_part.split(',')]
        
        # Thêm service name vào kết quả
        result.append(f"\tService: {service_name}")
        
        # Thêm từng host entry
        for host in hosts_list:
            result.append(f"\t\t+ {host.strip()}")
    
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
                hostnames = clean_hostnames(item.get('hostnames', []))
                port_protocol = f"{item.get('port', '')}/{item.get('protocol', '')}"
                
                if target and hostnames and port_protocol:
                    entry = f"{target} - {hostnames} - {port_protocol}"
                elif target and hostnames:
                    entry = f"{target} - {hostnames}"
                elif target and port_protocol:
                    entry = f"{target} - {port_protocol}"
                elif hostnames and port_protocol:
                    entry = f"{hostnames} - {port_protocol}"
                elif target:
                    entry = target
                elif hostnames:
                    entry = hostnames
                elif port_protocol:
                    entry = port_protocol
                else:
                    continue
                
                target_host_entries.append(entry)
            
            if target_host_entries:
                service_entry = f"{service_name}: {json.dumps(target_host_entries)}"
                merged['target_detail'].append(service_entry)

        # Thêm field affected_services_host
        if 'target_detail' in merged:
            merged['affected_services_host'] = format_affected_services(merged['target_detail'])

        # Remove only the specified fields
        fields_to_remove = { 'target', 'service_name', 'port', 'protocol', 'id', 'service', 'confirmed', 'comments', 'owner', 'easeofresolution', 'website', 'path', 'status_code', 'request', 'response', 'method', 'params', 'pname', 'query', 'policyviolations', 'external_id', 'cf_affected_software/os', 'cf_affected', 'host_id', 'host_description', 'mac', 'host_owned', 'host_creator_id', 'host_date', 'host_update_date', 'service_id', 'service_owned', 'version', 'service_date', 'service_update_date', 'service_parent_id', 'service_creator_id', 'cvss2_vector_string', 'cvss2_base_score', 'cvss3_vector_string', 'cvss3_base_score', 'cvss4_vector_string', 'cvss4_base_score'}
        for field in fields_to_remove:
            if field in merged:
                del merged[field]
        
        result.append(merged)
    
    return result

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
    
    # Xác định quý hiện tại
    current_quarter = (datetime.now().month - 1) // 3 + 1
    
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
Qua kết quả đánh giá an ninh TTDL Quý {current_quarter}, Ban ANTT có ghi nhận lỗ hổng có thông tin như sau:
- Name: "{item.get('name', '')}"
- CVSS: {item.get('cvss', '')}
- Related CVE: {item.get('cve', '')}
- Severity: {normalize_severity(item.get('severity', ''))}
- Description: {item.get('desc', '')}
- Impact: {item.get('data', '')}
- Affected OS detected: {item.get('os', '')}
- Affected services/hosts:
{item.get('affected_services_host', '')}
- Resolution: {item.get('resolution', '')}"""
            
            # Tạo row dữ liệu
            row = {
                # "Project key": "QVA",
                # "Project name": "General",
                "Assignee": "",
                "Reporter": "",
                "Creator": "",
                "Assignee": "",
                "Assignee": "",
                "Issue Type": "Vấn đề của khách hàng",
                "Custom field (Kênh hỗ trợ)": "Khối sản xuất",
                "Custom field (Loại hỗ trợ)": "Lỗi phần mềm",
                "Custom field (Loại lỗi)" : "Lỗi an ninh",
                "Custom field (Độ khó)": "Trung bình",
                "Custom field (Phân loại yêu cầu)": "Bảo mật",
                "Custom field (Bộ phận phản ánh)": "TT PTPM",
                "Summary": item.get('name', ''),
                "Custom field (Ghi chú (Mô tả vấn đề))": description_template,
                "Custom field (Severity)": normalize_severity(item.get('severity', '')),
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
if __name__ == "__main__":
    input_csv = "SR-Test.csv"
    output_json = "final_output1.json"
    output_csv = "final_output.csv"

    csv_to_final_json(input_csv, output_json, indent=4)
    # json_to_csv(output_json, output_csv)
    # json_to_csv_advanced(output_json, output_csv)
    create_jira_csv('final_output.json', 'jira_import.csv')