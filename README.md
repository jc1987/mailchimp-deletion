
## Installation ##

    sudo pip install -r requirements.txt
    cp settings.ini.dist settings.ini   
    
FIll the settings 
Create an instance of mysql on your machine

## Usage ##
fill the lists on a local db
    python go.py -a=get_lists
backup the emails     
    python go.py -a=backup
launch the deletion    
    python go.py -a=delete
