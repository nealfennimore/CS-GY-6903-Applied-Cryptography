FROM nginx:1.25.3

ADD https://github.com/OpenVPN/easy-rsa/releases/download/v3.1.7/EasyRSA-3.1.7.tgz /tmp/EasyRSA-3.1.7.tgz

RUN tar zxvf /tmp/EasyRSA-3.1.7.tgz && \
    rm /tmp/EasyRSA-3.1.7.tgz

WORKDIR /EasyRSA-3.1.7

COPY easyrsa.vars /EasyRSA-3.1.7/vars

RUN ./easyrsa init-pki && \
    echo | ./easyrsa build-ca nopass && \
    echo "yes" | ./easyrsa build-server-full "project5.local" nopass

RUN mkdir -p /etc/nginx/ssl/ && \
    cp pki/ca.crt /etc/nginx/ssl/ca.crt && \
    cp pki/issued/project5.local.crt /etc/nginx/ssl/project5.local.crt && \
    cp pki/private/project5.local.key /etc/nginx/ssl/project5.local.key && \
    chown -R nginx:nginx /etc/nginx/ssl

RUN echo "yes" | ./easyrsa --days=365 build-client-full client nopass && \
    ./easyrsa export-p12 client nopass

COPY default.conf /etc/nginx/conf.d/default.conf