import os
import argparse

import certifi

parser = argparse.ArgumentParser(description='Install specify SSL certificate.')
parser.add_argument('-c', '--cert', help='Path the certificate PEM file', required=True)

args = parser.parse_args()

# installs the cert into the python environment

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
CA_CERT_FILE = os.path.join(SCRIPT_DIR, f"{args.cert}")

if __name__ == "__main__":
    print("Installing the certificate in {}".format(CA_CERT_FILE))

    with open(CA_CERT_FILE, "rb") as infile:
        customca = infile.read()

    with open(certifi.where(), "ab") as outfile:
        outfile.write(customca)
