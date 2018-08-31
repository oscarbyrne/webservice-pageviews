# webservice-pageviews
Flask webservice for calculating statistics for webpage visits


## To use

```shell
$ export DATABASE_URI=sqlite:////tmp/test.db
$ pip install -r requirements.txt
$ flask db upgrade
$ flask add_visits_from_file data.csv
$ flask run
```

## To do

- implement `models.User.is_loyal`
- containerize / deploy
- improve documentation
