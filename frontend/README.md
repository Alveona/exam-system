## Инструкции по редактированию и запуску фронтенда

### Запуск локально

    npm install
    npm run dev
    
Открыть localhost:3000
    
### Подготовка к деплою

    npm run build
    
На выходе получается папка dist  

Необходимо настроить Nginx/Apache для раздачи фронтенде  
Пример:

    server {
            server_name example.com; # ваш домен

            location / {
                    root /www/exam-system/frontend/dist;
                    index index.html index.htm;
                    try_files $uri $uri/ /index.html;
                    proxy_set_header  Host              $http_host;
                    proxy_set_header  X-Forwarded-For   $proxy_add_x_forwarded_for;
            }
          listen 80;

    }
