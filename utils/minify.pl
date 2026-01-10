#!/usr/bin/perl

#--------------------------------------------------------------------
# Дополнительные модули
#--------------------------------------------------------------------

use strict;
use warnings;

#--------------------------------------------------------------------
# Объявление переменных
#--------------------------------------------------------------------

my $css     = "../setup/style.css";
my $js      = "../setup/script.js";

my $css_min = "../assets/css/style.min.css";
my $js_min  = "../assets/js/script.min.js";

#--------------------------------------------------------------------
# Обработка Curl запросов
#--------------------------------------------------------------------

print "Продолжить выполнение программы? (y/n): ";

chomp(my $run = <STDIN>); # удалить конец строки
$run = "\L$run"; # нижний регистр

if (($run eq "y") || ($run eq "yes")) {

    my $get_css = "curl -X POST -s --data-urlencode input\@$css https://www.toptal.com/developers/cssminifier/api/raw > $css_min";
    my $get_js = "curl -X POST -s --data-urlencode input\@$js https://www.toptal.com/developers/javascript-minifier/api/raw > $js_min";

    system($get_css); # создаем style.min.css
    system($get_js); # создаем script.min.js

    print "Файлы:\n\x1b[32m$css_min\n$js_min\x1b[0m\nуспешно созданы.\n";

} else {

    print "Процесс был прерван пользователем.\n";
}

exit; # выход из приложения
