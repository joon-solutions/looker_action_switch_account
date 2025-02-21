#!/bin/bash
# Usage: bash deploy_one.sh

# set -a
# source .env
# set +a

# Set Environment Variables
ACTION_LABEL="Switch ONE or Customer View POC"
ACTION_NAME="switch-one-customer-poc-stg"
REGION="asia-southeast1"
PROJECT="joon-sandbox"
# todo: change this to the service account email
SERVICE_ACCOUNT_EMAIL=vertex-ai-cloud-function-demo@${PROJECT}.iam.gserviceaccount.com
# CLIENT_ID=${CLIENT_ID}
# CLIENT_SECRET=${CLIENT_SECRET}
# USERNAME=${USERNAME}
# PASSWORD=${PASSWORD}

# Create .env.yaml
printf "ACTION_LABEL: ${ACTION_LABEL}\nACTION_NAME: ${ACTION_NAME}\nREGION: ${REGION}\nPROJECT: ${PROJECT}" > .env.yaml

# deploy cloud functions
gcloud functions deploy ${ACTION_NAME}-list \
    --entry-point action_list \
    --env-vars-file .env.yaml \
    --trigger-http \
    --runtime=python311 \
    --allow-unauthenticated \
    --no-gen2 \
    --memory=1024MB \
    --timeout=540s \
    --region=${REGION} \
    --project=${PROJECT} \
    --service-account ${SERVICE_ACCOUNT_EMAIL} \
    --source=staging
gcloud functions deploy ${ACTION_NAME}-form \
    --entry-point action_form \
    --env-vars-file .env.yaml \
    --trigger-http \
    --runtime=python311 \
    --allow-unauthenticated \
    --no-gen2 \
    --memory=1024MB \
    --timeout=540s \
    --region=${REGION} \
    --project=${PROJECT} \
    --service-account ${SERVICE_ACCOUNT_EMAIL} \
    --source=staging
gcloud functions deploy ${ACTION_NAME}-execute \
    --entry-point action_execute \
    --env-vars-file .env.yaml \
    --trigger-http \
    --runtime=python311 \
    --allow-unauthenticated \
    --no-gen2 \
    --memory=8192MB \
    --timeout=540s \
    --region=${REGION} \
    --project=${PROJECT} \
    --service-account ${SERVICE_ACCOUNT_EMAIL} \
    --source=staging