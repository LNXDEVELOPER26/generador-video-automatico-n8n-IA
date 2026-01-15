# N8N Video Generator

Sistema de automatizacion para generar videos estilo diapositiva usando n8n como orquestador. Combina generacion de imagenes, texto a voz y renderizado de video en un flujo de trabajo visual.

> [!CAUTION]
> **Requisitos de ubicacion obligatorios:**
> - El proyecto DEBE estar en `C:/generador-video-automatico-n8n-IA/`
> - NO cambiar nombres de carpetas (IMG, IMGSUB, AUDIO, PRODUCCION, Fuente, N8n Plantilla)
> - NO borrar la carpeta `Fuente/` ni las tipografias que contiene
> - NO mover ni renombrar los archivos `.py`

## Requisitos

- Python 3.10 o superior
- n8n 2.2.5 o superior
- FFmpeg (instalado y en PATH)
- Dependencias Python (ver `requirements.txt`)

## Estructura del Proyecto

```
n8nvideo/
├── N8n Plantilla/
│   ├── DEVDOP.json          # Workflow de n8n (importar en n8n)
│
├── Fuente/                   # Tipografias para los slides
├── INICIAR_N8N.bat          # Lanzador de n8n con variables configuradas
├── generar_slide_educativo.py
├── generar_slide_narrativo.py
├── generar_video.py
├── crear_voz_gratis.py
├── exportar_guion.py
└── README.md
```

## Carpetas del Sistema

| Carpeta | Modificar | Descripcion |
|---------|-----------|-------------|
| `IMG/` | NO | Imagenes generadas por DALL-E (se crean automaticamente) |
| `IMGSUB/` | NO | Slides con texto superpuesto (se crean automaticamente) |
| `AUDIO/` | NO | Archivos de audio TTS (se crean automaticamente) |
| `PRODUCCION/` | SI | Videos y guiones finales, puedes borrar contenido antiguo |
| `Fuente/` | NO | Tipografias requeridas, no borrar |
| `N8n Plantilla/` | NO | Workflow de n8n, solo importar en n8n |

> [!TIP]
> Solo la carpeta `PRODUCCION/` contiene archivos que puedes eliminar libremente para liberar espacio.

## Instalacion

1. Instalar Python 3.10+ desde https://python.org
2. Instalar dependencias Python:
   ```bash
   pip install -r requirements.txt
   ```
3. Instalar FFmpeg:
   - **Windows**: Descargar de https://ffmpeg.org/download.html y agregar al PATH
   - O usar: `winget install ffmpeg`
4. Instalar n8n (version 2.2.5):
   ```bash
   npm install -g n8n@2.2.5
   ```
5. Importar `N8n Plantilla/DEVDOP.json` en n8n

## Configuracion de APIs

Despues de importar el workflow en n8n, debes configurar tus propias claves de acceso:

1. **Nodo "Cerebro IA"** (OpenRouter)
   - Abre el nodo "Cerebro IA" en el workflow
   - En Headers > Authorization, reemplaza `TU_API_KEY_OPENROUTER` con tu clave de OpenRouter
   - Obtener clave: https://openrouter.ai/keys

2. **Nodo "DALL-E"** (OpenAI)
   - Abre el nodo "DALL-E" en el workflow
   - En Headers > Authorization, reemplaza `TU_API_KEY_OPENAI` con tu clave de OpenAI
   - Obtener clave: https://platform.openai.com/api-keys

## Uso

1. Ejecutar `INICIAR_N8N.bat`
2. Abrir `http://localhost:5678` en el navegador
3. Activar el workflow DEVDOP
4. Configurar el contenido del video en el nodo inicial
5. Ejecutar el workflow

## Modos de Video

- **Educativo**: Formato pregunta-respuesta con muletillas de transicion
- **Narrativo**: Formato titulo-parrafo para contar historias

## Campos del Formulario

### Configuracion Principal

| Campo | Tipo | Descripcion |
|-------|------|-------------|
| `modo_video` | Dropdown | Selecciona entre `narrativa` o `educativa` |
| `input_texto` | Textarea | Texto base para generar el video |
| `usar_ia` | Checkbox | Si esta activo, la IA genera y expande el contenido |
| `num_escenas` | Numero | Cantidad de escenas a generar (default: 5) |
| `caracteres_objetivo` | Numero | Longitud aproximada del guion (default: 3000) |
| `idioma` | Dropdown | Idioma del video: `es`, `en`, `pt` |
| `formato_video` | Dropdown | Resolucion: `720p`, `360p`, o ambas |

### Personalizacion Visual

| Campo | Tipo | Descripcion |
|-------|------|-------------|
| `filtro` | Dropdown | Estilo visual: `cinema`, `vintage`, `noir`, `cyber` |
| `color_titulo` | Color | Color del titulo (hex, default: #FFD700) |
| `color_parrafo` | Color | Color del texto narrativo (hex, default: #FFFFFF) |
| `color_pregunta` | Color | Color de preguntas en modo educativo (hex, default: #00BFFF) |
| `color_respuesta` | Color | Color de respuestas en modo educativo (hex, default: #32CD32) |
| `fuente_titulo` | Dropdown | Tipografia para titulos |
| `fuente_parrafo` | Dropdown | Tipografia para parrafos |
| `fuente_pregunta` | Dropdown | Tipografia para preguntas |
| `fuente_respuesta` | Dropdown | Tipografia para respuestas |
| `tamano_fuente` | Numero | Tamano base de la fuente (default: 48) |

### Margenes y Alineacion

| Campo | Tipo | Descripcion |
|-------|------|-------------|
| `margen_arriba` | Numero | Espacio superior en pixeles (default: 50) |
| `margen_izquierda` | Numero | Espacio izquierdo en pixeles (default: 50) |
| `margen_derecha` | Numero | Espacio derecho en pixeles (default: 50) |
| `margen_abajo` | Numero | Espacio inferior en pixeles (default: 50) |
| `alineacion` | Dropdown | Alineacion del texto: `izquierda`, `centro`, `derecha` |

### Opciones Avanzadas

| Campo | Tipo | Descripcion |
|-------|------|-------------|
| `fix_visual` | Textarea | Correcciones por escena (ej: "Escena 2: fondo oscuro") |
| `es_correccion` | Checkbox | Solo regenera slides sin llamar a DALL-E |
| `forzar_video` | Checkbox | Genera video sin procesar escenas nuevas |

## Scripts

| Script | Funcion |
|--------|---------|
| `generar_slide_educativo.py` | Genera imagenes con formato pregunta/respuesta |
| `generar_slide_narrativo.py` | Genera imagenes con formato titulo/parrafo |
| `crear_voz_gratis.py` | Convierte texto a audio usando Edge TTS |
| `generar_video.py` | Ensambla imagenes y audios en video MP4 |
| `exportar_guion.py` | Exporta el guion a archivo TXT |

## Creditos

**DEVDOP**
- Web: https://www.devdop.com/
- Autor: Jose Michel Mejia
- YouTube: https://www.youtube.com/@DEVDOPIT

## Licencia

MIT License
