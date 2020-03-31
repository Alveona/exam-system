## Инструкция по запуску серверной части
---------

0. Установить docker и docker-compose

Инструкция по установке docker-ce для Linux-based систем  

      https://docs.docker.com/install/linux/docker-ce/ubuntu/
Инструкция по установке docker-compose  

      https://docs.docker.com/compose/install/

1. Развернуть MySQL базу данных, убедиться, что она доступна с внешних IP адресов

2. Создать файл exam-system/backend/exam-backend/connection.py по шаблону connection.py.template  
Файл содержит данные подключения к базе данных и криптографический ключ для авторизации

3. Настроить внешний веб-сервер Apache или Nginx  
Пример настройки конфигурации Nginx:  

        server {
                server_name api.example.com; # ваш домен

                location /static-files/ {
                    autoindex on;
                    alias /www/exam-system/backend/exam_backend/static/;

                }

                location /media/ {
                        alias /www/exam-system/backend/exam_backend/static/media/;
                }

                location / {
                    proxy_pass                          http://localhost:8000/api/;
                    proxy_set_header  Host              $http_host;   
                    proxy_set_header  X-Forwarded-For   $proxy_add_x_forwarded_for;
                }

                location /token-auth/ {
                    proxy_pass http://localhost:8000;

                }


            listen 80;
          }
          
  
4. В папке exam-system/backend запустить

        docker-compose build --no-cache
        docker-compose up -d

API будет доступен по вашему домену
