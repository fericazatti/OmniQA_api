from processing_tools.atia_processing_mamo import AtiaProcessingMamo
from processing_tools.iq_daily_ct import IqDailyCt  # ← asegurate que esté en processing_tools/

class ProcessingFactory:
    """
    Fábrica de algoritmos de procesamiento.
    Determina qué algoritmo aplicar en función del tipo de imagen y estudio.
    """

    @staticmethod
    def get_algorithm(modality, study_description):
        modality = (modality or "").lower().strip()
        study_description = (study_description or "").lower().strip()

        # Mamografía: ATIA
        if modality == "mg" and any(kw in study_description for kw in ["atia"]):
            return AtiaProcessingMamo()

        # Tomografía: fantoma de calidad
        if modality == "ct" and any(kw in study_description for kw in ["daily", "diario", ""]):
            return IqDailyCt()

        print(f"⚠️ Rechazo esperado: No hay un algoritmo asignado para {modality} - {study_description}")
        return None
