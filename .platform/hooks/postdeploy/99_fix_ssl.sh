#!/bin/bash
# Fix SSL certificate errors by updating trusted certs
yum install -y ca-certificates
update-ca-trust force-enable
update-ca-trust extract
ln -sf $(python3 -m certifi) /etc/pki/tls/certs/ca-bundle.crt


