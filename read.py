import requests
import OpenSSL.crypto as crypto

pfx_file = 'Realm-managerDemo.pfx'
pfx_password = 'your_pfx_password_here'

pfx = crypto.load_pkcs12(open(pfx_file, 'rb').read(), pfx_password.encode())

cert = crypto.dump_certificate(crypto.FILETYPE_PEM, pfx.get_certificate())
key = crypto.dump_privatekey(crypto.FILETYPE_PEM, pfx.get_privatekey())

session = requests.Session()
session.cert = (cert, key)

# URL для API
base_url = 'https://demo.u-system.tech/api/v1'
get_all_url = f'{base_url}/org-unit/get-all'
get_url = f'{base_url}/org-unit/get/{{id}}'
get_children_url = f'{base_url}/org-unit/get-children/{{id}}'
get_parents_url = f'{base_url}/org-unit/get-parents/{{id}}'


def perform_get_request(url):
    try:
        response = session.get(url)

        response.raise_for_status()


                print(f"Запрос выполнен успешно. Код ответа: {response.status_code}")

    except requests.exceptions.HTTPError as e:
        print(f"Ошибка при выполнении запроса: {e}")


perform_get_request(get_all_url)

org_unit_id = 'your_org_unit_id_here'
specific_get_url = get_url.replace('{{id}}', org_unit_id)
perform_get_request(specific_get_url)

child_org_unit_id = 'your_child_org_unit_id_here'
specific_get_children_url = get_children_url.replace('{{id}}', child_org_unit_id)
perform_get_request(specific_get_children_url)

parent_org_unit_id = 'your_parent_org_unit_id_here'
specific_get_parents_url = get_parents_url.replace('{{id}}', parent_org_unit_id)
perform_get_request(specific_get_parents_url)
