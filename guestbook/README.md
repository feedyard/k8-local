# Guestbook example local development of web ui

create local development namespace. Example assume team name is "blue"  
```bash
$ inv deploy.devns "blue-local"
```

create local domain cert. Depends on `mkcert`  
```bash
$ inv deploy.localdomain "local.guestbook.com"
```

add guestbook.localhost to hostfile. Example uses `hostess` on MacOs  
```bash
$ hostess local.guestbook.com <ingressgateway IP>
```


deploy:

- gateway
- destination rules
- redis-master
- redis-slave
- guestbook-ui
