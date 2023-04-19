# Hello, this is our application: Health Hero
- Health Hero is meant to assist Doctors, Patients, and Pharmacists navigate the technologically complex world.
- It is meant to be an easy to use application that offers users a wide variety of funtionality.
- The framework of the project is based of of 3 blueprint, and each blueprint contains GET, DELETE, POST, and PUT queries to make our relational model come to life.

Video-Demo: https://drive.google.com/file/d/1Twp5fW9dio3H_LKwHMMhnccWRQeu1NDT/view?usp=sharing

# MySQL + Flask Boilerplate Project

This repo contains a boilerplate setup for spinning up 3 Docker containers: 
1. A MySQL 8 container for obvious reasons
1. A Python Flask container to implement a REST API
1. A Local AppSmith Server

## How to setup and start the containers
**Important** - you need Docker Desktop installed

1. Clone this repository.  
1. Create a file named `db_root_password.txt` in the `secrets/` folder and put inside of it the root password for MySQL. 
1. Create a file named `db_password.txt` in the `secrets/` folder and put inside of it the password you want to use for the a non-root user named webapp. 
1. In a terminal or command prompt, navigate to the folder with the `docker-compose.yml` file.  
1. Build the images with `docker compose build`
1. Start the containers with `docker compose up`.  To run in detached mode, run `docker compose up -d`. 
