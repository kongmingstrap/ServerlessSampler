sampler-cfn
=======

# requirements

- [AWS CLI](https://aws.amazon.com/cli/)
- [Docker for Mac](https://www.docker.com/docker-mac)
- [yarn](https://yarnpkg.com)

# Setting
```bash
$ yarn install 
```

# Deploy

## 1. configure AWS credentials

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

## 2. Docker image build

```bash
$ ./build.sh
```

## 3. Deploy

```bash
$ ./run.sh -t <template.yml>
```
