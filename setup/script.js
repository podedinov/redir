// Скрытый div-код для button
function openbox(box) {

  if(document.getElementById) {
    var openBox = document.getElementById(box);

    if(openBox.className == "none") {
        openBox.className = "block";
    } else {
        openBox.className = "none";
    }
  }
}

// Скрытый div-код для checkbox
function checkbox(check, box) {
    var checkBox = document.getElementById(check);
    var openBox = document.getElementById(box);

    if (checkBox.checked == true){
        openBox.className = "none";
    } else {
        openBox.className = "block";
    }
}

// Перенаправить на другой адрес
function redirect(url) {
    var ua = navigator.userAgent.toLowerCase();
    var isIE = ua.indexOf('msie') !== -1;
    var version = parseInt(ua.substr(4, 2), 10);

    // Internet Explorer 8 и ниже
    if (isIE && version < 9) {
        var link = document.createElement('a');
        link.href = url;
        document.body.appendChild(link);
        link.click();
    }

    // Все остальные браузеры
    else {
        window.location.href = url;
    }
}

// Вынужденное обновление страницы
function reboot() {
    window.location.reload();
}
