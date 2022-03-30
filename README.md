# Notification service

This project is API for sending notifications via http.

The project was created as a test task.


## How this is working?

API allows you to create a list of customers and messaging them by time.
Celery task every minute checks time interval and status of sending then make sending at next format -

```sh
{
 'id': send.id,
 'phone': customer.phone_number,
 'text': send.message_text
}
```

The API can also provide statistics on created mailing lists and sent messages and detailed information about these messages.


## How to use this project?

Clone down project.

```sh
$ git clone https://github.com/evgdgl/web-api.git
$ cd web-api
```

In the .env.dev file, change the required values. Specify your tokens and external API, database and superuser settings.

Spin up the containers:

```sh
$ docker-compose up -d --build
```
After running the project, go to http://localhost:8000/admin and login to the admin page using the username and password from the .env.dev file. Now you can manage accounts and create tokens for them.

## Integration with the service

An authorization token is used to make requests to the API. Information about all API methods is contained in the OpenAPI specification of service http://localhost:8000/docs/.
