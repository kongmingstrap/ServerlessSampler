#!/usr/bin/env bash

set -xeuo pipefail

image_name="sampler-cfn"

docker image build --tag "$image_name" .
