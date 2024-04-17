import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import learning_curve
from sklearn.datasets import load_digits
from sklearn.svm import SVC

# Cargar datos
digits = load_digits()
X, y = digits.data, digits.target

# Define el modelo
model = SVC(kernel='linear')

# Calcula las curvas de aprendizaje
train_sizes, train_scores, test_scores = learning_curve(
    model, X, y, train_sizes=np.linspace(0.1, 1.0, 10), cv=5)

# Calcula los promedios y las desviaciones estándar
train_scores_mean = np.mean(train_scores, axis=1)
train_scores_std = np.std(train_scores, axis=1)
test_scores_mean = np.mean(test_scores, axis=1)
test_scores_std = np.std(test_scores, axis=1)

# Grafica las curvas de aprendizaje
plt.figure()
plt.title("Curva de Aprendizaje (SVM)")
plt.xlabel("Tamaño del Conjunto de Entrenamiento")
plt.ylabel("Puntaje")
plt.grid()

plt.fill_between(train_sizes, train_scores_mean - train_scores_std,
                 train_scores_mean + train_scores_std, alpha=0.1,
                 color="r")
plt.fill_between(train_sizes, test_scores_mean - test_scores_std,
                 test_scores_mean + test_scores_std, alpha=0.1, color="g")
plt.plot(train_sizes, train_scores_mean, 'o-', color="r",
         label="Puntaje de Entrenamiento")
plt.plot(train_sizes, test_scores_mean, 'o-', color="g",
         label="Puntaje de Validación Cruzada")

plt.legend(loc="best")
plt.show()