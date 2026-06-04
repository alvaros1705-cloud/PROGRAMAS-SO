# WebOS 7 - Carpeta de Imágenes

============================================================
  FONDOS DE PANTALLA
============================================================
Coloca tus imágenes de fondo aquí con estos nombres exactos:

  wallpaper_win7.jpg           -> Fondo predeterminado (Windows 7 clásico)
  wallpaper_architecture.jpg   -> Fondo Arquitectura
  wallpaper_landscapes.jpg     -> Fondo Paisajes
  wallpaper_nature.jpg         -> Fondo Naturaleza

Para agregar más fondos:
1. Copia tu imagen JPG/PNG a esta carpeta
2. Edita WIN7.html y busca "wallpapers:" en el JavaScript
3. Agrega: { url: 'images/tu_imagen.jpg', color: 'rgba(R,G,B,0.55)', name: 'Nombre' }

============================================================
  ÍCONOS PERSONALIZADOS
============================================================
Tienes DOS formas de cambiar los íconos:

1. DESDE EL SISTEMA (más fácil):
   - Haz clic DERECHO en el escritorio
   - Selecciona "Personalizar íconos"
   - Pega la URL de tu ícono en el campo correspondiente
   - Ejemplos de URLs:
     * https://win7simu.visnalize.com/img/icons/notepad.png
     * images/mi_icono.png  (imagen en esta misma carpeta)
     * https://img.icons8.com/color/96/calculator.png

2. EDITANDO EL HTML:
   Busca "icons:" en el JavaScript y cambia las URLs directamente.

============================================================
  NOTAS TÉCNICAS
============================================================
- Resolución recomendada para fondos: 1920x1080 o 1366x768
- Formatos soportados: JPG, PNG, WEBP, GIF
- El HTML y la carpeta images/ deben estar en la misma ubicación
- Los íconos se guardan en localStorage del navegador
- Si los íconos no cargan, se muestran emojis como respaldo
