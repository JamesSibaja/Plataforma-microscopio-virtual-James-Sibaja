from celery import shared_task
import os
import math
import openslide
from PIL import Image
from Microscopio.models import Slide,OpenSlide

@shared_task
def convert_to_tiles(input_path, output_path, idOpenSLide, idSlide,tile_size=256):
    try:
        slide = openslide.open_slide(input_path)
        slide_width, slide_height = slide.dimensions
        num_levels = slide.level_count
        
        os.makedirs(output_path, exist_ok=True)
        
        # Calcula el nivel de zoom donde la imagen debe abarcar la totalidad de una tesela
        base_level = math.ceil(math.log(max(slide_width, slide_height) / tile_size, 2))
        # print(f"num_levels: {num_levels}")

        if (base_level>num_levels):
            base_level=num_levels
            
        for level in range(num_levels):
            # print(f"Saved: {level}--------------------------------------------")

            level_width, level_height = slide.level_dimensions[level]
            level_downsample = slide.level_downsamples[level]
            num_level_folder = base_level-level
            level_folder = os.path.join(output_path, str(num_level_folder))
            # print(f"num_level_folder: {num_level_folder}")
            if num_level_folder>=0:
                os.makedirs(level_folder, exist_ok=True)
                
                rows = math.ceil(level_height / tile_size)
                cols = math.ceil(level_width / tile_size)
                
                for row in range(rows):
                    row_folder = os.path.join(level_folder, f"{row}")
                    os.makedirs(row_folder, exist_ok=True)
                    
                    for col in range(cols):
                        x = col * tile_size * int(level_downsample)
                        y = row * tile_size * int(level_downsample)
                        
                        # tile_width = min(tile_size, level_width  - int(x/ level_downsample))
                        # tile_height = min(tile_size, level_height  - int(y/ level_downsample))
                        
                        # if tile_width <= 0 or tile_height <= 0:
                        #     continue
                        
                        tile = slide.read_region((x, y), level, (tile_size, tile_size))
                        tile = tile.convert("RGB")  # Convertir a modo RGB
                        
                        tile_filename = os.path.join(row_folder, f"{col}.jpg")
                        tile.save(tile_filename, "JPEG")
                        
                        print(f"Saved: {tile_filename}")
                print(f"row: {row}")
        rawSlide = OpenSlide.objects.get(id=idOpenSLide)
        microscopeSlide = Slide.objects.get(id=idSlide)
        rawSlide.assembled = True
        microscopeSlide.assembled = True
        microscopeSlide.zoomM = base_level
        microscopeSlide.zoomI = 1
        rawSlide.save()
        microscopeSlide.save()
        print(f"Saved: {num_levels}")
        
        
        # Calcula el nivel de zoom donde la imagen debe abarcar la totalidad de una tesela
        
        return base_level
    except Exception as e:
        # En caso de error, registra el error y retorna un mensaje de error
        print(f"An error occurred: {str(e)}")
        return f"Error: {str(e)}"
# @shared_task
# def procesar_archivo(nombre_archivo):
#     # Lógica para procesar el archivo aquí
#     # Puedes llamar a tu script de Python aquí

#     # Por ejemplo:
#     resultado = "Archivo {} procesado exitosamente".format(nombre_archivo)
#     return resultado