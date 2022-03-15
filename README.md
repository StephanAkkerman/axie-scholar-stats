# Scholar Stats
This is a simple python script for saving the historical data of your scholars. 

## Features
Overview of:
- Daily SLP
- Daily $
- Daily Average SLP 
- Total SLP
- Total $	
- Manager Share SLP
- Manager Share $
- Scholar Share SLP	
- Scholar Share $	
- SLP Price
- Daily overview of SLP on scholars accounts
- Specific overview of every scholar
For more see the screenshots below.

## Dependencies
The required packages to run this code can be found in the `requirements.txt` file. To run this file, execute the following code block:
```
$ pip install -r requirements.txt 
```
Alternatively, you can install the required packages manually like this:
```
$ pip install <package>
```

## Setup
Start by cloning the repository. 

Next, get your authentication.json file, by following the steps below carefully. Or follow the instructions from this (starts from 1:58) [video](https://youtu.be/6zeDGeGGHx4?t=118)

If you prefer written instructions follow the instructions below:
- Enable API access for the new project [instructions](https://docs.gspread.org/en/latest/oauth2.html#enable-api-access-for-a-project).
- Creating the `authentication.json file` [instructions](https://docs.gspread.org/en/latest/oauth2.html#for-bots-using-service-account).

After follow the instructions above, last things you need to do is this:
- Save your `authentication.json` file in the same folder as you saved the files for this script.
- Open `authentication.json` and copy the email behind `"client_email":`
![auth](https://github.com/StephanAkkerman/Axie_Manager_Bot/blob/main/img/authentication.png)
- Open Google Drive and go to the folder that you want the bot to make the spreadsheets in, right click on that folder and press share
![drive1](https://github.com/StephanAkkerman/Axie_Manager_Bot/blob/main/img/drive.png)
- Share the folder with the client email out of `authentication.json`
![drive2](https://github.com/StephanAkkerman/Axie_Manager_Bot/blob/main/img/drive2.png)

Then after that is done, go to the folder where this repository is stored and execute the following code block:
```
python src/setup.py
```

This will setup the Spreadsheet and worksheet for you in Google Drive. After doing that you will need to fill in the information of your scholars. If you are not sure what you should fill in here, check the [examples](#examples) below.

If you filled out the information you are done and at last you need to execute this code:
```
python src/main.py
```

## Note
The same method as described here is also used for setting up our [Discord bot](https://github.com/StephanAkkerman/Axie_Manager_Bot). So if you would like to have a Discord bot to manage your scholars, be sure to check out that repository.

## Examples
This is how your "Scholars" worksheet should look like if you want the basic functioning:
![Basic functioning](https://github.com/StephanAkkerman/Scholar_Stats/blob/main/img/simple.png)
    
After running this the code this is how your spreadsheet should look like:
![Result](https://github.com/StephanAkkerman/Scholar_Stats/blob/main/img/complete.png)
