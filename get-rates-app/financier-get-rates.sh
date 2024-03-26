#!/bin/bash
docker run -d --rm --name financier-get-rates --env-file /PRODUCTION/Financier/enviromental.txt --env-file /PRODUCTION/Financier/get-rates-app/enviromental.txt get-rates
