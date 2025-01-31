# Try Bruno to replace Postman

## Table of Contents
- [Overview](#overview)
- [Setup Local Environment for Tests](#setup-local-environment-for-tests)
  - [Local HTTP Server](#local-http-server)
  - [Local Hashicorp Vault](#local-hashicorp-vault)
    - [Launch Vault in Docker](#launch-vault-in-docker)
    - [Init Vault](#init-vault)
    - [Unseal Vault](#unseal-vault)
    - [Login to Vault Web UI](#login-to-vault-web-ui)
    - [Write Secrets to Vault](#write-secrets-to-vault)
- [Bruno Secret Management](#bruno-secret-management)
- [Bruno CLI](#bruno-cli)

## Overview
This repository is an example of trying to use Bruno instead of a Postman or Insomnia free account.

You can find complete [Bruno documentation](https://docs.usebruno.com/introduction/what-is-bruno) here.

## Setup Local Environment for Tests

### Local HTTP Server
Python local HTTP server can be used for tests.
To start the server, run the following command:
```
cd ./Local\ HTTP\ server
python simple_http_server.py
```
The server will be started on port 3000.
It contains the following endpoints:
* GET `/api/v1/hello`
* POST `/api/v1/greet`
* POST `/api/v1/register`
* GET `/api/v1/profile/{userId}`

### Local Hashicorp Vault
#### Launch Vault in Docker
To start the local Hashicorp Vault, run the following command:
```
docker run --cap-add=IPC_LOCK -d --name=dev-vault -p 8200:8200 hashicorp/vault:latest
```

#### Init Vault
```
docker exec -it dev-vault vault operator init
```
You will get:
* Unseal Key
* Root Token

#### Unseal Vault
```
docker exec -it dev-vault vault operator unseal <unseal_key>
```
or
```
curl --request PUT \
  --url http://localhost:8200/v1/sys/unseal \
  --header 'content-type: application/json' \
  --data '{"key":"<unseal_key>"}'
```

#### Login to Vault Web UI
```
docker exec -it dev-vault vault ui
```
Open in web browser http://localhost:8200/ui

#### Write Secrets to Vault
You can write a secret to the Vault using the following command:
```
docker exec -it dev-vault vault kv put secret/bruno vault_password=<any value>
```
or using the Web UI.

### Bruno Secret Management
If you use `Open Source` or `Pro` [licence](https://www.usebruno.com/pricing), you won't be able to use Bruno's Integration with Secret Managers, as it is available only for `Ultimate` licence.

Anyway, you can get secrets from Secret Managers like Hashicorp Vault. To do that, you need to:
1. Create a `.env` as a copy of `.env.sample` file and fill it with your Vault tokens. You can find more information about [DotEnv File for Bruno here](https://docs.usebruno.com/secrets-management/dotenv-file).
2. Investigate files in `./Bruno First Steps/Vault example/` folder:
   1. `folder.bru` file and its `script:pre-request` section. It contains logic to import functions from `js` files.
   2. `js/hashicorp-vault-secrets.js` file. It contains functions to get secrets from Hashicorp Vault.
   3. `js/time-for-secret.js` file. It contains functions to reduce the number of Secret Manager calls.
3. Update above files according to your needs.

Another way to get secrets from Secret Managers is utilizing external libraries like [node-vault](https://www.npmjs.com/package/node-vault). Such an example you can find in `Bruno First Steps/Vault via node-vault example/Get Request with Vault Secret via node-vault` request. Check its `Pre Request` section. It is used to get `secret/data/bruno` secret and its value.

To make this example working do the follow:
1. Enable [Developer Mode](https://docs.usebruno.com/get-started/javascript-sandbox).
2. Set `true` value for `useNodeVault` environment variable.
3. Open `Tools` -> `Chrome Console` to check console output.

## Bruno CLI
You need to install the [Bruno CLI](https://docs.usebruno.com/bru-cli/overview):
```
npm install -g @usebruno/cli
```
After that, you will be able to run your collection in terminal using the following commands:
```
cd ./Bruno\ First\ Steps/
bru run --env Local --reporter-html results.html
```
