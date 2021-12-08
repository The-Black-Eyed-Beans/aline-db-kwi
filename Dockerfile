FROM mysql:latest

COPY aline-db-schema.sql /docker-entrypoint-initdb.d

ENV MYSQL_ROOT_PASSWORD=root
ENV MYSQL_DATABASE=alinedb
ENV MYSQL_USER=aline
ENV MYSQL_PASSWORD=Aline2022!