import sys
import os
import io
import argparse
import base64
import re
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

FONT_DIR = "C:/generador-video-automatico-n8n-IA/Fuente"
FALLBACK_FONTS = ["C:/Windows/Fonts/arialbd.ttf", "C:/Windows/Fonts/arial.ttf"]

FILTROS = {
    "ninguno": {"brillo": 1.0, "contraste": 1.0, "saturacion": 1.0, "tinte": None},
    "cinema": {"brillo": 0.75, "contraste": 1.25, "saturacion": 0.9, "tinte": (15, 5, -5)},
    "vintage": {"brillo": 0.85, "contraste": 0.9, "saturacion": 0.6, "tinte": (30, 15, -10)},
    "noir": {"brillo": 0.7, "contraste": 1.4, "saturacion": 0.0, "tinte": None},
    "cyber": {"brillo": 0.8, "contraste": 1.3, "saturacion": 1.4, "tinte": (-15, 5, 30)}
}

FONT_MAP = {
    "roboto": {"bold": "roboto/Roboto-Bold.ttf", "regular": "roboto/Roboto-Regular.ttf"},
    "poppins": {"bold": "poppins/Poppins-Bold.ttf", "regular": "poppins/Poppins-Regular.ttf"},
    "inter": {"bold": "inter/Inter-Bold.ttf", "regular": "inter/Inter-Regular.ttf"},
    "montserrat": {"bold": "montserrat/Montserrat-Bold.ttf", "regular": "montserrat/Montserrat-Regular.ttf"},
    "open-sans": {"bold": "open-sans/OpenSans-Bold.ttf", "regular": "open-sans/OpenSans-Regular.ttf"},
    "nunito": {"bold": "nunito/Nunito-Bold.ttf", "regular": "nunito/Nunito-Regular.ttf"},
    "mulish": {"bold": "mulish/Mulish-Bold.ttf", "regular": "mulish/Mulish-Regular.ttf"},
    "manrope": {"bold": "manrope/Manrope-Bold.ttf", "regular": "manrope/Manrope-Regular.ttf"},
    "work-sans": {"bold": "work-sans/WorkSans-Bold.ttf", "regular": "work-sans/WorkSans-Regular.ttf"},
    "dm-sans": {"bold": "dm-sans/DMSans-Bold.ttf", "regular": "dm-sans/DMSans-Regular.ttf"},
    "heebo": {"bold": "heebo/Heebo-Bold.ttf", "regular": "heebo/Heebo-Regular.ttf"},
    "archivo": {"bold": "archivo/Archivo-Bold.ttf", "regular": "archivo/Archivo-Regular.ttf"},
    "cinzel": {"bold": "Cinzel/Cinzel-Bold.ttf", "regular": "Cinzel/Cinzel-Regular.ttf"},
    "cinzel-decorative": {"bold": "Cinzel_Decorative/CinzelDecorative-Bold.ttf", "regular": "Cinzel_Decorative/CinzelDecorative-Regular.ttf"},
    "cormorant": {"bold": "OpenType Font Files/Cormorant-Bold.otf", "regular": "OpenType Font Files/Cormorant-Regular.otf"},
    "ibm-plex-sans": {"bold": "ibm-plex-sans/IBMPlexSans-Bold.ttf", "regular": "ibm-plex-sans/IBMPlexSans-Regular.ttf"},
    "source-sans": {"bold": "source-sans-3/SourceSans3-Bold.ttf", "regular": "source-sans-3/SourceSans3-Regular.ttf"},
}

def decode_text(text, is_base64=False):
    if not text:
        return ""
    if is_base64:
        try:
            return base64.b64decode(text).decode('utf-8')
        except:
            return text
    return text

def get_font_by_name(font_name, size, bold=True):
    font_name = font_name.lower().strip() if font_name else "roboto"
    variant = "bold" if bold else "regular"
    
    if font_name in FONT_MAP:
        font_path = os.path.join(FONT_DIR, FONT_MAP[font_name][variant])
        if os.path.exists(font_path):
            try:
                return ImageFont.truetype(font_path, size)
            except:
                pass
    
    for subdir in os.listdir(FONT_DIR):
        subdir_path = os.path.join(FONT_DIR, subdir)
        if os.path.isdir(subdir_path) and font_name in subdir.lower():
            for f in os.listdir(subdir_path):
                fl = f.lower()
                if (fl.endswith('.ttf') or fl.endswith('.otf')):
                    if (bold and 'bold' in fl) or (not bold and 'regular' in fl):
                        try:
                            return ImageFont.truetype(os.path.join(subdir_path, f), size)
                        except:
                            continue
            for f in os.listdir(subdir_path):
                if f.lower().endswith('.ttf') or f.lower().endswith('.otf'):
                    try:
                        return ImageFont.truetype(os.path.join(subdir_path, f), size)
                    except:
                        continue
    
    for fb in FALLBACK_FONTS:
        if os.path.exists(fb):
            try:
                return ImageFont.truetype(fb, size)
            except:
                continue
    return ImageFont.load_default()

def aplicar_filtro(img, filtro_nombre):
    if filtro_nombre not in FILTROS:
        filtro_nombre = "cinema"
    f = FILTROS[filtro_nombre]
    img = ImageEnhance.Brightness(img).enhance(f["brillo"])
    img = ImageEnhance.Contrast(img).enhance(f["contraste"])
    img = ImageEnhance.Color(img).enhance(f["saturacion"])
    if f["tinte"] and img.mode == "RGB":
        try:
            r, g, b = img.split()
            r = r.point(lambda x: min(255, max(0, x + f["tinte"][0])))
            g = g.point(lambda x: min(255, max(0, x + f["tinte"][1])))
            b = b.point(lambda x: min(255, max(0, x + f["tinte"][2])))
            img = Image.merge("RGB", (r, g, b))
        except:
            pass
    return img

def crear_gradiente(w, h, centrado=False):
    overlay = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    if centrado:
        for y in range(h):
            draw.line([(0, y), (w, y)], fill=(0, 0, 0, 160))
    else:
        inicio = int(h * 0.35)
        for y in range(inicio, h):
            progreso = (y - inicio) / (h - inicio)
            alpha = int(240 * (progreso ** 1.2))
            draw.line([(0, y), (w, y)], fill=(0, 0, 0, alpha))
    return overlay

def wrap_text(text, font, max_width, draw):
    if not text:
        return []
    words = text.split()
    lines = []
    line = ""
    for word in words:
        test = line + word + " "
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] <= max_width:
            line = test
        else:
            if line:
                lines.append(line.strip())
            line = word + " "
    if line:
        lines.append(line.strip())
    return lines

def calcular_x(alineacion, line, font, draw, margen_x, max_w, w):
    if alineacion == "centro":
        bbox = draw.textbbox((0, 0), line, font=font)
        text_w = bbox[2] - bbox[0]
        return (w - text_w) // 2
    elif alineacion == "derecha":
        bbox = draw.textbbox((0, 0), line, font=font)
        text_w = bbox[2] - bbox[0]
        return w - margen_x - text_w
    else:
        return margen_x

def get_font_scale(tamano):
    try:
        return int(tamano) / 48.0
    except:
        return 1.0

def dibujar_texto(draw, x, y, texto, font, color, sombra=3):
    for dx in range(-sombra, sombra+1):
        for dy in range(-sombra, sombra+1):
            if dx != 0 or dy != 0:
                draw.text((x + dx, y + dy), texto, font=font, fill="#000000")
    draw.text((x, y), texto, font=font, fill=color)

def generar(entrada, titulo, parrafo, color_titulo, color_parrafo, fuente_titulo, fuente_parrafo, salida, filtro="cinema", is_base64=False, tamano_fuente="48", margen_arriba="100", margen_izquierda="50", margen_derecha="50", margen_abajo="50", alineacion="izquierda"):
    try:
        titulo = decode_text(titulo, is_base64)
        parrafo = decode_text(parrafo, is_base64)
        
        if not os.path.exists(entrada):
            print(f"ERROR: Imagen no encontrada: {entrada}")
            sys.exit(1)
        
        img = Image.open(entrada).convert("RGB")
        img = aplicar_filtro(img, filtro)
        w, h = img.size
        
        es_centrado = alineacion == "centro"
        img_rgba = img.convert('RGBA')
        gradiente = crear_gradiente(w, h, centrado=es_centrado)
        img = Image.alpha_composite(img_rgba, gradiente).convert('RGB')
        
        draw = ImageDraw.Draw(img)
        try:
            m_arriba = int(margen_arriba)
            m_izq = int(margen_izquierda)
            m_der = int(margen_derecha)
            m_abajo = int(margen_abajo)
        except:
            m_arriba, m_izq, m_der, m_abajo = 100, 50, 50, 50
        max_w = w - m_izq - m_der
        escala = get_font_scale(tamano_fuente)
        
        if es_centrado:
            all_lines = []
            line_heights = []
            
            if titulo and titulo.strip():
                font_titulo = get_font_by_name(fuente_titulo, int(h * 0.07 * escala), bold=True)
                lines_t = wrap_text(titulo.upper(), font_titulo, max_w, draw)
                for line in lines_t:
                    all_lines.append((line, font_titulo, "#FFD700", 3))
                    line_heights.append(int(h * 0.08 * escala))
            
            if parrafo and parrafo.strip():
                font_parrafo = get_font_by_name(fuente_parrafo, int(h * 0.05 * escala), bold=False)
                lines_p = wrap_text(parrafo, font_parrafo, max_w, draw)
                for line in lines_p:
                    all_lines.append((line, font_parrafo, "#FFFFFF", 2))
                    line_heights.append(int(h * 0.06 * escala))
            
            total_height = sum(line_heights)
            y = (h - total_height) // 2
            
            for i, (line, font, color, sombra) in enumerate(all_lines):
                bbox = draw.textbbox((0, 0), line, font=font)
                text_w = bbox[2] - bbox[0]
                x = (w - text_w) // 2
                dibujar_texto(draw, x, y, line, font, color, sombra=sombra)
                y += line_heights[i]
        else:
            y = m_arriba
            
            if titulo and titulo.strip():
                font_titulo = get_font_by_name(fuente_titulo, int(h * 0.08 * escala), bold=True)
                lines_titulo = wrap_text(titulo.upper(), font_titulo, max_w, draw)
                for line in lines_titulo:
                    x = calcular_x(alineacion, line, font_titulo, draw, m_izq, max_w, w)
                    dibujar_texto(draw, x, y, line, font_titulo, "#FFD700", sombra=3)
                    y += int(h * 0.07 * escala)
            
            y += int(h * 0.02)
            
            if parrafo and parrafo.strip():
                font_parrafo = get_font_by_name(fuente_parrafo, int(h * 0.055 * escala), bold=False)
                lines_parrafo = wrap_text(parrafo, font_parrafo, max_w, draw)
                for line in lines_parrafo:
                    x = calcular_x(alineacion, line, font_parrafo, draw, m_izq, max_w, w)
                    dibujar_texto(draw, x, y, line, font_parrafo, "#FFFFFF", sombra=2)
                    y += int(h * 0.045 * escala)

        output_dir = os.path.dirname(salida)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        img.save(salida, quality=95)
        print(f"OK: {salida}")
        
    except Exception as e:
        print(f"ERROR: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--entrada", required=True)
    p.add_argument("--titulo", default="")
    p.add_argument("--parrafo", required=True)
    p.add_argument("--color_titulo", default="#FFD700")
    p.add_argument("--color_parrafo", default="#FFFFFF")
    p.add_argument("--fuente_titulo", default="roboto")
    p.add_argument("--fuente_parrafo", default="roboto")
    p.add_argument("--filtro", default="cinema")
    p.add_argument("--tamano_fuente", default="48")
    p.add_argument("--margen_arriba", default="100")
    p.add_argument("--margen_izquierda", default="50")
    p.add_argument("--margen_derecha", default="50")
    p.add_argument("--margen_abajo", default="50")
    p.add_argument("--alineacion", default="izquierda")
    p.add_argument("--salida", required=True)
    p.add_argument("--base64", action="store_true")
    args = p.parse_args()
    
    generar(args.entrada, args.titulo, args.parrafo, args.color_titulo, args.color_parrafo, args.fuente_titulo, args.fuente_parrafo, args.salida, args.filtro, args.base64, args.tamano_fuente, args.margen_arriba, args.margen_izquierda, args.margen_derecha, args.margen_abajo, args.alineacion)