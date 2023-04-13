FROM nginx:stable-alpine
COPY ./nginx/default.conf /etc/nginx
COPY ./nginx/default.conf /etc/nginx/conf.d


EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]