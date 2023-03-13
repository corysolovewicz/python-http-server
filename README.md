# simple-http-server
A simple http server written in python. 

## How to run HTTP only server
### clone this repo
`git clone https://github.com/corysolovewicz/python-http-server.git`

### start http only server running on specified address and port
`cd simple-http-server && python3 http_server.py [address] [port]`

## use 0.0.0.0 for world accessible or 127.0.0.1 for local only

## How to run HTTPS only server
### first generate certificates
### You can either 1) create a self signed certificate
`openssl req -new -x509 -keyout key.pem -out server.pem -days 365 -nodes`

### Or 2) generate one with letsencrypt certbot
```
# install certbot
apt-get install certbot
# run certonly option
certbot certonly
```
```
Saving debug log to /var/log/letsencrypt/letsencrypt.log
How would you like to authenticate with the ACME CA?
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
1: Apache Web Server plugin (apache)
2: Spin up a temporary webserver (standalone)
3: Place files in webroot directory (webroot)
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Select the appropriate number [1-3] then [enter] (press 'c' to cancel): 
```
### pick option 2
```
Select the appropriate number [1-3] then [enter] (press 'c' to cancel): 2
```
### set the domain to <your_domain>
```
Please enter the domain name(s) you would like on your certificate (comma and/or
space separated) (Enter 'c' to cancel): example.com
Requesting a certificate for example.com

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

Successfully received certificate.
Certificate is saved at: /etc/letsencrypt/live/example.com/fullchain.pem
Key is saved at:         /etc/letsencrypt/live/example.com/privkey.pem
This certificate expires on 2022-02-22.
These files will be updated when the certificate renews.
Certbot has set up a scheduled task to automatically renew this certificate in the background.

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
If you like Certbot, please consider supporting our work by:
 * Donating to ISRG / Let's Encrypt:   https://letsencrypt.org/donate
 * Donating to EFF:                    https://eff.org/donate-le
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

```

### Now start your server
#### using self signed cert
`python3 https_server.py 0.0.0.0 443 server.pem key.pem`

#### using letsencrypt cert
`python3 https.py 0.0.0.0 443 "/etc/letsencrypt/live/example.com/fullchain.pem" "/etc/letsencrypt/live/example.com/privkey.pem"
`

### run https.py in the background and log to file named http.log
#### run in screen session
`screen`

### start server in screen
`python3 https_server.py 0.0.0.0 443 "/etc/letsencrypt/live/example.com/fullchain.pem" "/etc/letsencrypt/live/example.com/privkey.pem" > https.log`

### or start https server on port 443 in screen writing to stdout and writing to log using tee
`python3 https_server.py 0.0.0.0 443 /etc/letsencrypt/live/example.com/fullchain.pem /etc/letsencrypt/live/example.com/privkey.pem 2>&1 | tee -a https.log`

### or start http server on port 80 in screen writing to stdout and writing to log using tee
`python3 http_server.py 0.0.0.0 80 2>&1 | tee -a http.log`

### or start https server for images on port 443 in screen 
### writing to stdout and writing to log using tee
`python3 https_images_server.py 0.0.0.0 443 /etc/letsencrypt/live/example.com/fullchain.pem /etc/letsencrypt/live/example.com/privkey.pem 2>&1 | tee -a https.log`

### disconnect from screen
`CTRL-A CTRL-D`

### exiftool command to remove extra exifdata for privacy purposes for an entire directory of image files
`exiftool -all:all= -overwrite_original -r <directory>`