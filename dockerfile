# Use an official PostgreSQL image as the base image
FROM postgres:latest

# Set environment variables for database connection
ENV POSTGRES_USER root
ENV POSTGRES_PASSWORD 1234
ENV POSTGRES_DB kindle_reviews

# Copy the SQL files into the Docker container
COPY ./schema.sql /docker-entrypoint-initdb.d/
COPY ./populate.sql /docker-entrypoint-initdb.d/

# Expose PostgreSQL port (default is 5432)
EXPOSE 5432