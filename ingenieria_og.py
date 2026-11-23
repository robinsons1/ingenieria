"""Generador de Open Graph (1200x630) e iconos raster para Ingeniería & Automatización by Ingversia."""

import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont

SCALE = 2
FINAL_W, FINAL_H = 1200, 630
W, H = FINAL_W * SCALE, FINAL_H * SCALE


def s(val):
    return int(round(val * SCALE))


def load_font(candidates, size):
    font_dirs = [
        "C:/Windows/Fonts",
        "/usr/share/fonts/truetype/dejavu",
        "/usr/share/fonts/truetype/liberation",
        "/usr/share/fonts/TTF",
        "/System/Library/Fonts",
    ]
    for name in candidates:
        try:
            return ImageFont.truetype(name, s(size))
        except Exception:
            pass
        for d in font_dirs:
            path = os.path.join(d, name)
            if os.path.exists(path):
                try:
                    return ImageFont.truetype(path, s(size))
                except Exception:
                    pass
    return ImageFont.load_default()


font_badge = load_font(["segoeuib.ttf", "arialbd.ttf", "DejaVuSans-Bold.ttf"], 11)
font_title = load_font(["segoeuib.ttf", "arialbd.ttf", "DejaVuSans-Bold.ttf"], 48)
font_sp_title = load_font(["segoeuib.ttf", "arialbd.ttf", "DejaVuSans-Bold.ttf"], 37)
font_endorse = load_font(["segoeuib.ttf", "arialbd.ttf", "DejaVuSans-Bold.ttf"], 22)
font_sub = load_font(["segoeui.ttf", "arial.ttf", "DejaVuSans.ttf"], 18)
font_card_t = load_font(["segoeuib.ttf", "arialbd.ttf", "DejaVuSans-Bold.ttf"], 18)
font_card_k = load_font(["consolab.ttf", "consola.ttf", "DejaVuSansMono-Bold.ttf"], 11)
font_card_d = load_font(["segoeui.ttf", "arial.ttf", "DejaVuSans.ttf"], 13)
font_mono = load_font(["consolab.ttf", "consola.ttf", "DejaVuSansMono-Bold.ttf"], 12)
font_footer = load_font(["segoeuib.ttf", "arialbd.ttf", "DejaVuSans-Bold.ttf"], 16)
font_footer_s = load_font(["segoeui.ttf", "arial.ttf", "DejaVuSans.ttf"], 15)


def draw_ingenieria_logo(draw_ctx, x, y, size):
    """Dibuja el símbolo oficial de Ingeniería (3 módulos claros + 1 módulo cian #06b6d4)."""
    draw_ctx.rounded_rectangle(
        (x, y, x + size, y + size),
        radius=int(size * 0.21),
        fill="#0b1324",
        outline="#1e3354",
        width=s(2),
    )
    pad = int(size * 0.15)
    inner = size - 2 * pad
    gap = max(s(4), int(size * 0.06))
    sq = (inner - gap) // 2
    r_piece = int(size * 0.07)

    ix, iy = x + pad, y + pad
    draw_ctx.rounded_rectangle((ix, iy, ix + sq, iy + sq), radius=r_piece, fill="#f8fafc")
    draw_ctx.rounded_rectangle((ix + sq + gap, iy, ix + 2 * sq + gap, iy + sq), radius=r_piece, fill="#f8fafc")
    draw_ctx.rounded_rectangle((ix, iy + sq + gap, ix + sq, iy + 2 * sq + gap), radius=r_piece, fill="#f8fafc")
    draw_ctx.rounded_rectangle(
        (ix + sq + gap, iy + sq + gap, ix + 2 * sq + gap, iy + 2 * sq + gap),
        radius=r_piece,
        fill="#06b6d4",
    )


def draw_favicon_symbol(size_2x):
    """Dibuja icono cuadrado oficial de Ingeniería (3 módulos blancos + 1 cian técnico)."""
    icon = Image.new("RGB", (size_2x, size_2x), "#0b1324")
    idraw = ImageDraw.Draw(icon)

    pad = int(size_2x * 0.15)
    inner = size_2x - 2 * pad
    gap = int(size_2x * 0.065)
    sq = (inner - gap) // 2
    r_piece = int(size_2x * 0.08)

    idraw.rounded_rectangle((pad, pad, pad + sq, pad + sq), radius=r_piece, fill="#f8fafc")
    idraw.rounded_rectangle((pad + sq + gap, pad, pad + 2 * sq + gap, pad + sq), radius=r_piece, fill="#f8fafc")
    idraw.rounded_rectangle((pad, pad + sq + gap, pad + sq, pad + 2 * sq + gap), radius=r_piece, fill="#f8fafc")
    idraw.rounded_rectangle(
        (pad + sq + gap, pad + sq + gap, pad + 2 * sq + gap, pad + 2 * sq + gap),
        radius=r_piece,
        fill="#06b6d4",
    )
    return icon


def wrap_text(draw_ctx, text, font, max_w):
    words = text.split(" ")
    lines = []
    current = ""
    for word in words:
        test = (current + " " + word).strip()
        bbox = draw_ctx.textbbox((0, 0), test, font=font)
        if (bbox[2] - bbox[0]) <= max_w:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def _create_og_canvas(badge_text, primary_glow=(8, 125, 165), badge_accent="#22d3ee", badge_border="#0e7490", badge_fill="#071e26"):
    """Crea el lienzo base 2x con resplandores, grilla sutil y encabezado institucional."""
    base = Image.new("RGB", (W, H), "#05080f")
    glow_layer = Image.new("RGB", (W, H), (0, 0, 0))
    gd = ImageDraw.Draw(glow_layer)

    gd.ellipse((s(-160), s(-180), s(560), s(440)), fill=primary_glow)
    gd.ellipse((s(420), s(210), s(880), s(580)), fill=(22, 65, 130))
    gd.ellipse((s(820), s(260), s(1360), s(740)), fill=(12, 74, 110))

    glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(radius=s(130)))
    img = Image.blend(base, glow_layer, 0.5)
    draw = ImageDraw.Draw(img)

    for x in range(s(36), W, s(36)):
        for y in range(s(36), H, s(36)):
            r_dot = s(1)
            draw.ellipse((x - r_dot, y - r_dot, x + r_dot, y + r_dot), fill="#132036")

    margin_x = s(64)
    badge_x, badge_y = margin_x, s(46)
    tb = draw.textbbox((0, 0), badge_text, font=font_badge)
    badge_w = (tb[2] - tb[0]) + s(50)
    badge_h = s(34)
    draw.rounded_rectangle(
        (badge_x, badge_y, badge_x + badge_w, badge_y + badge_h),
        radius=s(17),
        fill=badge_fill,
        outline=badge_border,
        width=s(1.5),
    )
    dot_x, dot_y = badge_x + s(18), badge_y + badge_h // 2
    draw.ellipse((dot_x - s(5), dot_y - s(5), dot_x + s(5), dot_y + s(5)), fill=badge_border)
    draw.ellipse((dot_x - s(3.5), dot_y - s(3.5), dot_x + s(3.5), dot_y + s(3.5)), fill=badge_accent)
    draw.text(
        (badge_x + s(32), badge_y + badge_h // 2),
        badge_text,
        font=font_badge,
        fill="#f1f5f9",
        anchor="lm",
    )

    loc_txt = "BOGOTÁ D.C. · COLOMBIA"
    loc_w, loc_h = s(222), s(34)
    loc_x = W - margin_x - loc_w
    draw.rounded_rectangle(
        (loc_x, badge_y, loc_x + loc_w, badge_y + loc_h),
        radius=s(17),
        fill="#0b111e",
        outline="#1e293b",
        width=s(1.2),
    )
    draw.text((loc_x + loc_w // 2, badge_y + loc_h // 2), loc_txt, font=font_badge, fill="#94a3b8", anchor="mm")
    return img, draw, margin_x


def _draw_og_footer(draw, margin_x):
    """Dibuja pie de marca uniforme y borde de tarjeta."""
    footer_y = H - s(42)
    url_txt = "ingenieria.ingversia.com"
    draw.text((margin_x, footer_y), url_txt, font=font_footer, fill="#f8fafc", anchor="lm")
    ub = draw.textbbox((0, 0), url_txt, font=font_footer)
    uw = ub[2] - ub[0]
    draw.text(
        (margin_x + uw + s(14), footer_y),
        "—  División Ingeniería & Automatización",
        font=font_footer_s,
        fill="#64748b",
        anchor="lm",
    )
    draw.text(
        (W - margin_x, footer_y),
        "Pruebas Reales en Operación · Ecosistema Ingversia",
        font=font_mono,
        fill="#22d3ee",
        anchor="rm",
    )
    draw.rectangle((s(1), s(1), W - s(2), H - s(2)), outline="#17233b", width=s(2))


def generate_og_banner():
    img, draw, margin_x = _create_og_canvas("INGENIERÍA APLICADA · OPERACIÓN REAL")

    logo_y = s(104)
    logo_size = s(86)
    draw_ingenieria_logo(draw, margin_x, logo_y, logo_size)

    title_x = margin_x + logo_size + s(24)
    draw.text((title_x, logo_y - s(2)), "Ingeniería & Automatización", font=font_title, fill="#f8fafc")
    draw.text((title_x, logo_y + s(58)), "by Ingversia", font=font_endorse, fill="#f5821f")

    draw.text(
        (margin_x, s(216)),
        "Redes MikroTik Dual-WAN  ·  Electrónica & PCB  ·  Automatización PLC & NEXUS  ·  Manuales Técnicos",
        font=font_sub,
        fill="#bae6fd",
    )

    div_y = s(262)
    draw.rectangle((margin_x, div_y, W - margin_x, div_y + s(1.5)), fill="#1a263e")
    draw.rectangle((margin_x, div_y, margin_x + s(210), div_y + s(2)), fill="#06b6d4")

    cards = [
        {
            "kicker": "01 · REDES & MIKROTIK",
            "title": "Failover & VPN",
            "desc": "Dual-WAN recursivo real, WireGuard, Tailscale y servidores locales.",
            "tag": "Prueba real",
            "accent": "#22d3ee",
            "bg": "#081421",
            "border": "#155e75",
        },
        {
            "kicker": "02 · HARDWARE & EMBEDDED",
            "title": "Electrónica & PCB",
            "desc": "Diseño PCB 1-2 capas, microcontroladores, armado THT y carcasas 3D.",
            "tag": "Gerbers + THT",
            "accent": "#fbbf24",
            "bg": "#15120a",
            "border": "#78350f",
        },
        {
            "kicker": "03 · CONTROL & DATOS",
            "title": "PLCs & Telemetría",
            "desc": "Tableros, Modbus/4-20 mA, alertas y demo viva NEXUS.",
            "tag": "Demo NEXUS",
            "accent": "#38bdf8",
            "bg": "#0a1222",
            "border": "#1e3a8a",
        },
        {
            "kicker": "04 · DOCUMENTACIÓN",
            "title": "Manuales Técnicos",
            "desc": "Levantamiento de circuitos, planos limpios y guías de falla.",
            "tag": "PDF A4 + planos",
            "accent": "#34d399",
            "bg": "#071813",
            "border": "#065f46",
        },
    ]

    card_y = s(292)
    card_h = s(248)
    card_gap = s(18)
    total_w = W - 2 * margin_x
    card_w = (total_w - 3 * card_gap) // 4

    for i, c in enumerate(cards):
        cx = margin_x + i * (card_w + card_gap)
        draw.rounded_rectangle(
            (cx, card_y, cx + card_w, card_y + card_h),
            radius=s(18),
            fill=c["bg"],
            outline=c["border"],
            width=s(1.5),
        )
        draw.rounded_rectangle(
            (cx + s(20), card_y, cx + s(95), card_y + s(3.5)),
            radius=s(1.5),
            fill=c["accent"],
        )

        draw.text((cx + s(20), card_y + s(26)), c["kicker"], font=font_card_k, fill=c["accent"])
        draw.text((cx + s(20), card_y + s(54)), c["title"], font=font_card_t, fill="#f8fafc")

        lines = wrap_text(draw, c["desc"], font_card_d, card_w - s(40))
        for li, line in enumerate(lines[:4]):
            draw.text((cx + s(20), card_y + s(96) + li * s(22)), line, font=font_card_d, fill="#94a3b8")

        route_y = card_y + card_h - s(32)
        draw.line((cx + s(20), route_y - s(10), cx + card_w - s(20), route_y - s(10)), fill="#1b263b", width=s(1))
        draw.text((cx + s(20), route_y), c["tag"], font=font_mono, fill=c["accent"])
        draw.text((cx + card_w - s(32), route_y - s(2)), "→", font=font_card_d, fill=c["accent"])

    _draw_og_footer(draw, margin_x)

    final_img = img.resize((FINAL_W, FINAL_H), Image.Resampling.LANCZOS)
    assets_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "html", "assets")
    os.makedirs(assets_dir, exist_ok=True)
    out_path = os.path.join(assets_dir, "og-banner.jpg")
    final_img.save(out_path, "JPEG", quality=95, optimize=True, subsampling=0)
    print(f"OK — OG Banner generado en {out_path} ({FINAL_W}x{FINAL_H})")


def generate_specialty_og_banners():
    """Genera banners Open Graph 1200x630 dedicados por especialidad."""
    assets_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "html", "assets")
    os.makedirs(assets_dir, exist_ok=True)

    specs = [
        {
            "filename": "og-mikrotik.jpg",
            "badge": "REDES MIKROTIK · ALTA DISPONIBILIDAD",
            "title": "Redes MikroTik & Failover Dual-WAN Real",
            "subtitle": "Conmutación automática probada en vivo, VPN segura y servidores locales.",
            "glow": (8, 125, 165),
            "accent": "#22d3ee",
            "card_bg": "#081421",
            "border": "#155e75",
            "badge_fill": "#071e26",
            "pillars": [
                ("01 · FAILOVER REAL", "Failover Recursivo Real", "Rutas recursivas externas con prueba física y transición limpia para POS y VPN."),
                ("02 · CONECTIVIDAD", "VPN WireGuard / Tailscale", "Túneles cifrados entre sedes y teletrabajo sin exponer puertos WAN críticos."),
                ("03 · CONTINUIDAD", "Servidores + Backups 3-2-1", "Nodos Debian/Docker, bloqueo DNS Pi-hole, copias externas y respaldo .rsc."),
            ],
        },
        {
            "filename": "og-pcb.jpg",
            "badge": "ELECTRÓNICA · HARDWARE Y EMBEDDED",
            "title": "Diseño de PCBs 1–2 Capas & Armado THT",
            "subtitle": "Del esquemático a tarjetas ordenadas listas para fabricar y gabinete 3D.",
            "glow": (140, 82, 12),
            "accent": "#fbbf24",
            "card_bg": "#15120a",
            "border": "#78350f",
            "badge_fill": "#1f1608",
            "pillars": [
                ("01 · DISEÑO PCB", "Esquemático, Gerbers y BOM", "Layout 1–2 capas con verificación ERC/DRC, protecciones y archivos listos."),
                ("02 · FIRMWARE", "ESP32, Sensores y Firmware", "Adquisición estable, comunicación RS-485/I2C y recuperación automática."),
                ("03 · ENSAMBLE Y 3D", "Banco THT + BerdeX 3D", "Soldadura pasante THT, pruebas eléctricas y carcasas riel DIN 4 colores."),
            ],
        },
        {
            "filename": "og-plc.jpg",
            "badge": "CONTROL INDUSTRIAL · TELEMETRÍA",
            "title": "Automatización Industrial, PLCs & Telemetría",
            "subtitle": "Tableros de control, instrumentación industrial y datos locales sin licencias cerradas.",
            "glow": (22, 85, 155),
            "accent": "#38bdf8",
            "card_bg": "#0a1222",
            "border": "#1e3a8a",
            "badge_fill": "#09172a",
            "pillars": [
                ("01 · TABLEROS", "PLCs y Tableros de Control", "Lógica secuencial, variadores VFD, protecciones y pruebas reales de marcha."),
                ("02 · CAMPO", "Modbus RTU/TCP · 4–20 mA", "Lectura de transmisores industriales, redes RS-485 y señales analógicas."),
                ("03 · DEMO NEXUS", "Edge Local-First · Demo NEXUS", "Históricos locales, alertas bidireccionales Telegram y reportes PDF A4."),
            ],
        },
        {
            "filename": "og-manuales.jpg",
            "badge": "DOCUMENTACIÓN · INGENIERÍA INVERSA",
            "title": "Manuales Técnicos & Levantamiento de Circuitos",
            "subtitle": "Elimina la dependencia operativa con diagramas claros y guías paso a paso.",
            "glow": (8, 118, 84),
            "accent": "#34d399",
            "card_bg": "#071813",
            "border": "#065f46",
            "badge_fill": "#061f17",
            "pillars": [
                ("01 · CAMPO", "Ingeniería Inversa Documentada", "Trazado cable a cable de tableros, máquinas y redes sin planos previos."),
                ("02 · PLANOS", "Planos Eléctricos y de Red", "Diagramas unifilares, borneras rotuladas, topologías WAN/VPN y tabla de IPs."),
                ("03 · ENTREGABLE", "Matriz de Fallas en PDF A4", "Procedimientos Síntoma → Causa → Verificación listos para auditoría."),
            ],
        },
    ]

    for sp in specs:
        img, draw, margin_x = _create_og_canvas(
            sp["badge"],
            primary_glow=sp["glow"],
            badge_accent=sp["accent"],
            badge_border=sp["border"],
            badge_fill=sp["badge_fill"],
        )

        logo_y = s(106)
        logo_size = s(78)
        draw_ingenieria_logo(draw, margin_x, logo_y, logo_size)

        title_x = margin_x + logo_size + s(24)
        draw.text((title_x, logo_y + s(2)), sp["title"], font=font_sp_title, fill="#f8fafc")
        draw.text((title_x, logo_y + s(52)), "Ingeniería & Automatización · by Ingversia", font=font_endorse, fill="#f5821f")

        draw.text((margin_x, s(212)), sp["subtitle"], font=font_sub, fill="#cbd5e1")

        div_y = s(258)
        draw.rectangle((margin_x, div_y, W - margin_x, div_y + s(1.5)), fill="#1a263e")
        draw.rectangle((margin_x, div_y, margin_x + s(220), div_y + s(2.5)), fill=sp["accent"])

        card_y = s(292)
        card_h = s(242)
        card_gap = s(22)
        total_w = W - 2 * margin_x
        card_w = (total_w - 2 * card_gap) // 3

        for idx, (pk, pt, pd) in enumerate(sp["pillars"]):
            cx = margin_x + idx * (card_w + card_gap)
            draw.rounded_rectangle(
                (cx, card_y, cx + card_w, card_y + card_h),
                radius=s(18),
                fill=sp["card_bg"],
                outline=sp["border"],
                width=s(1.5),
            )
            draw.rounded_rectangle(
                (cx + s(22), card_y, cx + s(108), card_y + s(3.5)),
                radius=s(1.5),
                fill=sp["accent"],
            )
            draw.text((cx + s(22), card_y + s(28)), pk, font=font_card_k, fill=sp["accent"])
            draw.text((cx + s(22), card_y + s(58)), pt, font=font_card_t, fill="#f8fafc")
            lines = wrap_text(draw, pd, font_card_d, card_w - s(44))
            for li, line in enumerate(lines[:4]):
                draw.text((cx + s(22), card_y + s(102) + li * s(24)), line, font=font_card_d, fill="#94a3b8")

        _draw_og_footer(draw, margin_x)

        final_img = img.resize((FINAL_W, FINAL_H), Image.Resampling.LANCZOS)
        out_path = os.path.join(assets_dir, sp["filename"])
        final_img.save(out_path, "JPEG", quality=95, optimize=True, subsampling=0)
        print(f"OK — OG Especialidad generado en {out_path} ({FINAL_W}x{FINAL_H})")


def generate_icons():
    assets_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "html", "assets")
    os.makedirs(assets_dir, exist_ok=True)

    icon_2x = draw_favicon_symbol(360)

    apple_path = os.path.join(assets_dir, "apple-touch-icon.png")
    icon_2x.resize((180, 180), Image.Resampling.LANCZOS).save(apple_path, "PNG", optimize=True)
    print(f"OK — Apple Touch Icon generado en {apple_path} (180x180)")

    fav_path = os.path.join(assets_dir, "favicon-48.png")
    icon_2x.resize((48, 48), Image.Resampling.LANCZOS).save(fav_path, "PNG", optimize=True)
    print(f"OK — Favicon PNG generado en {fav_path} (48x48)")


if __name__ == "__main__":
    generate_og_banner()
    generate_specialty_og_banners()
    generate_icons()
