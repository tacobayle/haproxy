import requests, json, sys
ip = sys.argv[1]
response = requests.get('https://{}/api/cluster/status'.format(ip), verify=False, timeout=2)
json_data = json.loads(response.text)
for item in json_data['node_states']:
  if item['role'] == 'CLUSTER_LEADER':
    if item['mgmt_ip'] == ip:
      sys.exit(0)
    else:
      sys.exit(43)
