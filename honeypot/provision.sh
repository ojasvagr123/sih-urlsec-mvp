#!/usr/bin/env bash
set -e
# Minimal provisioning for Debian/Ubuntu EC2
apt-get update
apt-get install -y ca-certificates curl gnupg lsb-release python3 python3-pip
curl -fsSL https://get.docker.com | sh
python3 -m pip install --upgrade pip
python3 -m pip install docker-compose || true
echo "Provisioning done."
