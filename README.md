# python-http-server
A python http server written in python which creates spoofed iOS screenshots to mess with scammers and gather intel on them.

## How to run HTTP only server
### clone this repo
`git clone https://github.com/corysolovewicz/python-http-server.git`

### switch to branch 'spoof'
`cd python-http-server && git checkout spoof`

### install imagemagick
```
# install ImageMagick (ubuntu)
apt-get install ImageMagick

# install ImageMagick (centos)
yum install ImageMagick

# confirm installation
convert -version
```
```
Version: ImageMagick 6.9.10-68 Q16 x86_64 2021-10-14 https://imagemagick.org
Copyright: © 1999-2019 ImageMagick Studio LLC
License: https://imagemagick.org/script/license.php
Features: Cipher DPC Modules OpenMP(3.1) 
Delegates (built-in): bzlib cairo fontconfig freetype gslib jng jp2 jpeg lcms ltdl lzma openexr pangocairo png ps rsvg tiff wmf x xml zlib
```

## Currently the images server is only setup to run under https so you'll need to setup certs before starting

## How to run HTTPS images server
### first generate certificates
### You can either:
### 1) create a self signed certificate
`openssl req -new -x509 -keyout key.pem -out server.pem -days 365 -nodes`

### Or 2) generate one with letsencrypt certbot
```
# install certbot (ubuntu)
apt-get install certbot

# install certbot (centos)
yum install certbot python3-certbot-apache epel-release

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

### Now start your server using letsencrypt cert
`python3 https_images_server.py 0.0.0.0 443 "/etc/letsencrypt/live/example.com/fullchain.pem" "/etc/letsencrypt/live/example.com/privkey.pem"
`

### test that the server is running by going to
`https://example.com/image/IMG_1234.png`
### You should be able to the output from std output
```
[IP ADDRESS] - - [13/Mar/2023 11:58:44] "GET /image/IMG_1234.png HTTP/1.1" 200 -
INFO:root:GET request,
Path: /favicon.ico
Headers:
Host: example.com
Connection: keep-alive
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36
Accept: image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8
Sec-GPC: 1
Accept-Language: en-US,en;q=0.9
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: no-cors
Sec-Fetch-Dest: image
Referer: https://example.com/image/IMG_1234.png
Accept-Encoding: gzip, deflate, br

Body:

```


### And there should be an image which is loaded
![This is the sample image which is included](/images/IMG_1234.png)

### run https_images_server.py in the background and log to file named https_images.log
#### run in screen session so that we don't have to keep a terminal window open
`screen`

### start server in screen
### start https server on port 443 in screen writing to stdout and writing to log using tee
`python3 https_images server.py 0.0.0.0 443 /etc/letsencrypt/live/example.com/fullchain.pem /etc/letsencrypt/live/example.com/privkey.pem 2>&1 | tee -a https.log`


### disconnect from screen
`CTRL-A CTRL-D`


# Misc Notes: 
### exiftool command to remove extra exifdata for privacy purposes for an entire directory of image files
`exiftool -all:all= -overwrite_original -r <directory>`

### if you want to fingerprint the browsers of the users you will need
### to create an account and API Key for FingerPrint JS
### and add it to ./spoof/js/fingerprintjs.js
`https://dashboard.fingerprint.com/signup`

### if all you want to do is create iOS screenshots you can simply run this command after checking out the repo
`./spoof/iMessage_1.sh <filename>`
### ignore the following warning as I'm not sure how to get rid of it passing `-q` didn't seem to quiet it
```
Warning: [minor] Text/EXIF chunk(s) found after PNG IDAT (fixed) - ./images/<filename>
```
### You can find your newly created image in `<project root>/images/<filename>`