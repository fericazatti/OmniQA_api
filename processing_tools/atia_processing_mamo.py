from processing_tools.base import ProcessingAlgorithm
from utils.image_processing import segment_and_draw_rois
import pydicom
import numpy as np
import cv2

class AtiaProcessingMamo(ProcessingAlgorithm):
    """
    Algoritmo de procesamiento ATIA para mamografía.
    """

    def process(self, filepath):
        """
        Carga un archivo DICOM, extrae la imagen, aplica ajustes de ventana y segmenta las ROIs.
        """
        try:
            # Cargar el archivo DICOM
            dicom_data = pydicom.dcmread(filepath)
            image_array = dicom_data.pixel_array.astype(np.float32)

            # Aplicar ajustes de ventana
            window_center = dicom_data.get("WindowCenter", np.median(image_array))
            window_width = dicom_data.get("WindowWidth", np.max(image_array) - np.min(image_array))

            if isinstance(window_center, (list, pydicom.multival.MultiValue)):
                window_center = float(window_center[0])
            if isinstance(window_width, (list, pydicom.multival.MultiValue)):
                window_width = float(window_width[0])

            # Normalizar imagen 
            min_window = window_center - (window_width / 2)
            max_window = window_center + (window_width / 2)
            image_array = np.clip(image_array, min_window, max_window)
            image_array = ((image_array - min_window) / (max_window - min_window)) * 255.0
            image_array = image_array.astype(np.uint8)

            # Extraer y dibujar ROIs específicas para ATIA
            image_with_rois, rois = segment_and_draw_rois(image_array)

            return {
                        "image": image_with_rois,
                        "rois": rois,
                        "metrics": {},
                        "log": "ROIs segmentadas correctamente"
            }
            
        except Exception as e:
            print(f"❌ Error en ATIA Processing Mamo: {e}")
            return None, []
