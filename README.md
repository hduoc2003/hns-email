# MoonMail - Docker based mail server with Handshake domain

## Introduction

MoonMail is built on top of [Mailu](attachments/https://mailu.io/2.0/). It is a simple yet full-featured mail server as a set of Docker images. We've enhanced Mailu to support interaction with **Handshake** domains, including:
- Automatically issuing TLS certificates for Handshake domains.
- Exclusively engage with Handshake HNS domain names, guaranteeing compatibility and full support within the Handshake ecosystem.

Main features include:
- **E2E Encryption**, secure email communications, safeguarding the privacy and confidentiality of messages exchanged.
- **Standard email server**, IMAP and IMAP+, SMTP and Submission with autoconfiguration profiles for clients
- **Advanced email features**, aliases, domain aliases, custom routing
- **Web access**, multiple Webmails and administration interface
- **User features**, aliases, auto-reply, auto-forward, fetched accounts
- **Admin features**, global admins, announcements, per-domain delegation, quotas
- **Security**, enforced TLS, DANE, MTA-STS, Letsencrypt!, outgoing DKIM, anti-virus scanner, [Snuffleupagus](attachments/https://github.com/jvoisin/snuffleupagus/), block malicious attachments
- **Antispam**, auto-learn, greylisting, DMARC and SPF, anti-spoofing
- **Freedom**, all FOSS components, no tracker included

## Setup

First, you need to clone this repository. We will use an Ubuntu server, `moon.allinpepetothemoon` as the domain name, and `14.225.217.169` as the IP address.

### Prerequisites

- Docker CLI
- Python 3, pip, python venv
- Root user

### Setup [HNSD](https://github.com/handshake-org/hnsd) for DNS resolution

Run HNSD locally
```bash
docker run -d --name hnsd --restart always -p 53:53/udp namebasehq/hnsd "/opt/hnsd/dist/hnsd" -p 4 -r 0.0.0.0:53
```

Add the following line to the top of the `/etc/resolv.conf` file
```
nameserver 127.0.0.1
```

It took a while for HNSD to finish running. You can `ping` a Handshake domain to check everything is working properly
```bash
ping mail.moon.allinpepetothemoon
```

### Setup DNS records

We use [Namebase.io](attachments/https://www.namebase.io/) as Handshake domain provider. We need to add a few records as follows:
![](attachments/Pasted%20image%2020240506120538.png)
![](attachments/Pasted%20image%2020240506120551.png)
![](attachments/Pasted%20image%2020240506120618.png)

### Setup a new mail server

First, create an `.env` file in the root directory of the repository as shown below

```ini
STORAGE_PATH=/moonmail

DOMAIN=moon.allinpepetothemoon

WEBSITE_NAME="Moon Mail"

IP_ADDRESS=14.225.217.169

HOSTNAMES=mail.moon.allinpepetothemoon
```

Then, create `venv` and install necessary python packages

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt 
python script.py
```

After running these commands, the following files will be created: 
- `cert.key` (private key) 
- `cert.crt` (public key)
- `tlsa`
- `nginx.conf`
- `mailu.env`
- `docker-compose.yml`

Then copy `tlsa` file content and add a DNS record as follow:
![](attachments/Pasted%20image%2020240506135913.png)
Run
```bash
docker compose up -d
```

Before you can use MoonMail, you must create the primary administrator user account. This should look like admin@moon.allinpepetothemoon. Use the following command, changing PASSWORD to your liking:
```bash
docker compose exec admin flask mailu admin admin moon.allinpepetothemoon PASSWORD
```

Then access your domain with HTTPS, and the website interface will look like this

![](attachments/Pasted%20image%2020240506141053.png)

## Demo 
### Sending emails to other email server used handshake domain
[demo_sending_emails](https://www.youtube.com/watch?v=OjO4SZG7zaE)


