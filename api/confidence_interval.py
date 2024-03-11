######## HEADER TO CONFIGURE LOGS ########
import logging
log = logging.getLogger(__name__)
##########################################

from typing import Tuple
import numpy as np
import pandas as pd

from modelbuilder.dataset import Dataset

class ConfidenceInterval:
    """
    Clase estandar de comportamiento de un objeto ConfidenceInterval
    """
    
    def fit(self, dataset: Dataset) -> None:
        self.dataset = dataset
        self.train_err = self.dataset.get_y() - self.dataset.data["prediction_train"]

    def transform(self, model_input: Dataset, base_error: float) -> Tuple[np.ndarray, np.ndarray]:
        # Cálculo ci
        ci = base_error

        # Cálculo ci_min y ci_max
        predictions = model_input.data["prediction"].to_numpy()
        ci_min = predictions - ci
        ci_max = predictions + ci
        return ci_min, ci_max
    
class ConfidenceIntervalEnsemble(ConfidenceInterval):
    """
    Subclase ConfidenceInterval calculado segun el acierto del modelo (error del modelo)
    y la diferencia entre modelos del ensemble (std de las predicciones unitarias)
    ci = sqrt(err**2 + std(modelos)**2)
    """

    def fit(self, dataset: Dataset) -> None:
        super().fit(dataset)
        self.sigma2 = (self.train_err ** 2).mean()
        # almacenando error de entrenamiento por fuel_type
        try:
            self.sigma2_fuel_type = pd.concat([self.dataset.data.Fuel_type,
                                            self.train_err ** 2], axis=1).groupby("Fuel_type").mean().iloc[:,0]
        except:
            log.warning("Error obteniendo sigma2_fuel_type durante entrenamiento.")

    def transform(self, model_input: Dataset, base_error: float) -> Tuple[np.ndarray, np.ndarray]:
        # recuperando predicciones individuales de los modelos en el ensemble
        pred_cols = [col for col in model_input.columns.predictions if col[:11]=="prediction_"]
        pred_partials = model_input.data[pred_cols]

        # Calculo anchura intervalo de confianza
        try:
            ci = np.sqrt(model_input.data.Fuel_type.map(self.sigma2_fuel_type).fillna(self.sigma2) + (pred_partials.std(axis=1)*2)**2)
        except:
            log.warning("Error aplicando sigma2_fuel_type")
            if hasattr(self, "sigma2"):
                ci = np.sqrt(self.sigma2 + (pred_partials.std(axis=1)*2)**2)
            else:
                ci = np.sqrt(base_error**2 + (pred_partials.std(axis=1)*2)**2)
        ci = 0.001 * ci
        # Cálculo ci_min y ci_max
        predictions = model_input.data["prediction"].to_numpy()
        ci_min = predictions - ci
        ci_max = predictions + ci
        return ci_min, ci_max