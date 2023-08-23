import requests
import OpenSSL.crypto as crypto

pfx_file = 'Realm-managerDemo.pfx'
pfx_password = 'dt%ga8`g&?MU53qW'

session = requests.Session()


def authenticate_with_pfx():
    try:
        pfx = crypto.load_pkcs12(open(pfx_file, 'rb').read(), pfx_password.encode())

        cert = crypto.dump_certificate(crypto.FILETYPE_PEM, pfx.get_certificate())
        key = crypto.dump_privatekey(crypto.FILETYPE_PEM, pfx.get_privatekey())

        auth_url = 'https://demo.u-system.tech/api/v1/auth'
        auth_response = session.post(auth_url, cert=(cert, key))

        assert auth_response.status_code == 200
        assert 'token' in auth_response.json()

        return auth_response.json()['token']

    except Exception as e:
        print(f"Authentication with Realm-managerDemo.pfx failed: {e}")
        return None


def create_org_unit(parent_id, name):
    try:
        create_url = 'https://demo.u-system.tech/api/v1/org-unit/create'

        data = {
            'parent_id': parent_id,
            'name': name
        }

        response = session.post(create_url, data=data, headers={'Authorization': f'Bearer {token}'})

        assert response.status_code == 201
        assert 'id' in response.json()

        return response.json()['id']

    except Exception as e:
        print(f"Failed to create org unit: {e}")
        return None


if __name__ == '__main__':
    token = authenticate_with_pfx()

    if token:
        group_company_id = create_org_unit(None, "Group Company")
        organization_id = create_org_unit(group_company_id, "Organization")
        department_id = create_org_unit(organization_id, "Department")

        print(f"Group Company ID: {group_company_id}")
        print(f"Organization ID: {organization_id}")
        print(f"Department ID: {department_id}")
