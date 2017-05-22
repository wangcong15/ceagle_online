# Ceagle Online 部署
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

### mysql 密码设置为forever
* sudo apt-get install mysql-server
* sudo apt-get install mysql-client
* sudo apt-get install libmysqlclient-dev
* sudo apt-get install python-mysqldb

### clang llvm
* sudo apt install llvm
* sudo update-alternatives --install /usr/bin/clang clang /usr/bin/clang-3.5 100
* sudo update-alternatives --install /usr/bin/opt opt /usr/bin/opt-3.5 100
* sudo update-alternatives --install /usr/bin/llvm-dis llvm-dis /usr/bin/llvm-dis-3.5 100

### the project:需要输入gitlab的账号密码
* git clone http://sts.thss.tsinghua.edu.cn:5080/beagle-team/sv-online.git

* cd sv-online/
* sudo pip install pycparser
* python manage.py migrate

### run the server
* uwsgi --http :9794 --chdir ~/Desktop/sv-online --wsgi-file SV_Online_Python/wsgi.py --processes 1 --static-map /static=SV_Online_Python/static

