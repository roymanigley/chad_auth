# Chad Auth
> for the average OIDC enjoyer 😎

## Features

- Authorization Flow
- Client Credentials flow

### Compatible with `all-auth` using the OIDC provider

to use it with the auth flow you first need to create following data, this can be done using the API or the django shell 

1. create a `realm` → /api/docs
2. create one ore more `users` → /api/docs
3. create one ore more `clients` → /api/docs

```python
SOCIALACCOUNT_PROVIDERS = {
    "openid_connect": {
        "APPS": [
            {
                "provider_id": "openid_connect",
                "name": "openid_connect",
                "client_id": "<client_id>",
                "secret": "<client_secret>",
                "settings": {
                    "server_url": "http://localhost:8000/oidc/<realm>/.well-known/openid-configuration",
                },
            }
        ]
    }
}
```

for the rest follow this instructions [django_social_login_keycloak](https://github.com/roymanigley/django_social_login_keycloak), just skip the keycloak specific part

### Showcase

1. Presenting the Welcome Page
2. Presenting the management api (needed to manage the users, clients, roles and realms)
3. Presenting the OIDC endpoints
4. Showcasing the Auth Flow using an other django application with `all-auth`

![showcase](docs/images/show-case.gif)

## initial setup
### DEV
    ./scripts/build-dev.sh
### PROD
    ./scripts/build-prod.sh
### DOCKER
    ./scripts/build-docker.sh

## run the server
### DEV
    ./scripts/run-dev.sh
### PROD
    ./scripts/run-prod.sh
### DOCKER
    ./scripts/run-docker.sh
