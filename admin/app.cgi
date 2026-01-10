#!/usr/bin/perl

#--------------------------------------------------------------------
# Дополнительные модули
#--------------------------------------------------------------------

use CGI;
use DBI;

use strict;
use warnings;

#--------------------------------------------------------------------
# Объявление переменных
#--------------------------------------------------------------------

# База данных
my $mode  = "SQLite"; # режим работы
my $base  = "../dbase/base.db"; # файл базы

# Формат ссылки
my $lgth  = 6; # длина короткой ссылки
my @chars = (0..9); # ('A'..'Z', 'a'..'z', 0..9)

# Другие переменные
my $title = "Панель управления"; # заголов страницы
my $descs = "Простая ссылка для сайта"; # нет описания

# Статические файлы
my $css   = "../assets/css/style.min.css"; # файл стилей
my $js    = "../assets/js/script.min.js"; # файл скриптов

# Другие URL ссылки
my $fav   = "http://jodies.de/favicon.ico"; # файл иконки

#--------------------------------------------------------------------
# Подключение к базе данных
#--------------------------------------------------------------------

my $dsn = "DBI:$mode:dbname=$base";

my $dbh = DBI->connect($dsn, "", "", { RaiseError => 1, AutoCommit => 1 })
    or die $DBI::errstr;

#--------------------------------------------------------------------
# Объект CGI и URL страницы
#--------------------------------------------------------------------

my $q = CGI->new;
my $uri = $q->url;

#--------------------------------------------------------------------
# Получение даты и времени
#--------------------------------------------------------------------

my $date = get_date();

#--------------------------------------------------------------------
# Получение GET и POST запросов
#--------------------------------------------------------------------

my $action = $q->param('action') // "";
my $cmd = $q->param('cmd') // "";

#--------------------------------------------------------------------
# Получение стилей и скриптов
#--------------------------------------------------------------------

my $style = get_style();
my $script = get_script();

#--------------------------------------------------------------------
# Заголовок HTML страницы
#--------------------------------------------------------------------

print
    $q->header(
        -type => 'text/html',
        -charset => 'utf-8'
    );

print
    $q->start_html(
        -title => $title,
        -style => {-code => $style},
        -script => $script,
        -head => $q->Link({
                     -rel => 'icon',
                     -type => 'image/x-icon',
                     -href => $fav
                 })
    );

#--------------------------------------------------------------------
# Главное меню приложения
#--------------------------------------------------------------------

print
    $q->button(-name => 'button', -value => 'Главная', -class => 'button', -onClick => "redirect('$uri')"), " ",
    $q->button(-name => 'button', -value => 'Создать', -class => 'button', -onClick => "redirect('$uri?action=create')"), " ",
    $q->button(-name => 'button', -value => 'Поиск', -class => 'button', -onClick => "redirect('$uri?action=search')"), " ",
    $q->button(-name => 'button', -value => 'Список', -class => 'button', -onClick => "redirect('$uri?action=list')");

#--------------------------------------------------------------------
# Форма для создание ссылки
#--------------------------------------------------------------------

if ($action eq "create") {

    print
        $q->h1("Создать ссылку"),

        $q->start_form,

        $q->hidden(-name => 'action', -default => 'create'),
        $q->hidden(-name => 'cmd', -default => 'add'),

        "Название:", $q->br,
        $q->textfield(-name => 'text', -class => 'input', -id => 'text', -maxlength => 50), $q->br,

        "Адрес:", $q->br,
        $q->textfield(-name => 'url', -class => 'input'), $q->br,

        $q->div({-class => 'block', id => 'div'},
        "Ссылка:", $q->br,
        $q->textfield(-name => 'link', -class => 'input', -id => 'link')),

        "Описание:", $q->br,
        $q->textarea(-name => 'desc', -rows => 3, -cols => 30, -maxlength => 100), $q->p,

        $q->checkbox(-name => 'gen', -id => 'gen', -onClick => "checkbox('gen', 'div')", -label => 'Сгенерировать ссылку'), $q->p,

        $q->submit(-value => 'Создать', -class => 'button'), " ",

        $q->reset(-value => 'Очистить', -class => 'button'),

        $q->end_form, $q->p;

    # Добавление новой ссылки
    if ($cmd eq "add") {

        # Переменные undef присвоить ничего
        my $text = $q->param('text') // "";
        my $link = $q->param('link') // "";
        my $gen = $q->param('gen') // "";
        my $url = $q->param('url') // "";

        if ($text eq "") { # нет заголовка

            print $q->hr, $q->strong({-class => 'red'}, "Не введено название ссылки");

        } elsif ($url eq "") { # нет адреса

            print $q->hr, $q->strong({-class => 'red'}, "Не введен адрес ссылки");

        } elsif ($link eq "" && $gen ne "on") { # нет ссылки

            print $q->hr, $q->strong({-class => 'red'}, "Не введена короткая ссылка");

        # Введены все поля
        } else {

            # Получаем описание ссылки
            my $desc = $q->param('desc');

            # Добавляем описания если его нет
            if ($desc eq "") { $desc = $descs; }

            # Убираем слэш на конце адреса
            if (substr($url, -1) eq "/") { $url = substr($url, 0, -1); }

            # Добавляем протокол к ссылке
            if (substr($url, 0, 4) ne "http") { $url = "http://$url"; }

            # Генерация короткой ссылки
            if ($gen eq "on" || $link eq "") { $link = join("", @chars[map{rand @chars}(1..$lgth)]); }

            # Добавляем ссылку в базу
            $dbh->do("INSERT INTO base (url, link, text, desc) VALUES ('$url', '$link', '$text', '$desc')");

            # Ссылка для копирования
            $uri =~ s/admin\///g;
            $link = "$uri?r=$link";

            print
                $q->hr, $q->p, $q->strong({-class => 'green'}, "Новая ссылка добавлена"), $q->p;

            print
                $q->table(
                $q->Tr([
                    $q->th(['Название','Адрес','Ссылка','Описание']),
                    $q->td([$q->b($text), $q->a({-href => $url, -target => '_blank'}, $url), $q->a({-href => $link, -target => '_blank'}, $link), $desc])
                ])
            );
        }
    }
}

#--------------------------------------------------------------------
# Форма для поиска ссылки
#--------------------------------------------------------------------

if ($action eq "search") {

    print
        $q->h1("Поиск ссылки"),

        $q->start_form,

        $q->hidden(-name => 'action', -default => 'search'),
        $q->hidden(-name => 'cmd', -default => 'find'),

        "Ссылка:", $q->br,
        $q->textfield(-name => 'link', -class => 'input', -id => 'link'), $q->p,

        $q->submit(-value => 'Поиск', -class => 'button'), " ",

        $q->reset(-value => 'Очистить', -class => 'button'),

        $q->end_form, $q->p;

    # Поиск ссылки
    if ($cmd eq "find") {

        my $links = $q->param('link') // "";

        # Если ввели в поиск URL целиком
        if (length($links) > $lgth) {

            my ($tmp, $lnk) = split(/r=/, $links);

            $links = $lnk // "";
        }

        my $sth = $dbh->prepare("SELECT * FROM base WHERE link = '$links'");
           $sth->execute;

        # Если ссылка была найдена
        if (my ($id, $url, $link, $text, $desc, $date, $click) = $sth->fetchrow_array) {

            $uri =~ s/admin\///g;

            print
                $q->hr, $q->br,
                $q->table,
                $q->Tr([$q->th(['Название','Адреса','Статистика','Действие'])]);

            print
                $q->Tr(
                    $q->td($q->b($text), $q->br, $desc),
                    $q->td($q->a({-href => $url, -target => '_blank'}, $url), $q->br, $q->a({-href => "$uri?r=$link", -target => '_blank'}, "$uri?r=$link")),
                    $q->td($date, $q->br, "Количество кликов:", $q->b($click)),
                    $q->td($q->a({-href => "?action=list&cmd=del&id=$id", -onClick => "return confirm('Вы уверены, что хотите удалить ссылку?')"}, "Удалить"))
                );

            print $q->end_table;

        # Такой ссылке не существует
        } else {

            print $q->hr, $q->strong({-class => 'red'}, "Ссылка не найдена");
        }

        $sth->finish;
    }
}

#--------------------------------------------------------------------
# Вывести весь список ссылок
#--------------------------------------------------------------------

if ($action eq "list") {

    print
        $q->h1("Список ссылок");

    # Удаление ссылки
    if ($cmd eq "del") {

        my $id = $q->param('id');

        $dbh->do("DELETE FROM base WHERE id = '$id';");

        print
            $q->strong({-class => 'green'}, "Ссылка удалена"), $q->p;
    }

    # Сортировка по id
    my $sth = $dbh->prepare("SELECT * FROM base ORDER BY id ASC");
       $sth->execute;

    print
        $q->table,
        $q->Tr([$q->th(['Название','Адреса','Статистика','Действие'])]);

    while (my ($id, $url, $link, $text, $desc, $date, $click) = $sth->fetchrow_array) {

        $uri =~ s/admin\///g;

        print
            $q->Tr(
                $q->td($q->b($text), $q->br, $desc),
                $q->td($q->a({-href => $url, -target => '_blank'}, $url), $q->br, $q->a({-href => "$uri?r=$link", -target => '_blank'}, "$uri?r=$link")),
                $q->td($date, $q->br, "Количество кликов:", $q->b($click)),
                $q->td($q->a({-href => "?action=list&cmd=del&id=$id", -onClick => "return confirm('Вы уверены, что хотите удалить ссылку?')"}, "Удалить"))
            );
    }

    print $q->end_table;

    $sth->finish;
}

#--------------------------------------------------------------------
# Главная страница приложения
#--------------------------------------------------------------------

unless ($q->param('action')) {

    print
        $q->h1("Главная страница"),
        $q->p("Программа для подсчета количества кликов по ссылке."),
        $q->h2("О программе"),
        $q->p("Версия приложения: v1.10", $q->br, "Дата релиза: 10.01.2026 г."),
        $q->h2("Контакты"),
        $q->p("Почта:", $q->a({-href => "mailto:podedinov\@mail.ru"}, "podedinov\@mail.ru"));
}

#--------------------------------------------------------------------
# Конец HTML и отключение от базы
#--------------------------------------------------------------------

print $q->end_html;

$dbh->disconnect;

exit; # выход из приложения

#####################################################################
#                                                                   #
# Дополнительные функции приложения                                 #
#                                                                   #
#####################################################################

#--------------------------------------------------------------------
# Получение даты и времени
#--------------------------------------------------------------------

sub get_date {

    my ($day, $mday, $year, $hour, $min, $sec) = (localtime)[3,4,5,2,1,0];
    my $date = sprintf("%02d.%02d.%04d", $day, $mday + 1, $year + 1900);
    my $time = sprintf("%02d:%02d:%02d", $hour, $min, $sec);

    $date = sprintf("%s %s", $date, $time); # dd.mm.yyyy hh:mm:ss

    return $date;
}

#--------------------------------------------------------------------
# Получение стилей страницы
#--------------------------------------------------------------------

sub get_style {

    open(STYLE, $css) or die($!);
        local $/ = undef; # файл целиком
        my $style = <STYLE>;
    close(STYLE);

    return $style;
}

#--------------------------------------------------------------------
# Получение скриптов страницы
#--------------------------------------------------------------------

sub get_script {

    open(SCRIPT, $js) or die($!);
        local $/ = undef; # файл целиком
        my $script = <SCRIPT>;
    close(SCRIPT);

    return $script;
}
