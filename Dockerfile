# Base Image
FROM php:fpm-bullseye

# Add Composer
RUN php -r "copy('https://getcomposer.org/installer', 'composer-setup.php');" && php composer-setup.php --install-dir=/usr/local/bin --filename=composer && php -r "unlink('composer-setup.php');"

# Update Composer
RUN composer self-update

# Install PHP Extension
RUN docker-php-ext-install pdo_mysql

# Set Working Directory
WORKDIR /var/www/html

# Expose Port 9000 and Start php-fpm server
EXPOSE 9000