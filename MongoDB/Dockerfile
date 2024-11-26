#dockerfile for MONGO_DB

FROM mongo:latest

ENV MONGO_INITDB_ROOT_USERNAME=jayesh
ENV MONGO_INITDB_ROOT_PASSWORD=jayesh
ENV MONGO_INITDB_DATABASE=quote_db

COPY init-db.js /docker-entrypoint-initdb.d/init-db.js
