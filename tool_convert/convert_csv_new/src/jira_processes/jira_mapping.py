import json
from collections import defaultdict

def load_mapping(file_path):
    """Đọc file mapping dạng key:value"""
    mapping = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            # Bỏ qua dòng trống và comment
            if not line or line.startswith('#'):
                continue
            # Tách key-value
            if ':' in line:
                key, value = line.split(':', 1)
                mapping[key.strip()] = value.strip()
    return mapping

def assign_issue(project_key, file_path="D:/my tools/convert_csv/jira_processes/jira_assign_mapping.txt", default_user='admin'):
    """Tự động assign issue dựa trên project key"""
    mapping_dict = load_mapping(file_path)
    return mapping_dict.get(project_key, default_user)

def host_to_project(hostname, mapping_file_path="D:/my tools/convert_csv/jira_processes/hostname_mapping.txt", default_project="SRE"):
    """
    Chuyển đổi hostname thành tên project dựa trên các quy tắc ánh xạ.
    
    Tham số:
        hostname (str): Hostname cần kiểm tra
        mapping_file_path (str): Đường dẫn tới file chứa ánh xạ
        default_project (str): Project mặc định nếu không tìm thấy kết quả khớp (mặc định: "SRE")
    
    Trả về:
        str: Tên project tương ứng
    """
    # Tải ánh xạ từ file
    mapping = load_mapping(mapping_file_path)
    
    # Kiểm tra từng key trong ánh xạ xem có xuất hiện trong hostname không
    for key in mapping:
        if key in hostname:
            return mapping[key]
    
    # Nếu không tìm thấy kết quả khớp, trả về project mặc định
    return default_project

def project_key_to_id(project_key, file_json_path = "D:/my tools/convert_csv/jira_processes/jira-projects.json"):
    """
    Tìm project name tương ứng với project key trong file JSON
    
    Args:
        project_key (str): Key của project cần tìm (ví dụ: "FO", "AIMS")
        file_json_path (str): Đường dẫn đến file JSON chứa danh sách project
    
    Returns:
        str: Tên project tương ứng nếu tìm thấy, None nếu không tìm thấy
    
    Raises:
        FileNotFoundError: Nếu file JSON không tồn tại
        json.JSONDecodeError: Nếu file JSON không đúng định dạng
    """
    try:
        # Đọc nội dung file JSON
        with open(file_json_path, 'r', encoding='utf-8') as f:
            projects = json.load(f)
        
        # Tìm project có key trùng khớp
        for project in projects:
            if project.get('key') == project_key:
                return project.get('id')
        
        # Nếu không tìm thấy
        return None
        
    except FileNotFoundError:
        raise FileNotFoundError(f"Không tìm thấy file: {file_json_path}")
    except json.JSONDecodeError:
        raise ValueError("File JSON không đúng định dạng")

def process_target_details(json_array, mapping_file_path = "D:/my tools/convert_csv/jira_processes/hostname_mapping.txt"):
    """
    Xử lý mảng JSON, nhóm các target_detail theo project name
    
    Args:
        json_array (list): Mảng JSON đầu vào
        mapping_file_path (str): Đường dẫn file mapping hostname-project
    
    Returns:
        list: Mảng JSON đã được xử lý, nhóm theo project name
    """
    result = []
    
    for item in json_array:
        if not item.get('target_detail'):
            # Nếu không có target_detail, giữ nguyên bản ghi
            result.append(item)
            continue
            
        # Tạo dict để nhóm các target_detail theo project
        project_groups = defaultdict(list)
        
        for target in item['target_detail']:
            # Lấy hostname (phần sau dấu '-' cuối cùng)
            hostname = target.split(' - ')[-1].strip()
            
            # Xác định project name
            project_key = host_to_project(hostname, mapping_file_path)
            # Thêm vào nhóm tương ứng
            project_groups[project_key].append(target)
        
        if len(project_groups) == 1:
            # Nếu tất cả cùng 1 project, thêm field project_key
            project_key = next(iter(project_groups))
            new_item = item.copy()
            new_item['project_key'] = project_key
            new_item['project_name'] = project_key_to_id(project_key)
            new_item['target_detail'] = project_groups[project_key]
            new_item['assigned'] = assign_issue(project_key)
            result.append(new_item)
        else:
            # Nếu nhiều project, clone bản ghi cho từng project
            for project_key, targets in project_groups.items():
                new_item = item.copy()
                new_item['project_key'] = project_key
                new_item['project_id'] = project_key_to_id(project_key)
                new_item['target_detail'] = targets
                new_item['assigned'] = assign_issue(project_key)
                result.append(new_item)
    
    return result

# Ví dụ sử dụng
if __name__ == '__main__':

    # Đường dẫn đến file JSON
    project_name = project_key_to_id("FO")
    
    # Sửa lỗi Unicode khi in thông báo
    try:
        # Tìm tên project với key "FO"
        print(f"Project name: {project_name}")  # Kết quả: "5FOOD"
        
        # Test với key không tồn tại
        print(project_key_to_id("XYZ"))  # Kết quả: None
    except UnicodeEncodeError:
        # Tìm tên project với key "FO"
        print(f"Project name: {project_name}")  # Kết quả: "5FOOD"
        
        # Test với key không tồn tại
        print(project_key_to_id("XYZ"))  # Kết quả: None