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

## How to run
- Clone the repository
- Get your authentication.json file following this [tutorial](https://docs.gspread.org/en/latest/oauth2.html#for-bots-using-service-account)
- Add the authentication.json to root directory of this folder
- Make a new spreadsheet called Scholar Stats
- Setup the "Scholars" worksheet by adding these columns on the first row:
  - Name 	(name of the scholar)
  - Split 	(0.6 if the scholar receives 60%)
  - Address 	(your Ronin address for that account)
  - See screenshots below for image
- Run `$ python src/main.py`
- See result

## Optional steps to combine this with our [Discord bot](https://github.com/StephanAkkerman/Axie_Manager_Bot)
- Add these columns to the "Scholars" worksheet: 
  - Discord ID	(Discord ID of the scholar in your server, find this by right-click 'copy id')
  - Info 	(Get this by typing !encrypt <your private key> after setting up the discord bot)

## Screenshots
This is how your "Scholars" worksheet should look like if you want the basic functioning:
![Basic functioning](https://github.com/StephanAkkerman/Scholar_Stats/blob/main/img/simple.png)
  
This is how your "Scholars" worksheet should look like if you want to use the Discord bot as well:
![Discord Bot inlcuded](https://github.com/StephanAkkerman/Scholar_Stats/blob/main/img/advanced.png)
  
After running this the code this is how your spreadsheet should look like:
![Result](https://github.com/StephanAkkerman/Scholar_Stats/blob/main/img/complete.png)
