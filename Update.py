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
update_url = f'{base_url}/org-unit/update/{{id}}'


def perform_put_request(url, data):
    try:
        response = session.put(url, json=data)

        response.raise_for_status()

        print(f"Запрос выполнен успешно. Код ответа: {response.status_code}")

    except requests.exceptions.HTTPError as e:
        print(f"Ошибка при выполнении запроса: {e}")


org_unit_id_to_update = 'your_org_unit_id_here'
update_group_data = {
    "name": "Обновленная Группа Компаний",
    "type": "Группа Компаний"
}

update_organization_data = {
    "name": "Обновленная Организация",
    "type": "Организация"
}

update_department_data = {
    "name": "Обновленный Департамент",
    "type": "Департамент"
}

specific_update_url = update_url.replace('{{id}}', org_unit_id_to_update)
perform_put_request(specific_update_url, update_group_data)
perform_put_request(specific_update_url, update_organization_data)
perform_put_request(specific_update_url, update_department_data)
