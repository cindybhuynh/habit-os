# Deployment Configuration

Config files live on AWS EC2 at:
- `/etc/systemd/system/habitos.service`
- `/etc/nginx/conf.d/habitos.conf`

These are versioned copies for reference.

## Common commands

Restart backend after code changes:
sudo systemctl restart habitos

View live backend logs:
sudo journalctl -u habitos -f

Nginx config test:
sudo nginx -t

Restart nginx:
sudo systemctl restart nginx