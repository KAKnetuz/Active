import requests
import OpenSSL.crypto as crypto
import logging

logging.basicConfig(level=logging.INFO)

signing_cert = 'signing-caDemo.pem'
root_cert = 'root-caDemo.pem'
pass_file = 'pass.txt'
pfx_file = 'Realm-managerDemo.pfx'
pfx_password = 'dt%ga8`g&?MU53qW'

session = requests.Session()

auth_url = 'https://demo.u-system.tech/api/v1/auth'


def authenticate_with_certificates():
    try:
        with open(signing_cert, 'rb') as signing_cert_file, \
                open(root_cert, 'rb') as root_cert_file:
            signing_cert_data = signing_cert_file.read()
            root_cert_data = root_cert_file.read()

        crypto.load_certificate(crypto.FILETYPE_PEM, signing_cert_data)
        signing_key = crypto.load_privatekey(crypto.FILETYPE_PEM, signing_cert_data)

        response = session.post(auth_url, cert=(signing_cert_data, signing_key), verify=root_cert_data)

        response.raise_for_status()
        token = response.json().get('token')
        logging.info(f"Authentication with certificates successful. Token: {token}")

    except Exception as e:
        logging.error(f"Authentication with certificates failed: {e}")


def authenticate_with_pass_file():
    try:
        with open(pass_file, 'r') as pass_file_handle:
            password = pass_file_handle.read().strip()

        response = session.post(auth_url, data={'password': password})

        response.raise_for_status()
        token = response.json().get('token')
        logging.info(f"Authentication with pass.txt successful. Token: {token}")

    except Exception as e:
        logging.error(f"Authentication with pass.txt failed: {e}")


def authenticate_with_pfx():
    try:
        pfx_data = open(pfx_file, 'rb').read()

        pfx = crypto.load_pkcs12(pfx_data, pfx_password.encode())

        cert = crypto.dump_certificate(crypto.FILETYPE_PEM, pfx.get_certificate())
        key = crypto.dump_privatekey(crypto.FILETYPE_PEM, pfx.get_privatekey())

        response = session.post(auth_url, cert=(cert, key))

        response.raise_for_status()
        token = response.json().get('token')
        logging.info(f"Authentication with Realm-managerDemo.pfx successful. Token: {token}")

    except Exception as e:
        logging.error(f"Authentication with Realm-managerDemo.pfx failed: {e}")


authenticate_with_certificates()
authenticate_with_pass_file()
authenticate_with_pfx()
