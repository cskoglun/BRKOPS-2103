# Way 1 - Automate monitoring

There are several methods for monitoring your network: you can manually log into your devices to check their operational state, use a GUI on the management controller that oversees your network, or opt to utilize your network's APIs to create a customized monitoring solution.

During this Cisco Live session, we explored two automation options for network monitoring. Firstly, we examined how to employ the programmatic interfaces of the IOS XE platform for streaming telemetry. Secondly, we looked at leveraging the REST APIs of the Catalyst Center and the Meraki Dashboard to gather necessary data and devise a tailored solution.

The choice of solution will depend on your skill set, interests, network requirements, and the devices you are using.

## Way1: Model Driven Telemetry

For documentation on how you can stream telemetry data with the help of the programmatic interfaces of the IOS XE platform by using the TIG Stack, we would like to point you to [Jeremy Cohoe's Github page](https://github.com/jeremycohoe/cisco-ios-xe-mdt)

## Way1: Consolidated data from Catalyst Center and the Meraki Dashboard

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

## Running the script

To run the script you need to make sure you are in the same folder in which you have your script and that you have your virtual environment activated. 
```bash
(venv) Way1 $
```
Run the python script
```bash
python way1.py
```
When you run your script the first time you will notice that a time series database  `poe_database_timeseries.csv` will be created in form of a csv file. This is where all your data will be stored over time

```csv
|-----------------|--------------------|--------------------|--------------------------------------|----------|--------------------------------------|--------------|-----------------|
| platform        | timestamp          | sw_name            | sw_identifier                        | powerinw | port                                 | ap_name      | ap_identifier   |
|-----------------|--------------------|--------------------|--------------------------------------|----------|--------------------------------------|--------------|-----------------|
| catalyst center |   1706646646.15081 | switch.ciscolab.dk | 6abaf622-b213-45a8-b732-ff1d8ed3e5f0 |       14 | f5301973-090d-452a-8e05-d9b7da46f63f | AP2          | AIR-AP4800-E-K9 |
|-----------------|--------------------|--------------------|--------------------------------------|----------|--------------------------------------|--------------|-----------------|
| catalyst center |   1706646646.15081 | switch.ciscolab.dk | 6abaf622-b213-45a8-b732-ff1d8ed3e5f0 |       13 | 2c7a368f-1006-41ba-b267-6b1323bb2cb9 | AP1          | AIR-AP4800-E-K9 |
|-----------------|--------------------|--------------------|--------------------------------------|----------|--------------------------------------|--------------|-----------------|
| meraki          |   1706646646.15081 | MS220-8P           | Q2HP-NJ5C-2DJA                       |      4.1 |                                    8 | MR33         | Q2PD-QJ4S-QUCC  |
|-----------------|--------------------|--------------------|--------------------------------------|----------|--------------------------------------|--------------|-----------------|
```


