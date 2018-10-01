# Backend

## Getting started

We are using Python 3, so make sure you have the correct version set as default. You will also need [pip](https://stackoverflow.com/questions/6587507/how-to-install-pip-with-python-3) package manager. If you care about avoiding dependency conflicts, look into [virtualenv](https://python-guide-cn.readthedocs.io/en/latest/dev/virtualenvs.html).

```
$ cd backend
$ virtualenv env    # optional, setup virtualenv
$ source env/bin/activate   # activate virtualenv
$ pip3 install -r requirements.txt
$ chmod +x run.sh   # make run.sh script executable
$ ./run.sh  # run Flask server
```
Once the server is running, visit [localhost:8080]().
