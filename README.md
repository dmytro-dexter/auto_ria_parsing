# Periodical parsing AutoRia
AutoRia is the most popular platform for selling used cars in Ukraine. This application helps to collect all the used cars data by web-scrapping, store it to the PostgreSQL and work with the data however you want.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for parsing data from auto.ria.ua

### Prerequisites

What things you need to install the software and how to install them

 - Python 3.12+
 - Docker
 - Docker Compose

### Installing

A step by step series of examples that tell you how to get a development env running

1. Clone the repository
    ```shell
    git clone https://github.com/dmytro-dexter/auto_ria_parsing.git
    ```
2. Build and up all services with Docker Compose
   ```shell
   docker-compose up -d --build --remove-orphans