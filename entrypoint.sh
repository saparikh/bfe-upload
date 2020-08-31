#!/bin/sh

# `$*` expands the `args` supplied in an `array` individually
# or splits `args` in a string separated by whitespace.


# required for SSL certificate verification to work if no DNS entry is present for Batfish Enterprise server
echo $INPUT_SERVER_IP $INPUT_SERVER_NAME |  tee -a /etc/hosts

# Install server certificate for python to use
# INPUT_SSL_CERTIFICATE MUST be a base64 encoded string version of the certificate PEM file used on the Batfish Enterprise server
# Run `base64 -i yourCA.pem`. Copy the output of into the Github secret `BFE_SSL_CERTIFICATE` of your repository and pass that as input
# to the Github action

echo $INPUT_SSL_CERTIFICATE > /scripts/serverCA_base64
base64 --decode /scripts/serverCA_base64 > /scripts/serverCA.pem
echo "Copied user SSL cert into file, installing it"
python /scripts/install_cert_python.py --cert serverCA.pem

# Upload snapshot to Batfish Enterprise server
python /scripts/upload_snapshot.py
if [ $? -eq 0 ]
then
  echo ::set-output name=status::PASS
  echo ::set-output name=URL::https://$INPUT_SERVER_NAME/dashboard/$INPUT_NETWORK_NAME/$INPUT_SNAPSHOT_NAME
else
  echo "Snapshot creation failed, exiting"
  echo ::set-output name=status::FAIL
  echo ::set-output name=url::empty
  exit 1
fi