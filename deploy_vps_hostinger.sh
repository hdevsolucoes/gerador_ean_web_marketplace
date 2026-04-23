#!/bin/bash
# Script de deploy para VPS Ubuntu (Hostinger) - FastAPI + Gunicorn/Uvicorn + Nginx
# Subpasta: /gerador-ean-validos
# Autor: HDevSoluções

# Variáveis
PROJ_DIR="/caminho/para/seu/projeto"  # Altere para o caminho real
DOMAIN="hdevsolucoes.tech"
SUBPATH="/gerador-ean-validos"
USER="www-data"

# 1. Instalar dependências
sudo apt update && sudo apt install -y python3-venv python3-pip nginx
cd "$PROJ_DIR"
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
gpip install gunicorn uvicorn

# 2. Criar serviço systemd
SERVICE_FILE="/etc/systemd/system/gerador-ean.service"
sudo tee $SERVICE_FILE > /dev/null <<EOF
[Unit]
Description=Gerador EAN-13 FastAPI
After=network.target

[Service]
User=$USER
WorkingDirectory=$PROJ_DIR
ExecStart=$PROJ_DIR/.venv/bin/gunicorn main:app -k uvicorn.workers.UvicornWorker --bind 127.0.0.1:8001 --workers 2
Restart=always

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable gerador-ean
sudo systemctl restart gerador-ean

# 3. Configurar Nginx para subpasta
NGINX_FILE="/etc/nginx/sites-available/gerador-ean"
sudo tee $NGINX_FILE > /dev/null <<EOF
server {
    listen 80;
    server_name $DOMAIN;

    location $SUBPATH/ {
        proxy_pass http://127.0.0.1:8001/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        proxy_set_header SCRIPT_NAME $SUBPATH;
    }
    location $SUBPATH/static/ {
        alias $PROJ_DIR/static/;
    }
}
EOF

sudo ln -sf $NGINX_FILE /etc/nginx/sites-enabled/gerador-ean
sudo nginx -t && sudo systemctl reload nginx

echo "Deploy concluído! Acesse: https://$DOMAIN$SUBPATH"
