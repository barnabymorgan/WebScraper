# Web Scraper | Swoon 

This project is a general purpose web scraper, with a specialisation towards scraping from http://swooneditions.com/

> - Basic Functionality is inherited from the Scraper class 
> - The data storage is integrated with cloud services (S3, RDS)
> - The project contains the unittest class, which is used to inspect the resulting data after the code is run.

## Basic information

Collect the statistics from http://swooneditions.com/ for the set furniture category.    
> - Data: Name, type, description, category, images

Also collects basic information and an associated image for each game.   
> - Tools used : Python, Selenium, SQL,   
> - Services used: AWS S3, RDS, EC2. Github, Dockerhub, Prometheus, Grafana   
