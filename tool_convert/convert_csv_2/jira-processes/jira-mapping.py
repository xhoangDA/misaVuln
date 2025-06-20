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

# Sử dụng
mapping = load_mapping('jira_assign_mapping.txt') 
print(mapping)
# Kết quả: {'FO': 'user1', 'AIMS': 'ai_owner', 'HRM': 'hrm_manager', 'MISA': 'admin'}

def assign_issue(project_key, mapping_dict, default_user='admin'):
    """Tự động assign issue dựa trên project key"""
    return mapping_dict.get(project_key, default_user)

# Ví dụ sử dụng
print(assign_issue('FO', mapping))  # -> user1
print(assign_issue('UNKNOWN', mapping))  # -> admin (default)