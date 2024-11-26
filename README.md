# Simple Microservice Example

A very simple microservice example with NodeJS, Python, Redis, and Mongo

## Dependencies

### API Gateway/FrontendApplication
* Node

### Data Backends
* MongoDB
* Redis

### QuoteService
* python3
* pip3
* flask
* pymongo
* redis

### Hosting
* NGINX


## Build the frontend

The application uses a frontend written with plain html with jQuery and to style with Bulma.

This is built with webpack. This default application is built assuming you are using the `localhost`.

To build this to fit your own **IP Address** please follow the steps before running the whole microservice.

- Install NodeJs on your system

- Go to *FrontendApplication* directory

- Run `npm install` or if you have yarn `yarn` to install packages

- Now you need to set the API Gateway for this frontend application. It can be any host you have.
    - Let's say you are hosting this application on `http://example.com` then your `API_GATEWAY` would be this one.
    - If you are hosting in some machine with IP `123.324.345.1` then your `API_GATEWAY` would be your IP.

- To pass this setting to webpack build you need to set an Environment Variable
    - Windows : `set API_GATEWAY=http://YOUR_HOST`
    - Linux/Max : `API_GATEWAY=http://YOUR_HOST`
    * Remember no / at the end of the URL to get your web app work
    * You will need to add a port if not using standard ports

- Now you can do `npm run build` or `yarn build`

- Check `dist/` folder for newly created index.html and the main.js


## Final Result
* check `http://YOUR_HOST:80` to see web app

![image](https://raw.githubusercontent.com/CSUChico-CSCI644/simple-microservice-example/main/working.png)
