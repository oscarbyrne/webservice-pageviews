# webservice-pageviews
Flask webservice for calculating statistics for webpage visits


## To use

```shell
$ sed -e "s/{{ DATABASE_URI }}/$DATABASE_URI/g" .env.template > .env
$ flask db upgrade
$ flask add_visits_from_file data.csv
$ docker build -t pageviews:latest .
$ docker run -p 5000:5000 --name pageviews --rm pageviews:latest
```
