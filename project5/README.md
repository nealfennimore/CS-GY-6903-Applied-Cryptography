## TLS Config

### Running

```sh
cd project5
docker build -f Dockerfile-TLS -t nginx-tls  .
docker run --rm -i -p 4443:443 nginx-tls
```

### Testing

```sh
curl -vvv -k https://localhost:4443
```
