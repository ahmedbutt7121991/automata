# automata
This repository contains learning materials for automation project. (python version 2.7)
A basic flask app that takes `key` (number from 1-9) from user and returns `square` and `double`. The values are fetched from a database.

## Requirements

- MySQL

- For python requirements please see `requirements.txt`.Run following for updating the packages
  
  ```python
  python -m pip install requirements.txt
  ```
  
## How to run?

- update `IP` and `Port` in `config.ini` file

- Make sure the credentials are set for MySQL in `config.ini` file. `db_dump.sql` contains the dump of required database. update as follows:

```bash
mysql db_name < backup-file.sql
```

- You need to run auto.py times as follows:

```bash
python auto.py square & #For square Service
python auto.py double & #For Double Service
```

## How to check?
Open a new tab in your browser, and enter the following link:

`http://<IP_address_of_machine_running_the_handler>:<Port>/`

e.g.

`http://192.168.10.125:5001/`

You should see the following page

![](https://i.imgur.com/2QAriNo.png)

Enter a number from 1-9 and click the button

![](https://i.imgur.com/eci2jTZ.png)

## Change background color

On your linux machine use the following command to set a `environment variable` with color value

```shell
export PG_COLOR=lightblue
```

if the environment variable is not set, the background color of the page defaults to `black`

![](https://i.imgur.com/dyD5ANX.png)



