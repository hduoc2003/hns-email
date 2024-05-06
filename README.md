# MoonMail - Docker based mail server with Handshake domain

## Introduction

MoonMail is built on top of [Mailu](https://mailu.io/2.0/). It is a simple yet full-featured mail server as a set of Docker images. We've enhanced Mailu to support interaction with **Handshake** domains, including:
- Automatically issuing TLS certificates for Handshake domains.
- Exclusively engage with Handshake HNS domain names, guaranteeing compatibility and full support within the Handshake ecosystem.

Main features include:
- **E2E Encryption**, secure email communications, safeguarding the privacy and confidentiality of messages exchanged.
- **Standard email server**, IMAP and IMAP+, SMTP and Submission with autoconfiguration profiles for clients
- **Advanced email features**, aliases, domain aliases, custom routing
- **Web access**, multiple Webmails and administration interface
- **User features**, aliases, auto-reply, auto-forward, fetched accounts
- **Admin features**, global admins, announcements, per-domain delegation, quotas
- **Security**, enforced TLS, DANE, MTA-STS, Letsencrypt!, outgoing DKIM, anti-virus scanner, [Snuffleupagus](https://github.com/jvoisin/snuffleupagus/), block malicious attachments
- **Antispam**, auto-learn, greylisting, DMARC and SPF, anti-spoofing
- **Freedom**, all FOSS components, no tracker included

## Setup

First, you need to clone this repository. We will use an Ubuntu server, `moon.allinpepetothemoon` as the domain name, and `14.225.217.169` as the IP address.

### Prerequisites

- Docker CLI
- Python 3, pip, python venv
- Root user

### Setup DNS records

We use [Namebase.io](https://www.namebase.io/) as Handshake domain provider. We need to add a few records as follows:
![](Pasted%20image%2020240506120538.png)
![](Pasted%20image%2020240506120551.png)
![](Pasted%20image%2020240506120618.png)

### Setup a new mail server

#### Generate configuration files

We use [Mailu configuration](https://setup.mailu.io/2.0/) website to to generate the necessary environment configuration variables.

##### Step 1 - Initial configuration

Fill in the fields in the below image with your own values.

![](step%201.png)

##### Step 2 - Pick some features

![](step%202.png)

##### Step 3 - Expose MoonMail to the world

![](Pasted%20image%2020240506110019.png)

And click to `Setup Mailu` button.

##### Step 4 - Download configuration files

Download file `mailu.env` and `docker-compose.yml` using the `wget` command provided on the website.

#### Run setup script

First, create `venv` and install necessary python packages

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt 
python script.py
```

After running this, the following files will be created: 
- `cert.key` (private key) 
- `cert.crt` (public key)
- `nginx.conf`
- `tlsa`
and your `docker-compose.yml` will be modified. Then copy `tlsa` file content and add a DNS record as follow:
![](Pasted%20image%2020240506135913.png)
Run
```
docker compose up -d
```

Before you can use MoonMail, you must create the primary administrator user account. This should be admin@moon.allinpepetothemoon. Use the following command, changing PASSWORD to your liking:
```
docker compose exec admin flask mailu admin admin moon.allinpepetothemoon PASSWORD
```

Then access your domain with HTTPS, and the website interface will look like this

![](Pasted%20image%2020240506141053.png)

