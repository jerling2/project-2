# Project 2
Welcome to the README page of Project 2! This guide will walk you through the installation process and provide instructions for getting started.
## Installation
To set up the project, please follow these steps:

1. **Docker:** First, ensure that you have Docker installed on your system. You can download Docker from [here](https://www.docker.com/).
2. **Clone the Repository:** Clone this repository to your local machine.
3. **Navigate to the Project Directory:** Change your working directory to the location where you cloned the repository
4. **Build Docker Image:** Build the docker image by running this command:
```shell 
docker-compose build
```
5. **Run the Docker Container:** Run the Docker container and launch the application with the following command: 
``` shell
docker-compose up -d
```

6. **View Logs**: Follow the logs of the container by running this command:
``` shell
docker logs -f django_container
```

7. **Access the Application:** You can access the application by opening a web browser and navigating to http://127.0.0.1:8000.

8. **Program!** You can program on your local machine and see the server update in real time :)

**BUG:** the standard home page is not found. Fix this by removing the path('test/, foobar) in the project.urls.

*(Go to http://127.0.0.1:8000/test to see a proof-of-concept API's GET request)*

*ChatGPT co-authored this readme document.*

