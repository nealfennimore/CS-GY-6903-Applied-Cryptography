FROM nginx:1.25.3

RUN mkdir -p /etc/nginx/ssl/ && \
    openssl ecparam -genkey -name secp384r1 -out project5.local.key && \
    openssl ec -in project5.local.key -text -noout  && \
    openssl req -new -sha256 -key project5.local.key -subj "/CN=project5.local/C=US/ST=A/L=B/O=Org/OU=project5" -out project5.local.csr && \
    openssl req -in project5.local.csr -text -noout | grep -i "Signature.*SHA256" && echo "All is well" && \
    openssl req -x509 -sha256 -days 365 -key project5.local.key -in project5.local.csr -out project5.local.crt && \
    mv project5.local.crt project5.local.key /etc/nginx/ssl/

RUN chown -R nginx:nginx /etc/nginx/ssl/

COPY default.conf /etc/nginx/conf.d/default.conf