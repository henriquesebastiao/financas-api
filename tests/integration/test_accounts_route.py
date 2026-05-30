
from fastapi import status


async def test_route_create_account(client):
    response = await client.post(
        '/accounts',
        json={
            'name': 'Nubank',
            'balance': 100.00,
        },
    )

    json = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert json['deleted'] is False
    assert json['balance'] == '100.00'


async def test_route_create_account_without_balance(client):
    response = await client.post(
        '/accounts',
        json={
            'name': 'MP',
        },
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()['balance'] == '0.00'


async def test_route_create_account_without_name(client):
    response = await client.post(
        '/accounts',
        json={
            'balance': 100.00,
        },
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


async def test_route_create_account_already_exists(client):
    await client.post(
        '/accounts',
        json={
            'name': 'Nubank',
            'balance': 100.00,
        },
    )

    response = await client.post(
        '/accounts',
        json={
            'name': 'Nubank',
            'balance': 200.00,
        },
    )

    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json()['detail'] == 'Account already exists'


async def test_route_update_account_name(client, account):
    response = await client.patch(
        f'/accounts/{account.id}',
        json={
            'name': 'Sicredi',
        },
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()['name'] == 'Sicredi'
    assert response.json()['balance'] == '150.00'


async def test_route_update_account_balance(client, account):
    response = await client.patch(
        f'/accounts/{account.id}',
        json={
            'balance': '200.00',
        },
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()['name'] == account.name
    assert response.json()['balance'] == '200.00'


async def test_route_update_account_does_not_exist(client):
    response = await client.patch(
        '/accounts/10',
        json={
            'name': 'Conta Inexistente',
        },
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['detail'] == 'Account does not exist'


async def test_route_update_account_already_exists(client, account):
    await client.post(
        '/accounts',
        json={
            'name': 'Nubank',
            'balance': 100.00,
        },
    )

    response = await client.patch(
        f'/accounts/{account.id}',
        json={
            'name': 'Nubank',
        },
    )

    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json()['detail'] == 'Account already exists'
