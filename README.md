# Ceagle Online Deployment
### django
* sudo apt-get install python-pip
* sudo apt-get install python-virtualenv
* mkdir ~/django
* cd ~/django
* virtualenv venv
* source venv/bin/activate
* sudo pip install django==1.9.2

### uwsgi
* sudo pip install uwsgi -I --no-cache-dir

### nginx
* cd ~
* wget http://nginx.org/download/nginx-1.9.9.tar.gz
* tar xf nginx-1.9.9.tar.gz
* cd nginx-1.9.9
* sudo apt-get install libpcre3 libpcre3-dev
* sudo apt-get install zlib1g-dev
* ./configure --prefix=/usr/local/nginx
* sudo make
* sudo make install
* sudo /usr/local/nginx/sbin/nginx -c /usr/local/nginx/conf/nginx.conf

### git
* cd ~/Desktop
* sudo apt-get install git

### mysql set the password as: forever
* sudo apt-get install mysql-server
* sudo apt-get install mysql-client
* sudo apt-get install libmysqlclient-dev
* sudo apt-get install python-mysqldb

### clang llvm
* sudo apt install llvm
* sudo apt-get install clang-3.5
* sudo update-alternatives --install /usr/bin/clang clang /usr/bin/clang-3.5 100
* sudo update-alternatives --install /usr/bin/opt opt /usr/bin/opt-3.5 100
* sudo update-alternatives --install /usr/bin/llvm-dis llvm-dis /usr/bin/llvm-dis-3.5 100

### the project: input the username and password of gitlab
* git clone https://github.com/wangcong15/ceagle_online.git

* cd ceagle_online/
* sudo pip install pycparser
* sudo pip install django==1.8
* python manage.py makemigrations
* python manage.py migrate
* sudo pip install django==1.9.2

### run the server
* uwsgi -i uwsgi.ini

