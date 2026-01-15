import sys
import base64
import asyncio
import edge_tts
import os

VOICE_ES = "es-MX-JorgeNeural"
VOICE_EN = "en-US-GuyNeural"
VOICE_PT = "pt-BR-AntonioNeural"

async def run_tts(base64_text, output_file, lang="es"):
    voices = {"es": VOICE_ES, "en": VOICE_EN, "pt": VOICE_PT}
    voice = voices.get(lang.lower()[:2], VOICE_ES)
    
    try:
        text = base64.b64decode(base64_text).decode('utf-8')
        if not text.strip():
            print("ERROR: Texto vacio")
            sys.exit(1)
        
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
            
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_file)
        
        if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
            print(f"OK: {output_file}")
        else:
            print("ERROR: Archivo de audio vacio")
            sys.exit(1)
            
    except base64.binascii.Error:
        print("ERROR: Base64 invalido")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("USO: python crear_voz_gratis.py <base64_text> <output.mp3> [idioma]")
        sys.exit(1)
    
    lang = sys.argv[3] if len(sys.argv) > 3 else "es"
    asyncio.run(run_tts(sys.argv[1], sys.argv[2], lang))