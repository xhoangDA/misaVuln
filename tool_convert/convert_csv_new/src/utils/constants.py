from enum import Enum

class JIRAConstants:
    DEFAULT_PAGE_SIZE = 1000
    USER_SEARCH_ENDPOINT = "/rest/api/2/user/search"
    PROJECTS_ENDPOINT = "/rest/api/2/project"

class DirectoryDefault:
    USER_DIR = "users"
    PROJECT_DIR = "projects"
    ISSUE_DIR = "issues"
    JIRA_DIR = "jira"
    JIRA_PROJECTS_JSON = "../../intput/jira-projects.json"
    JIRA_USERS_JSON = "../../intput/jira-users.json"
    JIRA_ISSUES_JSON = "jira-issues.json"
    JIRA_ASSIGN_MAPPING_TXT = "../../intput/jira_assign_mapping.txt"
    HOSTNAME_MAPPING_TXT = "../../intput/hostname_mapping.txt"