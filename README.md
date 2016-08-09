## What ##
Delete all the subscribers that are 90 days old (backing them up first)

## Installation ##

    sudo pip install -r requirements.txt
    cp settings.ini.dist settings.ini   
    
Config looks like this  Mailchimp username,  key, and pagination
    
    [MailChimp]
    username: jerome
    key: blablabal
    items_per_page: 100

Config of DB, please Create an instance of mysql on your machine
        
    [DB]
    username: root
    password: lol
    host: 127.0.0.1
    port: 3128
    dbname: datameeting


## Usage ##
fill the lists on a local db

    python go.py -a=get_lists
backup the emails     

    python go.py -a=backup
launch the deletion    

    python go.py -a=delete
