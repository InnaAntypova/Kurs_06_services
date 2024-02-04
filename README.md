<H1> Курсовой проект по работе с DJANGO</H1>

<H3>Cервис по управлению рассылками.</H3>


Необходимо в корне проекта создать файл **.env** и внести в него свои данные для переменных по образцу из **.env.sample**.

Для заполнения раздела Блог тестовой информацией необходимо выполнить команду 
<br>**python manage.py loaddatautf8 data_blog.json** 

Для создания автоматически групп Модератора рассылок и Менеджера контента для Блога с необходимыми правами 
необходимо выполнить команду <br>**python manage.py moderate**

Superuser можно создать используя команду <br>**python manage.py createsuperuser**

Для запуска планировщика рассылок необходимо выполнить команду <br>**python manage.py runapscheduler**

<br></br>
<H3>!!!Примечание!!!</H3>
Необходимо в настройках вашего почтового провайдера создать т.н. App Password и ввести его в поле EMAIL_HOST_PASSWORD,
это сделано в целях безопасности.
<br>Как это сделать для: </br> 
<a name="links">[Mail.ru](https://help.mail.ru/mail/security/protection/external)<h2></h2></a>
<a name="links">[Gmail](https://www.lifewire.com/get-a-password-to-access-gmail-by-pop-imap-2-1171882)<h2></h2></a>
<a name="links">[Yandex](https://yandex.ru/support/id/authorization/app-passwords.html)<h2></h2></a>

