vkbackup
====
Downloads photos from VK groups

### Install
Install app dependencies
```
pip install -f requirements.pip
```

Visit the following link to acquire app permissions
```
https://oauth.vk.com/authorize?client_id=5712785&display=page&redirect_uri=http://example.com/callback&scope=262148&response_type=token
```

Grab from URL the access_token and update it in config.ini


### Usage
Download all group albums
```
python3 vkbackup.py <group>
python3 vkbackup.py 71741545
```

Download one group album
```
python3 vkbackup.py <group> <album>
python3 vkbackup.py 71741545 218786123
```
