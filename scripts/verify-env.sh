#!/usr/bin/env bash
set -e

required_vars=(
  APP_BASE_URL
  SUPABASE_URL
  SUPABASE_KEY
  SMTP_HOST
  SMTP_PORT
  SMTP_USER
  SMTP_PASSWORD
)

for var in "${required_vars[@]}"; do
  if [ -z "${!var}" ]; then
    echo "Missing required env var: $var"
    exit 1
  fi
done

echo "Environment variables OK"
