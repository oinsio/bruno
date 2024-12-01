# Try Bruno to replace Postman

[Bruno overview documentation](https://docs.usebruno.com/introduction/what-is-bruno)

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
* GET /api/v1/hello
* POST /api/v1/greet
* POST /api/v1/register
* GET /api/v1/profile/{userId}

### Local Hashicorp Vault
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

#### Write Secret to Vault
You can write a secret to the Vault using the following command:
```
docker exec -it dev-vault vault kv put secret/bruno vault_password=<any value>
```
or using the Web UI.

## Bruno Secret Management
[DotEnv File](https://docs.usebruno.com/secrets-management/dotenv-file)

## Bruno CLI
You need to install the Bruno CLI:
```
npm install -g @usebruno/cli
```
After that, you will be able to run your collection:
```
cd ./Bruno\ First\ Steps/
bru run --env Local --reporter-html results.html
```
Detailed information can be found [here](https://docs.usebruno.com/bru-cli/overview).