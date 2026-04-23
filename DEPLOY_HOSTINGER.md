# Deploy FastAPI na Hostinger VPS (Ubuntu) - Subpasta

Este guia mostra como fazer deploy do projeto FastAPI (Gunicorn/Uvicorn + Nginx) em uma VPS Ubuntu Hostinger, servindo em uma subpasta do domínio principal.

---

## 1. Pré-requisitos

- VPS Ubuntu 22.04 ou superior
- Acesso root/SSH
- Domínio configurado para a VPS

## 2. Passos automatizados

1. **Edite o script** `deploy_vps_hostinger.sh` e ajuste as variáveis:
   - `PROJ_DIR` (caminho do projeto)
   - `DOMAIN` (ex: hdevsolucoes.tech)
   - `SUBPATH` (ex: /gerador-ean-validos)

2. **Envie o projeto e o script para a VPS:**

   ```bash
   scp -r ./* usuario@ip-da-vps:/caminho/para/seu/projeto
   scp deploy_vps_hostinger.sh usuario@ip-da-vps:/caminho/para/seu/projeto
   ```

3. **Execute o script na VPS:**

   ```bash
   chmod +x deploy_vps_hostinger.sh
   sudo ./deploy_vps_hostinger.sh
   ```

4. **Acesse:**
   - `https://seu-dominio.com/gerador-ean-validos`

---

## 3. Estrutura do Nginx para subpasta

O Nginx está configurado para servir a aplicação e os arquivos estáticos na subpasta definida. Se mudar o nome da pasta, ajuste também no script e no arquivo de configuração do Nginx.

---

## 4. Logs e manutenção

- Para logs do serviço:
  ```bash
  sudo journalctl -u gerador-ean -f
  ```
- Para reiniciar o serviço:
  ```bash
  sudo systemctl restart gerador-ean
  ```

---

## 5. Segurança

- Recomenda-se usar HTTPS (Let's Encrypt) na VPS.
- Não esqueça de manter o sistema e dependências atualizados.

---

Dúvidas? Entre em contato: [LinkedIn](https://www.linkedin.com/in/harlem-afonso-claumann-silva-bb5160356/) | [Instagram](https://www.instagram.com/hdevsolucoes/) | [WhatsApp](https://wa.me/5511967745351)
