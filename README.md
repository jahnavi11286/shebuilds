
Azure demo link:https://examsin.azurewebsites.net/

Steps to run my application locally

step-1:-git clone https://github.com/jahnavi11286/microsoft-engage

step-2:-open this project in visual studio code

step-3:-pip install -r requirements.txt

step-4:-
      1)login to azure portal with your credentials
      
      2)create a postgres server with public access and allow azure services
      
      NOTE:enable Allow public access from any Azure service within Azure to this server
      
      3)Go to connection strings and copy the host name
     
      4)Now go to networking and create a new firewall rule with your public ip as start and  end ip addresses
      
      5)Download and install pg admin app
      
      6)go to connection and copy host name
      
      7)enter the hostname and credentials in pg admin app
      
      8)create a database of name mydb
      
      9)now add host name and password to databases in settings.py
      
      10)Type python manage.py makemigrations in terminal
      
      11)Type python manage.py migrate    
      
      12)Type python manage.py runserver
