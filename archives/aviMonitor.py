import requests, json, os, yaml
from shutil import copyfile
currentLeader = ''
if not os.path.exists('/etc/haproxy/haproxy.cfg.ori'):
  copyfile('/etc/haproxy/haproxy.cfg', '/etc/haproxy/haproxy.cfg.ori')
else:
# find the current avicontroller Leader configured in haproxy
  with open('haproxy.cfg') as f:
    for line in f:
      if 'aviavi' in line:
        currentLeader = line.split('aviavi ')[1].split(':')[0]
  f.close
with open("/etc/haproxy/hostAviController", 'r') as stream:
    data_loaded = yaml.load(stream)
stream.close
aviIps = [*data_loaded['all']['children']['controller']['hosts']]
ifPrimary = os.popen('ip route | grep default | sed -e "s/^.*dev.//" -e "s/.proto.*//"').read().strip('\n')
myPrimaryIp = os.popen("ifconfig " + ifPrimary + " | grep 'inet addr' | awk -F: '{print $2}' | awk '{print $1}'").read().strip('\n')

for ip in aviIps:
  try:
      response = requests.get('https://{}/api/cluster/status'.format(ip), verify=False, timeout=2)
      json_data = json.loads(response.text)
      for item in json_data['node_states']:
        # print(item)
        if item['mgmt_ip'] == ip and item['role'] == 'CLUSTER_LEADER':
          if item['mgmt_ip'] != currentLeader:
            copyfile('/etc/haproxy/haproxy.cfg.ori', '/etc/haproxy/haproxy.cfg')
            haproxyConfig = """
        frontend avivs
          bind {}:443
          mode tcp
          default_backend aviback

        backend aviback
          balance first
          mode tcp
          server aviavi {}:443
            """.format(myPrimaryIp, item['mgmt_ip'])
            with open('/etc/haproxy/haproxy.cfg', "a+") as f:
                print('Update haproxy config file with new leader {}'.format(item['mgmt_ip']))
                f.write(haproxyConfig)
            f.close
            os.popen('service haproxy restart')
            print('restart Haproxy')
  except:
      print('no https response (or cluster initializing..) from the Avi controllers: {}'.format(ip))
      pass
