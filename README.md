# Financier
## 🇬🇧 Engineering Bachelor Thesis - Web application that helps with making long-term financial decisions
## 🇵🇱 Temat Pracy Inżynierskiej - Aplikacja webowa wspierająca podejmowanie długoterminowych dezycji finansowych

The following application was created as a result of a Bachelor Thesis project, focusing on developing a web application that aids users in making long-term financial decisions. The project, titled "Financier," aims to provide valuable insights and tools to support financial planning and management.  
___
The application was finally graded as 6, which is the highest grade possible in Polish Universities that require high average grades and max score from Thesis.
___
# ======== Deployment process ========
Enable Docker
```bash
sudo systemctl enable docker
```
Run MongoDB:
```bash
docker run -d \
	--name financier-mongo \
	--env-file ./enviromental.txt \
	-v mongodbdata:/data/db \
	mongo:7.0.6
```
Run GetRates:
```bash
docker build -t get-rates ./get-rates-app/
docker run -d --rm \
	--name financier-get-rates \
	--env-file ./enviromental.txt \
	--env-file ./get-rates-app/enviromental.txt \
	get-rates
```
Run GetInflation:
```bash
docker build -t get-inflation . # run inside script folder
docker run -d --rm \
	--name financier-get-inflation \
	--env-file ./enviromental.txt \
	get-inflation
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
___
## Useful snippets:
Login to MongoDB:
```bash
mongosh --username <username> --password <password>
```

#### Importat details:
Created volume to make data persistant inside MongoDB:
```bash
docker volume create mongodbdata
```
Added `financier-get-rates.sh` to /etc/cron.daily/

___  
Used icons:
<a href="https://www.flaticon.com/" title="currency icons">Icons created by Freepik - Flaticon</a>  
Inflation data:
<a href="https://en.wikipedia.org/wiki/ISO_4217">Wikipedia data</a>