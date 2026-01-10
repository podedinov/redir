# Необходимые программы для работы
apt install curl wget p7zip-full zip unzip

# Необходимые модули для Perl
apt install libcgi-pm-perl
apt install libdbi-perl
apt install libdbd-sqlite3-perl

# Рекомендуемые модули для Perl
apt install libfile-slurp-perl
apt install libjson-perl
apt install libwww-perl

# Доступ к cgi-bin для .htaccess
AllowOverride All

# Логин по умолчанию для .htpasswd
user: admin
passwd: xcLK34

# Права доступа к файлам для Apache2
chown -R www-data:www-data /var/www
chown -R www-data:www-data /usr/lib/cgi-bin

# Очистка логов ошибок для Apache2
bash -c 'echo > /var/log/apache2/error.log'

# Дополнительные утилиты для работы
backup.pl - бэкап всего приложения
dbase.pl - создание новой базы данных
minify.pl - уменьшение кода .css и .js
