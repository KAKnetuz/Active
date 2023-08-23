import requests
import OpenSSL.crypto as crypto

pfx_file = 'Realm-managerDemo.pfx'
pfx_password = 'your_pfx_password_here'
pfx = crypto.load_pkcs12(open(pfx_file, 'rb').read(), pfx_password.encode())

cert = crypto.dump_certificate(crypto.FILETYPE_PEM, pfx.get_certificate())
key = crypto.dump_privatekey(crypto.FILETYPE_PEM, pfx.get_privatekey())

session = requests.Session()
session.cert = (cert, key)

base_url = 'https://demo.u-system.tech/api/v1'
delete_url = f'{base_url}/org-unit/delete/{{id}}'


def perform_delete_request(url):
    try:
        response = session.delete(url)

        response.raise_for_status()

        print(f"Удаление выполнено успешно. Код ответа: {response.status_code}")

    except requests.exceptions.HTTPError as e:
        print(f"Ошибка при выполнении запроса: {e}")


org_unit_id_to_delete = 'your_org_unit_id_here'

specific_delete_url = delete_url.replace('{{id}}', org_unit_id_to_delete)
perform_delete_request(specific_delete_url)
