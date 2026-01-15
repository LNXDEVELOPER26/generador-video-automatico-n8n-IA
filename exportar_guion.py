import os
import json
from datetime import datetime

BASE_DIR = "C:/generador-video-automatico-n8n-IA"
ESCENAS_FILE = os.path.join(BASE_DIR, "escenas_temp.json")
PROD_DIR = os.path.join(BASE_DIR, "PRODUCCION")

def exportar_guion():
    if not os.path.exists(ESCENAS_FILE):
        print("ERROR: No existe escenas_temp.json")
        return False
    
    try:
        with open(ESCENAS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"ERROR: JSON invalido - {e}")
        return False
    except Exception as e:
        print(f"ERROR: No se pudo leer archivo - {e}")
        return False
    
    scenes = data.get('scenes', [])
    modo = data.get('modo', 'narrativa')
    idioma = data.get('idioma', 'es')
    
    if not scenes:
        print("ERROR: No hay escenas en el JSON")
        return False
    
    os.makedirs(PROD_DIR, exist_ok=True)
    
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(PROD_DIR, f"guion_{ts}.txt")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"GUION - {modo.upper()} - {idioma.upper()}\n")
        f.write(f"Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 50 + "\n\n")
        
        for i, scene in enumerate(scenes, 1):
            f.write(f"--- ESCENA {i} ---\n\n")
            
            if modo == 'educativa':
                pregunta = scene.get('pregunta', '')
                respuesta = scene.get('respuesta', '')
                f.write(f"PREGUNTA:\n{pregunta}\n\n")
                f.write(f"RESPUESTA:\n{respuesta}\n\n")
            else:
                titulo = scene.get('titulo', '')
                parrafo = scene.get('parrafo', scene.get('texto', ''))
                if titulo:
                    f.write(f"TITULO:\n{titulo}\n\n")
                f.write(f"TEXTO:\n{parrafo}\n\n")
            
            f.write("\n")
    
    print(f"OK: Guion exportado a {output_file}")
    return True

if __name__ == "__main__":
    exito = exportar_guion()
    exit(0 if exito else 1)
