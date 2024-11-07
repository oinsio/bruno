# Try Bruno to replace Postman

[Bruno overview documentation](https://docs.usebruno.com/introduction/what-is-bruno)

## Secret Management
[DotEnv File](https://docs.usebruno.com/secrets-management/dotenv-file)

# Local HTTP Server
Python local HTTP server can be used for tests.

```
cd ./Local\ HTTP\ server
python simple_http_server.py
```

# Bruno CLI
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