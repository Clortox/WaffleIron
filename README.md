Syllabi Generator (Waffle Iron)
===============================


Running
-------

To run the application, be sure you have pip installed. Afterward, execute the
following command:

```
./run.sh
```

To view the application, visit [localhost:5000](http://127.0.0.1:5000). The
application will update as you update files locally

Run in docker
-------------

To run the application in docker, run the following commands:

```
docker build --tag waffleiron .
docker-compose up
```

The script `./run-docker.sh` will execute the two above commands. If the
application throws errors regarding access to mongodb, check the service is
running. Refer to the section below on mongodb

Running Mongodb
---------------

Mongodb can be run locally or via docker. Mongo is automatically started when
using the `./run-docker.sh` command.

Structure
---------

Strcutred as an MVC paradigm. Followed
[this](https://devstudioonline.com/article/create-python-flask-app-in-mvc-format)
example project.

