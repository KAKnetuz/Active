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
create_url = f'{base_url}/org-unit/create'


def create_org_unit(data):
    try:
        response = session.post(create_url, json=data)

        # Проверка кода ответа (должен быть 201 - Created)
        response.raise_for_status()

        print(f"Организационная единица создана успешно. Код ответа: {response.status_code}")

    except requests.exceptions.HTTPError as e:
        print(f"Ошибка при создании организационной единицы: {e}")


create_group_data = {
    "name": "Новая Группа Компаний",
    "type": "Группа Компаний"
}

create_organization_data = {
    "name": "Новая Организация",
    "type": "Организация"
}

create_department_data = {
    "name": "Новый Департамент",
    "type": "Департамент"
}

create_org_unit(create_group_data)
create_org_unit(create_organization_data)
create_org_unit(create_department_data)
