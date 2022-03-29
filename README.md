# Web Scraper | Swoon 

This project is a general purpose web scraper, with a specialisation towards scraping from http://swooneditions.com/

> - Basic Functionality is inherited from the Scraper class 
> - The data storage is integrated with cloud services (S3, RDS)
> - The project contains the unittest class, which is used to inspect the resulting data after the code is run.

## Basic information

Collect the data from http://swooneditions.com/ for the set furniture category.    
> - Tabular Data (furniture): ID, name, type, description, category
> - Tabular Data (images): ID, Furniture ID (foreign key), url, link 
> - Image Data: jpeg images are stored in an S3 bucket 
> - This is then stored used cloud services to prevent scraping replication and promote scalability 

Also collects basic information and an associated image for each game.   
> - Tools used : Python, Selenium, SQL
> - Services used: AWS S3, RDS, EC2. Github, Dockerhub, Prometheus, Grafana   

## Installation

This is a docker containerised application, to use it simply run the following code in a terminal:

```bash
docker run --rm -it barnabymorgan/furniture_scraper:latest
```

## Usage

Before using, you will need the following details:

#S3 Bucket Details
> - bucket_name
> - access_key_id
> - secret_access_key
> - access_region

#Database Connection Details 
> - ENDPOINT = '' #AWS Endpoint
> - USER = ''
> - PASSWORD = ''
> - PORT= ''
> - DATABASE= ''

After running the docker run command above, the container will start and it will ask you to input all of the information above. 
After it has done that it will to scrape based on the furniture product provided. 

## License
[MIT](https://choosealicense.com/licenses/mit/)
