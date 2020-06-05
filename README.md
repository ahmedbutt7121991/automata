# automata
This repository contains learning materials for automation project.
## How to run?
You need to run auto.py 4 times as follows:
```bash
python auto.py 9000 & #sqaure service
python auto.py 9001 & #double service
python auto.py 9002 & #fruit service
python auto.py 5001 & #handler
```
## How to check?
Open a new tab in your browser, and enter the following link:

`http://<IP_address_of_machine_running_the_handler>:5001/handler/<Any_number_from_0-9>`

e.g.

`http://192.168.10.125:5001/handler/5`

Result

```JSON
{"response2": "{\"double\": 10}\n", "response3": "{\"fruit\": \"watermelon\"}\n", "response1": "{\"square\": 25}\n"}
```
