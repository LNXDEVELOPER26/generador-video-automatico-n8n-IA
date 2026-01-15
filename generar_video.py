import os
import sys
import glob
import subprocess
from datetime import datetime

BASE_DIR = "C:/generador-video-automatico-n8n-IA"
SUB_DIR = os.path.join(BASE_DIR, "IMGSUB")
AUDIO_DIR = os.path.join(BASE_DIR, "AUDIO")
PROD_DIR = os.path.join(BASE_DIR, "PRODUCCION")

def ensamblar_video(formatos_str="720p"):
    os.makedirs(PROD_DIR, exist_ok=True)
    
    imagenes = sorted(
        [f for f in os.listdir(SUB_DIR) if f.startswith('final_') and f.endswith('.jpg')],
        key=lambda x: int(x.split('_')[1].split('.')[0])
    )
    
    if not imagenes:
        print("ERROR: No hay imagenes en IMGSUB")
        return False
    
    print(f"LOG: {len(imagenes)} imagenes encontradas")
    
    concat_file = os.path.join(BASE_DIR, "concat_list.txt")
    with open(concat_file, 'w', encoding='utf-8') as f:
        for img_name in imagenes:
            idx = img_name.split('_')[1].split('.')[0]
            img_path = os.path.join(SUB_DIR, img_name).replace('\\', '/')
            audio_path = os.path.join(AUDIO_DIR, f"audio_{idx}.mp3").replace('\\', '/')
            
            if not os.path.exists(audio_path):
                alt = sorted(glob.glob(os.path.join(AUDIO_DIR, "audio_*.mp3")))
                if alt:
                    audio_path = alt[0].replace('\\', '/')
                else:
                    continue
            
            duration = get_audio_duration(audio_path)
            if duration > 0:
                f.write(f"file '{img_path}'\n")
                f.write(f"duration {duration}\n")
                print(f"  {img_name} -> {duration:.2f}s")
        
        if imagenes:
            last_img = os.path.join(SUB_DIR, imagenes[-1]).replace('\\', '/')
            f.write(f"file '{last_img}'\n")
    
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    output = os.path.join(PROD_DIR, f"video_{ts}_720p.mp4")
    
    audio_inputs = []
    filter_parts = []
    for i, img_name in enumerate(imagenes):
        idx = img_name.split('_')[1].split('.')[0]
        audio_path = os.path.join(AUDIO_DIR, f"audio_{idx}.mp3")
        if os.path.exists(audio_path):
            audio_inputs.extend(['-i', audio_path])
            filter_parts.append(f"[{i+1}:a]")
    
    if not filter_parts:
        print("ERROR: No hay audios")
        return False
    
    audio_filter = f"{''.join(filter_parts)}concat=n={len(filter_parts)}:v=0:a=1[aout]"
    
    cmd = [
        'ffmpeg', '-y',
        '-f', 'concat', '-safe', '0', '-i', concat_file,
    ]
    cmd.extend(audio_inputs)
    cmd.extend([
        '-filter_complex', audio_filter,
        '-map', '0:v', '-map', '[aout]',
        '-c:v', 'libx264', '-preset', 'ultrafast', '-crf', '23',
        '-c:a', 'aac', '-b:a', '128k',
        '-pix_fmt', 'yuv420p',
        '-shortest',
        output
    ])
    
    print(f"LOG: Renderizando video...")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        if result.returncode == 0:
            print(f"OK: {output}")
            try:
                os.remove(concat_file)
            except:
                pass
            return True
        else:
            print(f"ERROR: {result.stderr[:500]}")
            return False
    except subprocess.TimeoutExpired:
        print("ERROR: Timeout")
        return False
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def get_audio_duration(path):
    try:
        cmd = ['ffprobe', '-v', 'quiet', '-show_entries', 'format=duration', 
               '-of', 'default=noprint_wrappers=1:nokey=1', path]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        return float(result.stdout.strip())
    except:
        return 5.0

if __name__ == "__main__":
    formatos = sys.argv[1] if len(sys.argv) > 1 else "720p"
    exito = ensamblar_video(formatos)
    sys.exit(0 if exito else 1)