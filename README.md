# certbot-dns-varo

Varo DNS Authenticator plugin for [Certbot](https://certbot.eff.org/).

Installation
------------
```
pip install certbot-dns-varo
```

Configuration
-------------
Your credentials ini file should look like this:
```
dns_varo_api_key = r4n8pvj82q8bdn120y7uzp5yayebgpju
```

Usage
-----
```
certbot certonly --authenticator dns-varo --dns-varo-credentials /path/to/your/varo.ini -d yourdomain.tld
```
