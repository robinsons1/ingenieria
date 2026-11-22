# Ingeniería & Automatización by Ingversia (`ingenieria.ingversia.com`)

Sitio web estático de alto rendimiento (**HTML5 + CSS3 + JavaScript vanilla**) para la división **Ingeniería & Automatización** del ecosistema **Ingversia**, preparado para despliegue en el servidor principal (`i5` — `100.92.40.116:8087`) y alta disponibilidad *warm-standby* en el nodo de contingencia (`Pentium` — `100.117.199.22`).

---

## 1. Estructura del Proyecto

```text
~/ingenieria-server/
├── docker-compose.yml          # Contenedor nginx:alpine en 100.92.40.116:8087:80
├── nginx.conf                  # Rutas limpias, Gzip, caché y headers de seguridad
├── ingenieria_og.py            # Generador Python/Pillow de OG (1200x630) e iconos
├── README.md                   # Esta guía de despliegue y contingencia
└── html/
    ├── index.html              # Portada (/)
    ├── 404.html                # Error 404 personalizado
    ├── robots.txt
    ├── sitemap.xml
    ├── llms.txt
    ├── llms-full.txt
    ├── assets/
    │   ├── ingenieria_logo.svg
    │   ├── ingenieria_simbolo.svg
    │   ├── ingversia_simbolo.svg
    │   ├── favicon.svg
    │   ├── favicon-48.png
    │   ├── apple-touch-icon.png
    │   └── og-banner.jpg
    ├── css/
    │   ├── styles.css
    │   └── legal.css
    ├── js/
    │   └── main.js
    ├── redes-mikrotik/index.html
    ├── electronica-pcb/index.html
    ├── automatizacion-plc/index.html
    ├── manuales/index.html
    ├── privacidad/index.html
    └── terminos/index.html
```

---

## 2. Vista Previa Local y Regeneración de Assets

```bash
# Vista previa local en http://127.0.0.1:8087
python -m http.server 8087 -d html

# Regenerar banner Open Graph (1200x630) e iconos PNG (requiere Pillow)
python ingenieria_og.py
```

---

## 3. Despliegue en Servidor Principal (`i5` — `100.92.40.116`)

### 3.1 Clonar o subir a `~/ingenieria-server/` y levantar Docker
```bash
cd ~/ingenieria-server
docker compose up -d

# Verificar salud local vía Tailscale
curl -I http://100.92.40.116:8087/
curl -I http://100.92.40.116:8087/redes-mikrotik/
```

### 3.2 Permisos ACL para micro-pull y backups (`backup_pull`)
Al ser un sitio estático dentro de `/home/robinson/ingenieria-server/html/`, entra automáticamente en el `rsync` nocturno de `backup_diario.sh` hacia el disco Toshiba. Aplica una sola vez los permisos ACL de lectura para que el Pentium pueda extraerlo sin errores `rsync code 23`:

```bash
sudo setfacl -R -m u:backup_pull:rX /home/robinson/ingenieria-server/html
sudo setfacl -R -d -m u:backup_pull:rX /home/robinson/ingenieria-server/html
sudo setfacl -m u:backup_pull:rX /home/robinson/ingenieria-server
```

---

## 4. Integración Warm-Standby en Nodo de Contingencia (`Pentium` — `100.117.199.22`)

### 4.1 Agregar bloque `# 6` en `/home/robinsonbackup/scripts/sync_live_frontends.sh`
Añadir al script de micro-pull cada 15 minutos (antes del `chmod -R 755 "$DEST_BASE"` final):

```bash
# 6. Ingeniería & Automatización
rsync -avz --delete -e "ssh -i $SSH_KEY -o ConnectTimeout=5" \
    "$SSH_USER@$I5_IP:/home/robinson/ingenieria-server/html/" \
    "$DEST_BASE/ingenieria/" >> "$LOG" 2>&1
```

Ejecutar manualmente una primera vez y verificar que existan los archivos:
```bash
/home/robinsonbackup/scripts/sync_live_frontends.sh
ls -la /home/robinsonbackup/live_standby/ingenieria/
```

### 4.2 Agregar `ingenieria_standby` en `~/ivia-contingencia/docker-compose.yml`
Copiar también `nginx.conf` hacia `~/ivia-contingencia/nginx-conf/ingenieria.conf` y añadir el servicio ligero (`~5 MB` RAM) conectado a `red_contingencia`:

```yaml
  ingenieria_standby:
    image: nginx:alpine
    container_name: ingenieria_standby
    restart: unless-stopped
    ports:
      - "8087:80"
    volumes:
      - /home/robinsonbackup/live_standby/ingenieria:/usr/share/nginx/html:ro
      - /home/robinsonbackup/ivia-contingencia/nginx-conf/ingenieria.conf:/etc/nginx/conf.d/default.conf:ro
    networks:
      - red_contingencia
```

Recrear el stack de contingencia:
```bash
cd ~/ivia-contingencia && sudo docker compose up -d
```

---

## 5. Enrutamiento Simétrico: Cloudflare Tunnel + Nginx Proxy Manager

### 5.1 Cloudflare Zero Trust (`servidor-bogota`)
Agregar Public Hostname compartido por ambos nodos (para conmutación transparente con `failover-watch.sh`):
- **Hostname:** `ingenieria.ingversia.com`
- **Service:** `http://localhost:80`

### 5.2 Nginx Proxy Manager — `i5` (`http://100.92.40.116:8181`)
- **Domain Names:** `ingenieria.ingversia.com`
- **Scheme / Forward Hostname / Port:** `http` · `100.92.40.116` · `8087`
- **Block Common Exploits:** Activo
- **Custom Nginx Configuration:** Dejar **vacío**.

### 5.3 Nginx Proxy Manager — `Pentium` (`http://100.117.199.22:8282`)
- **Domain Names:** `ingenieria.ingversia.com`
- **Scheme / Forward Hostname / Port:** `http` · `ingenieria_standby` · `80`
- **Block Common Exploits:** Activo
- **Custom Nginx Configuration:** Dejar **vacío** (para no invalidar el `proxy_pass`).

---

## 6. Monitoreo y Tablero Interno
1. **Uptime Kuma (`100.92.40.116:3001` y `100.117.199.22:3001`):** agregar monitor HTTP(S) para `https://ingenieria.ingversia.com/` y check local `http://100.92.40.116:8087/`.
2. **Homepage (`100.92.40.116:3000`):** añadir acceso directo a `https://ingenieria.ingversia.com`.

---

## 7. Checklist de Fase 3: Conectar con `ingversia.com` (Cuando el subdominio esté en vivo)
Una vez validado `https://ingenieria.ingversia.com` en producción:
1. Actualizar la **tarjeta #3 (Ingeniería & Automatización)** en `ingversia-landing-main/html/index.html` y su footer/selector para apuntar a `https://ingenieria.ingversia.com` (manteniendo mención explícita a `https://nexus.ingversia.com` como entorno demo en vivo).
2. Actualizar `ingversia-landing-main/html/llms.txt`, `llms-full.txt`, `ingversia_og.py` y enlazar `https://ingenieria.ingversia.com/privacidad/` dentro de `ingversia.com/privacidad.html`.
