ServerlessSampler
=======

# Requirements

- [AWS CLI](https://aws.amazon.com/cli/)
- [Docker for Mac](https://www.docker.com/docker-mac)

## Development

- [pyenv](https://github.com/pyenv/pyenv)
- [localstack](https://github.com/localstack/localstack)

# Architecture
![architecture](https://github.com/kongmingstrap/ServerlessSampler/blob/master/architecture.png "architecture")

# Setting

## 1. Python

### shell

```shell
$ pyenv local 3.6
$ python -m venv .venv3
$ source .venv3/bin/activate
$ pip install pipenv
$ pipenv install
```

### fish shell

```shell
$ pyenv local 3.6
$ python -m venv .venv3
$ source .venv3/bin/activate.fish
$ pip install pipenv
$ pipenv install
```

## 2. Start localstack

```shell
$ make localstack-up
```

## 3. Stop localstack

```shell
$ make localstack-stop
```

# Code style check

```shell
$ make lint
```

# Unit test

```shell
$ make unit-test
```

# Deploy

## 1. Configure AWS credentials

- `~/.aws/credentials`

```bash
[sampler-development]
aws_access_key_id = <your_aws_access_key_id>
aws_secret_access_key = <your_aws_secret_access_key>
```

- `~/.aws/config`

```bash
[profile sampler-development]
region = ap-northeast-1
output = json
```

## 2. Deploy

```shell
$ make deploy
```
