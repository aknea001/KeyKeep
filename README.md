# KeyKeep
 A simple CLI password manager written entirely in python, db hosted locally with mysql
 Support for multiple users on same db
 Securely encrypted passwords so only the right user has access to their passwords

## Installing
 - Start by downloading mysql, I personally use a raspberry pi, but could very well download locally
    * [Downloading mysql on ubuntu based systems](https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-20-04)
    * [Setting up remote access to mysql sever **optional**](https://www.digitalocean.com/community/tutorials/how-to-allow-remote-access-to-mysql)
 - Create a designated database for keykeep
 - Use the mysql dump 'keykeep.sql' to recreate the tables
    ```
    mysql -u root -p **keykeep database** < keykeep.sql
    ```
  - Make a designated user (***optional***, but ***recommended***)
  - Grant appropriate privileges to the user (SELECT, INSERT, UPDATE, DELETE)
    ```
    mysql> GRANT SELECT, INSERT, UPDATE, DELETE ON **keykeep database name**.* TO "**mysql keykeep user**";
    ```

## Getting started
 - Download all requirements
    * Start by creating a virtual environment
      ```
      python -m venv .venv
      ```
    * Activate your venv
      ```
      source .venv/bin/activate
      ```
    * Download requirements
      ```
      pip install -r requirements.txt
      ```
  - OR ignore that shit and just install globally
    ```
    pip install -r requirements.txt
    ```
 - To connect to your mysql server you have to fill out the .env file
    * SQLHOST= **the ip to your mysql server (alternatively 'localhost' if hosted locally**)
    * SQLUSER= **the username of the mysql user you want to use**
    * SQLPASSWD= **the password used with the USER to access mysql**
    * SQLDATABASE= **the name of the database you want to use**
 - The sqldump comes with a root user by default (user: root, password: root)
 - Login with root and use 'adduser' command to create your users
 - 'restart' to logout, then login with your new user

 ## Commands
  - 'new': Creates a new password entry
  - 'get': Copies password entry to clipboard (optionally creates a file if in a headless environment)
    Options:
    * '-h': If in a headless environment, creates a file with the password instead of copying to clipboard
    * Can be used either as: 'get [**Optionally** options]' or 'get [**Optionally** options] [Entry ID]'
  - 'rm': To permenantly delete an entry (**This is permanent and no way of getting the entry back**)
    * Can be used either as: 'rm' or 'rm [Entry ID]'
  - 'update': To update the password of an entry (**This will permenantly remove the old password on this entry**)
    * Can be used either as: 'update' or 'update [Entry ID]'
  - 'adduser': To create a new user
  - 'clear': To clear the terminal
  - 'restart': Restarts the app (also works as a logout)
  - 'exit': Exits / quits the app