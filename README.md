# Financier
### Engineering Bachelor Thesis - Application that helps with making long-term financial decisions

## Running Procedure
Switch docker into service
```bash
sudo systemctl enable docker
```
Run MongoDB:
```bash
docker run -d \
	--name financier-mongo \
	--env-file ./enviromental.txt \
	mongo:5.0.22
```
Run GetRates:
```bash
docker build -t get-rates ./get-rates-app/
docker run -d --rm 				\
	--name financier-get-rates 	\
	--env-file ./enviromental.txt \
	--env-file ./get-rates-app/enviromental.txt \
	get-rates
```
Run LoanProphet:
```bash
docker build -t loan-prophet ./approve-model/
docker run -d --rm \
	-v /PRODUCTION/Financier/app/package/:/model/package \
	loan-prophet
```
Run FinancierAPI:
```bash
docker build -t financier-api ./app
docker run -d \
	-p 80:8080 \
	--env-file ./enviromental.txt \
	--name financier-api_container \
	financier-api
```

## Useful snippets:
Login to MongoDB:
```bash
mongosh --username <username> --password <password>
```