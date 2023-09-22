# Non-pharmacological recommendation system using Large Language Models

This repo contains the code necessary to run the backend application for generating nonpharmacological recommendations to users ! It includes all our externally-facing APIs, and most of the services and storage models those APIs interact with.

In summary, you will do the following

- [Install the dependencies](#prerequisites) (python, docker, etc).

- [Choose and configure an IDE](#ide-setup) (we recommend either Pycharm or VScode).

- [Setting up chroma database using docker](#database-setup)

- [Spin-up your local dependencies for testing](#testing)

- [Deployment guidelines](#deployment).

## Setup

### Prerequisites

* Amazon AWS Account to connect to the S3 Bucket
* Install local dependencies in the requirements.in file. Core dependencies are:
  * [langchain](https://www.langchain.com/)  
  * [chromadb](https://www.trychroma.com/)  
  * [openai](https://openai.com/)  
  * [fastapi](https://fastapi.tiangolo.com/tutorial/)  
  * [uvicorn](https://www.uvicorn.org/)  
  * [unstructured[local-inference]]
  * [tiktoken]
  * [pyaml-env](https://pypi.org/project/pyaml-env/)   
* [homebrew](https://brew.sh/) A package manager that makes it easy to install stuff; use it if you do not care for installing each thing individually/mucking about with package dependencies; if you are not on Mac OS: Ubuntu - use apt-get instead. Windows - not sure.
* [Docker](https://www.docker.com/products/docker-desktop)
* [Python](https://www.python.org/). Make sure to download the right version for your CPU architecture. For M1 CPU Macbooks use 
  **arm**64. For Intel, use **amd**64.
* [git](https://git-scm.com/downloads)
* [Kubectl](https://kubernetes.io/)


## IDE setup

### Setup your preferred IDE either pycharm or VSCode  
  
* the configuration folder contains the application properties and the prompt template
* the dto folder contains the data transfer object classes
* the service folder contains classes that handle the business logic of the application
* the main class serves as the entry point for the application
* the Dockerfile contains step-by-step instructions on how to create a Docker image from the application

## Chroma Database setup

Most likely you'll need to setup chroma locally on docker.

Read [this doc](https://docs.trychroma.com/usage-guide#running-chroma-in-clientserver-mode) for some tips and guidelines around using ChromaDB.


### Running tests

Run the application from the main file

## Deployment

Deployments are managed through [Docker](https://www.docker.com/products/docker-desktop), and [Kubectl](https://kubernetes.io/). Kubernetes is hosted on [AWS](https://aws.amazon.com/), alternatively, you can use any cloud provider of your choice

## API and Component Documentation
### 1.  The */chat* endpoint 

* POST http://127.0.0.1:8000/chat

### Specification

| Field | Description | Required | Example | Datatype |
| ----- | ----------- | -------- | ------- | -------  |
| message | represents user's question | true | what is osteoporosis | string |

### Request Example

{
    "message": "define osteoporosis in one sentence"
}

### Response Example

{
    "message": "Osteoporosis is a disease that causes low bone mass and deterioration in the microarchitecture."
}

### 2.  The */chat/data/reload* endpoint 

* PUT http://127.0.0.1:8000/chat/data/reload

### Specification

This endpoint handles refreshing and reloading the entire collection of doucments. It doesnt receive contain a request body and returns a 201.
In the background it spins up an asynchronous thread to execute the task

### Response Example

201

### 2.  The */chat/data/insert* endpoint 

* POST http://127.0.0.1:8000/chat/data/insert

### Specification

| Field    | Description                                                  | Required | Example | Datatype |
|----------|--------------------------------------------------------------| -------- | ----- | -------  |
| fileName | represents the name of the file to be saved in the vector DB | true | pdf/2015_HealthyNutritionHealthyBones_ThematicReport_English.pdf | string |

### Request Example

{
    "fileName": "pdf/2015_HealthyNutritionHealthyBones_ThematicReport_English.pdf"
}
