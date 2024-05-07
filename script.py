import os
from dotenv import load_dotenv
import subprocess

def get_env(key: str) -> str:
    val = os.getenv(key)
    if val is None:
        raise Exception("{key} not found in .env")
    return val

load_dotenv('.env')
DOMAIN: str = get_env("DOMAIN")
HOSTNAMES = get_env("HOSTNAMES")
STORAGE_PATH = get_env("STORAGE_PATH")
WEBSITE_NAME = get_env("WEBSITE_NAME")
IP_ADDRESS = get_env("IP_ADDRESS")
HNS_DNS = "103.196.38.38"

TEMPLATE_DOMAIN = "$DOMAIN"
TEMPLATE_HOSTNAMES = "$HOSTNAMES"
TEMPLATE_STORAGE_PATH = "$STORAGE_PATH"
TEMPLATE_WEBSITE_NAME = "$WEBSITE_NAME"
TEMPLATE_IP_ADDRESS = "$IP"
TEMPLATE_HNS_DNS = "$HNS_DNS"


# Gen nginx.conf
def gen_nginx():
    print('Generating nginx.conf')

    with open('nginx.temp.conf', 'r') as r:
        nginx_conf = r.read()
    nginx_conf = nginx_conf.replace(TEMPLATE_HOSTNAMES, HOSTNAMES)
    with open('nginx.conf', 'w') as w:
        w.write(nginx_conf)

    print('Finish generating nginx.conf')

def gen_env():
    print('Generating mailu.env')

    with open('server.temp.env') as r:
        temp_env = r.read()
    env = temp_env.replace(TEMPLATE_HOSTNAMES, HOSTNAMES) \
                       .replace(TEMPLATE_DOMAIN, DOMAIN) \
                       .replace(TEMPLATE_WEBSITE_NAME, WEBSITE_NAME)
    with open('mailu.env', 'w') as w:
        w.write(env)

    print('Finish generating mailu.env')

def gen_cert():
    print('Generating certificates')

    subprocess.run('chmod +x gen_cert.sh'.split(' '), capture_output=True, text=True)
    cert = subprocess.run(['./gen_cert.sh', DOMAIN], capture_output=True, text=True)
    print(cert.stdout, cert.stderr)

    print('Finish generating certificates')

def gen_docker_compose():
    print('Generating docker-compose.yml')

    # yaml = ruamel.yaml.YAML()
    # yaml.preserve_quotes = True
    # yaml.indent(sequence=3, offset=1)

    # # Add configurations
    # with open("docker-compose.temp.yml", 'r') as ymlfile:
    #     data = yaml.load(ymlfile)
    # for key, service in data['services'].items():
    #     if 'dns' in service and key != 'admin':
    #         service['dns'].insert(0, HNS_DNS)
    # data['services']['front']['volumes'] += ["./cert.crt:/etc/ssl/cert.crt:ro",
    #                                          "./cert.key:/etc/ssl/cert.key:ro",
    #                                          "./nginx.conf:/etc/nginx/nginx1.conf:ro",
    #                                          "./tls.conf:/etc/nginx/tls1.conf:ro"]
    # data['services']['front']['command'] = [
    #         "/bin/sh",
    #         "-c",
    #         "/start.py & sleep 20 && cd /etc/nginx/ && rm nginx.conf && cp nginx1.conf nginx.conf && rm tls.conf && cp tls1.conf tls.conf && nginx -s reload && sleep infinity"
    #     ]
    # with open('docker-compose.yml', 'w') as w:
    #     yaml.dump(data, w)

    # Replace template
    with open('docker-compose.temp.yml', 'r') as r:
        data = r.read()
        data = data.replace(TEMPLATE_IP_ADDRESS, IP_ADDRESS) \
                   .replace(TEMPLATE_STORAGE_PATH, STORAGE_PATH) \
                   .replace(TEMPLATE_HNS_DNS, HNS_DNS)

    with open('docker-compose.yml', 'w') as w:
        w.write(data)

    print('Finish generating docker-compose.yml')

if __name__ == "__main__":
    gen_nginx()
    gen_cert()
    gen_env()
    gen_docker_compose()
