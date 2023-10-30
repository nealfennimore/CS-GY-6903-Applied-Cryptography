## TLS Config

### Building

```sh
cd project5
docker build -f tls/Dockerfile -t nginx-tls ./tls
docker run --rm -i -p 4443:443 nginx-tls
```

### Testing

Start wireshark and have it listen on loopback. You'll probably need root privileges to do so.

```sh
curl -vvv -k https://localhost:4443
```

End the wireshark packet capture. Go to `File` -> `Export Specified Packets`. Update `Export as` to export as `pcap` and export.

## mTLS Config

### Building

```sh
cd project5
docker build -f mtls/Dockerfile -t nginx-mtls ./mtls
docker run --rm -i -p 4443:443 nginx-mtls
```

### Testing

Copy the client certificate to the client machine

```sh
docker cp $(docker ps --filter="ancestor=nginx-mtls" --filter="status=running" -q):/EasyRSA-3.1.7/pki/private/client.p12 /tmp/client.p12
```

Start wireshark and have it listen on loopback. You'll probably need root privileges to do so. Start the packet capture.

Use the client cert with curl. This should return a 200 status code.

```sh
curl -vvv -k \
    --cert-type P12 \
    --cert /tmp/client.p12:'' \
    https://localhost:4443
```

Without a cert, it should return a 403.

```sh
curl -vvv -k \
    https://localhost:4443
```

End the wireshark packet capture. Go to `File` -> `Export Specified Packets`. Update `Export as` to export as `pcap` and export.
