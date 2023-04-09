FROM php:7.0.9-apache

# Copy files for website
COPY src/public_html/index.php /var/www/html/
COPY src/public_html/flag.txt /
RUN chmod +r /flag.txt
# Expose port 80 (HTTP)
EXPOSE 80
