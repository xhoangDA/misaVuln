import re
import requests
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class CVEScanner:
    def __init__(self):
        self.nvd_base_url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'MISA-CVE-Scanner/1.0',
            'Accept': 'application/json'
        })
    def get_cves_by_date_range(self, start_date, end_date, results_per_page=1000):
        all_cves = []
        start_index = 0
        while True:
            params = {
                'pubStartDate': f"{start_date}T00:00:00.000",
                'pubEndDate': f"{end_date}T23:59:59.999",
                'resultsPerPage': results_per_page,
                'startIndex': start_index
            }
            response = self.session.get(self.nvd_base_url, params=params, timeout=15)
            if response.status_code == 200:
                data = response.json()
                cves = data.get('vulnerabilities', [])
                all_cves.extend(cves)
                total_results = data.get('totalResults', 0)
                logger.info(f"Fetched {len(all_cves)}/{total_results} CVEs (batch size: {len(cves)})")
                if start_index + results_per_page >= total_results or not cves:
                    break
                start_index += results_per_page
            elif response.status_code == 429:
                logger.error("NVD API rate limit exceeded")
                raise Exception("NVD API rate limit exceeded. Please try again later.")
            elif response.status_code >= 500:
                logger.error(f"NVD API server error: {response.status_code}")
                raise Exception("NVD API server error. Please try again later.")
            else:
                logger.error(f"NVD API error: {response.status_code} - {response.text}")
                raise Exception(f"NVD API error: {response.status_code}")
        return all_cves
    def extract_cve_info(self, cve_data):
        try:
            cve = cve_data.get('cve', {})
            cve_id = cve.get('id', 'N/A')
            descriptions = cve.get('descriptions', [])
            description = descriptions[0].get('value', 'N/A') if descriptions else 'N/A'
            publish_date = cve.get('published', 'N/A')
            last_modified = cve.get('lastModified', 'N/A')
            metrics = cve.get('metrics', {})
            cvss_data = {}
            for version in ['cvssMetricV31', 'cvssMetricV30', 'cvssMetricV2']:
                if version in metrics and metrics[version]:
                    cvss_info = metrics[version][0].get('cvssData', {})
                    cvss_data = {
                        'version': version,
                        'baseScore': cvss_info.get('baseScore', 0.0),
                        'baseSeverity': cvss_info.get('baseSeverity', 'UNKNOWN'),
                        'attackVector': cvss_info.get('attackVector', 'UNKNOWN'),
                        'attackComplexity': cvss_info.get('attackComplexity', 'UNKNOWN'),
                        'privilegesRequired': cvss_info.get('privilegesRequired', 'UNKNOWN'),
                        'vectorString': cvss_info.get('vectorString', '')
                    }
                    break
            if not cvss_data:
                cvss_data = {
                    'version': 'unknown',
                    'baseScore': 0.0,
                    'baseSeverity': 'UNKNOWN',
                    'attackVector': 'UNKNOWN',
                    'attackComplexity': 'UNKNOWN',
                    'privilegesRequired': 'UNKNOWN',
                    'vectorString': ''
                }
            references = [ref.get('url', '') for ref in cve.get('references', [])]
            weaknesses = [w.get('description', [{}])[0].get('value', '') \
                        for w in cve.get('weaknesses', []) if w.get('description')]
            ips = self.extract_ips(description)
            for ref_url in references:
                ips.extend(self.extract_ips(ref_url))
            seen = set()
            unique_ips = [ip for ip in ips if not (ip in seen or seen.add(ip))]
            return {
                'cve_id': cve_id,
                'description': description,
                'publish_date': publish_date,
                'last_modified': last_modified,
                'cvss_data': cvss_data,
                'references': references,
                'weaknesses': weaknesses,
                'source_identifier': cve.get('sourceIdentifier', ''),
                'vuln_status': cve.get('vulnStatus', ''),
                'related_ips': unique_ips
            }
        except Exception as e:
            logger.error(f"Error extracting CVE info: {str(e)}")
            return {
                'cve_id': cve_data.get('cve', {}).get('id', 'ERROR'),
                'description': f"Error parsing CVE data: {str(e)}",
                'publish_date': 'N/A',
                'last_modified': 'N/A',
                'cvss_data': {'baseScore': 0.0, 'baseSeverity': 'UNKNOWN'},
                'references': [],
                'weaknesses': [],
                'related_ips': []
            }
    def extract_ips(self, text):
        if not text:
            return []
        ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
        ips = re.findall(ip_pattern, text)
        valid_ips = []
        for ip in ips:
            octets = ip.split('.')
            if all(0 <= int(octet) <= 255 for octet in octets):
                valid_ips.append(ip)
        return valid_ips
    def analyze_technology_vulnerability(self, technology, cve_info):
        pass
    def is_version_affected(self, current_version, min_version, max_version):
        pass

def check_component_vulnerability(component_name, cve_description):
    return component_name.lower() in cve_description.lower()
