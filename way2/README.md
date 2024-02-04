# Way 2 - Let's get ready to save some power!
This section is aimed for those who would like to try to automate the way you shut down access ports on switches through the Cisco Catalyst Center APIs and the Meraki Dashboard.

## Setup
1. Complete the `pip install -r requirements.txt` at the root of this repository
2. create a file `env` from the `env.template`
    ```bash
    cp env.template env
    ```
3. Fill in your preferred data to the `env`. If you are just planning to run certain tests, only those details need to be included

    ```
    MERAKI_API_KEY=<meraki key> # Your Meraki API key

    CC_USERNAME=<username> # Your Catalyst Center username
    CC_PASSWORD=<password> # Your Catalyst Center password
    CC_URL=<url> # your Catalyst Center URL
    ```

    For example (this is dummy data to give an example of the syntax):

    ```
    MERAKI_API_KEY=lhkdLHIFGIWAY872937173TGHJS

    CC_USERNAME=admin
    CC_PASSWORD=my_secure_password
    CC_URL=catcenter.ciscolab.dk
    ```
4. Add information about your Meraki Organization and your Meraki network to the `way2.py` file.
```python
ORG = "ORG-NAME" #Input your organization name
NETWORKS = ["NETWORK-1", "NETWORK-2"] # Names of your network
```

## Get started with the code
In the repository you will find two python scrips
- `database.py`
- `powersave.py`

`powersave.py` uses script `database.py` in order to make all API calls and data mapping that is required in order to create an csv database. It also uses `database.py` in order to make the API calls to turn down and turn on access ports that APs are connected to. 
 
```bash
(venv) $ python powersave.py
```

To run the script, you run the following command (make sure you are in the correct directory):
```bash
(venv) $ python powersave.py
```

When you run the script, you should be greetet with the following message: 

```bash
* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
*                                                                               *
*                          Welcome to the power saver script!                   *
*                                                                               *
* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
```
You will then be presented with input options, you will either be able to: 
* Create a new database
* Shut down the access points
* Turn the access points up again

Here is an example of how it can look like: 
```bash
* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
*                                                                               *
*                          Welcome to the power saver script!                   *
*                                                                               *
* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

Do you want to shut down the access points and save some watts (y/n)[n]?:y

...double checking: You REALLY want to shut down the access points?(y/n)[n]y

Your action "shut APs down" is being pushed to Cisco Catalyst Center and the Meraki Dashboard 

Port GigabitEthernet1/0/23 with id 43f9297c-9de3-4527-b513-2beecc6432ef is updated to DOWN
Port GigabitEthernet1/0/23 with id e500025a-f9bc-45db-a527-de3eca59be1d is updated to DOWN
Port 1 with id 1 has changed status to True on MS device
```

Now your task is to take this code, and start adapting it so it better fits ***your use cases***.

## Authors & Maintainers
People responsible for the creation and maintenance of this project:
* Christina Skoglund cskoglun@cisco.com
* Juulia Santala jusantal@cisco.com

## License
This project is licensed to you under the terms of the [Cisco Sample Code License](LICENSE).