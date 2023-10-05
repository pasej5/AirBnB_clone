#!/bin/bash
# Bash script to set up web servers for web_static deployment

# Install Nginx if it's not already installed
if ! dpkg -l | grep -q nginx; then
    sudo apt-get -y update
    sudo apt-get -y install nginx
fi

# Create necessary directories if they don't exist
web_static="/data/web_static"
web_static_test="$web_static/releases/test"

sudo mkdir -p $web_static_test
sudo mkdir -p $web_static/shared

# Create a fake HTML file for testing
echo "This is a test." | sudo tee "$web_static_test/index.html"

# Create a symbolic link, deleting it first if it already exists
if [ -L "$web_static/current" ]; then
    sudo rm -f "$web_static/current"
fi

sudo ln -sf "$web_static_test" "$web_static/current"

# Give ownership of /data/ to the ubuntu user and group recursively
sudo chown -R ubuntu:ubuntu $web_static

# Update Nginx configuration
nginx_config="/etc/nginx/sites-available/default"

# Replace the default Nginx configuration with a custom configuration
cat <<EOF | sudo tee $nginx_config
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    server_name _;

    location /hbnb_static/ {
        alias $web_static/current/;
        index index.html;
    }

    location / {
        try_files $uri $uri/ =404;
    }
}
EOF

# Restart Nginx to apply the new configuration
sudo service nginx restart

echo "Web server setup complete."
