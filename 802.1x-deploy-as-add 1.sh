#!/bin/bash

#Created by: Joseph Pumphrey
#Date: 8/4/2023
#Deployment script to configure a RHEL host for 802.1x network authentication. A new connection profile is created using the client cert/key and root CA.

exec &> /root/802.1x-deploy.out

CLIENT_CERT="/var/centrify/net/certs/auto_WC-Domain-Autoenroll-v1.1.cert"
CLIENT_KEY="/var/centrify/net/certs/auto_WC-Domain-Autoenroll-v1.1.key"
CLIENT_KEY_ENC="/var/centrify/net/certs/auto_WC-Domain-Autoenroll-v1.1.encrypted.key"

#### NOTE: You don't need to manually distribute the NREN root CA for this but it will work. It is better practice to point NM directly to the CA path assuming it is managed by a domain integration application like Centrify or SSSD.
ROOT_CA="/etc/pki/tls/certs/NREN-Root-CA.cert"
CA_PATH="/var/centrify/net/certs"


if ! [ -f $CLIENT_KEY ]; then
  echo "Error: Client private key does not exist."
  exit 1;
fi
if ! [ -f $ROOT_CA ]; then
  echo "Error: NREN Root CA certificate does not exist."
  exit 1;
fi
if ! [ -f $CLIENT_CERT ]; then
  echo "Error: Client certificate does not exist."
  exit 1;
fi

IFS=$'\n'
CON_LIST=$(nmcli -t -f UUID con show --active)

#echo $CON_LIST

openssl pkcs8 -topk8 -v2 aes256 -passout pass:<putpasswordhere> -in $CLIENT_KEY -out $CLIENT_KEY_ENC

chmod 400 $CLIENT_KEY_ENC

for i in $CON_LIST; do
  CON=$(echo $i | cut -d " " -f 1)
  #echo $CON
  nmcli con show $CON | grep -i nren.navy.mil > /dev/null
  if [ $? == 0 ]; then
    DEV=$(nmcli -t --fields UUID,DEVICE con show | grep $CON | cut -d ':' -f 2)
    #echo $DEV
    break
  fi
done

if [ -z "${DEV}" ]; then
  echo "Error: Unable to determine suitable network device."
  exit 1;
fi

#echo $DEV

nmcli con mod $CON connection.autoconnect no


### To use the CA path instead of the NREN root CA directly, replace 802-1x.ca-cert with 802-1x.ca-path.
if nmcli con show | grep dot1x-nren > /dev/null; then
  nmcli con mod dot1x-nren connection.autoconnect yes 802-1x.eap tls 802-1x.identity $HOSTNAME 802-1x.domain-suffix-match nren.navy.mil 802-1x.ca-cert $ROOT_CA 802-1x.client-cert $CLIENT_CERT 802-1x.private-key $CLIENT_KEY_ENC 802-1x.private-key-password <putpasswordhere>
else
  nmcli con add type ethernet ifname $DEV con-name dot1x-nren connection.autoconnect yes 802-1x.eap tls 802-1x.identity $HOSTNAME 802-1x.domain-suffix-match nren.navy.mil 802-1x.ca-cert $ROOT_CA 802-1x.client-cert $CLIENT_CERT 802-1x.private-key $CLIENT_KEY_ENC 802-1x.private-key-password <putpasswordhere>
fi

if ! nmcli con show | grep dot1x-nren > /dev/null; then
  echo "Error: dot1x-nren network connection profile failed to be created. Please address configuration manually."
  exit 1;
fi

nmcli con down $CON
nmcli con up dot1x-nren




