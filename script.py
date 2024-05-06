import os
from dotenv import load_dotenv
import subprocess
import ruamel.yaml
import sys

def get_env(key: str) -> str:
    val = os.getenv(key)
    if val is None:
        raise Exception("{key} not found in mailu.env")
    return val

load_dotenv('mailu.env')
domain: str = get_env("DOMAIN")
hostnames = get_env("HOSTNAMES")

TEMPLATE_DOMAIN = "moon.allinpepetothemoon"
TEMPLATE_HOSTNAMES = "mail.moon.allinpepetothemoon"
TEMPLATE_IP = "14.225.217.169"
HNS_DNS = "103.196.38.38"

def gen_cert():
    # Gen nginx.conf
    with open('nginx.temp.conf', 'r') as r:
        nginx_conf = r.read()
    nginx_conf = nginx_conf.replace(TEMPLATE_HOSTNAMES, hostnames)
    with open('nginx.conf', 'w') as w:
        w.write(nginx_conf)

    # Gen cert
    subprocess.run('chmod +x gen_cert.sh'.split(' '), capture_output=True, text=True)
    cert = subprocess.run(['./gen_cert.sh', domain], capture_output=True, text=True)
    print(cert.stdout, cert.stderr)

def gen_docker_compose():
    yaml = ruamel.yaml.YAML()
    yaml.preserve_quotes = True
    yaml.indent(sequence=3, offset=1)

    with open("docker-compose.yml", 'r') as ymlfile:
        data = yaml.load(ymlfile)

    for key, service in data['services'].items():
        if 'dns' in service and key != 'admin':
            service['dns'].insert(0, HNS_DNS)

    data['services']['front']['volumes'] += ["./cert.crt:/etc/ssl/cert.crt:ro",
                                             "./cert.key:/etc/ssl/cert.key:ro",
                                             "./nginx.conf:/etc/nginx/nginx1.conf:ro",
                                             "./tls.conf:/etc/nginx/tls1.conf:ro"]
    data['services']['front']['command'] = [
            "/bin/sh",
            "-c",
            "/start.py & sleep 20 && cd /etc/nginx/ && rm nginx.conf && cp nginx1.conf nginx.conf && rm tls.conf && cp tls1.conf tls.conf && nginx -s reload && sleep infinity"
        ]
    with open('docker-compose.yml', 'w') as w:
        yaml.dump(data, w)

if __name__ == "__main__":
    gen_cert()
    gen_docker_compose()
