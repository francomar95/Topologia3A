# -*- coding: utf-8 -*-
"""diabetes_model.py

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1cTTMhP7L_N-CzGROjnoPG0sbnG8T3Lgg
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.metrics import mean_squared_error, accuracy_score, confusion_matrix, roc_auc_score, roc_curve
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, cross_val_score
import requests
from io import StringIO

class DiabetesModel:
    def __init__(self, url):
        self.url = url
        self.data = self.load_data()
        self.scaler = StandardScaler()  # Inicializar el scaler aquí
        self.X_scaled, self.y = self.preprocess_data()
        self.model_logistic = None
        self.model_linear = None

    def load_data(self):
        response = requests.get(self.url)
        csv_content = response.content.decode('utf-8')
        data = pd.read_csv(StringIO(csv_content))
        return data

    def plot_heatmap(self):
        correlations = self.data.corr()
        plt.figure(figsize=(10, 8))
        sns.heatmap(correlations, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
        plt.title('Mapa de calor de correlaciones')
        plt.show()

    def plot_scatter(self):
        plt.figure(figsize=(8, 6))
        plt.scatter(self.data['glucosa'], self.data['imc'], color='blue', alpha=0.5)
        plt.title('Diagrama de Dispersión: Glucosa vs IMC')
        plt.xlabel('Glucosa en la Sangre')
        plt.ylabel('IMC')
        plt.grid(True)
        plt.show()

    def plot_regression(self, x, y):
        plt.figure(figsize=(10, 6))
        sns.regplot(data=self.data, x=x, y=y, logistic=True, ci=None, scatter_kws={'alpha': 0.5})
        plt.title(f'Relación entre {x} y {y} con regresión')
        plt.xlabel(x.capitalize())
        plt.ylabel(y.capitalize())
        plt.show()

    def preprocess_data(self):
        X = self.data[['imc', 'glucosa']]
        y = self.data['diabetes']
        X_scaled = self.scaler.fit_transform(X)
        return X_scaled, y

    def train_logistic_regression(self):
        X_train, X_test, y_train, y_test = train_test_split(self.X_scaled, self.y, test_size=0.2, random_state=42)
        self.model_logistic = LogisticRegression(max_iter=1000)
        self.model_logistic.fit(X_train, y_train)
        predicciones = self.model_logistic.predict(X_test)
        precision = accuracy_score(y_test, predicciones)
        print("Precisión del modelo:", precision)
        return X_test, y_test, predicciones

    def logistic_regression_metrics(self, X_test, y_test, predicciones):
        print("Coeficientes de la regresión logística:")
        print("Intercepto:", self.model_logistic.intercept_)
        print("Coeficientes:", self.model_logistic.coef_)

        cm = confusion_matrix(y_test, predicciones)
        print("Matriz de confusión:\n", cm)
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False)
        plt.title('Matriz de Confusión')
        plt.xlabel('Predicción')
        plt.ylabel('Actual')
        plt.show()

        y_prob = self.model_logistic.predict_proba(X_test)[:, 1]
        auc_roc = roc_auc_score(y_test, y_prob)
        print("AUC-ROC:", auc_roc)
        fpr, tpr, thresholds = roc_curve(y_test, y_prob)
        plt.figure()
        plt.plot(fpr, tpr, color='darkorange', lw=2, label='Curva ROC (AUC = %0.2f)' % auc_roc)
        plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('Tasa de falsos positivos')
        plt.ylabel('Tasa de verdaderos positivos')
        plt.title('Curva ROC')
        plt.legend(loc="lower right")
        plt.show()

        cv_scores = cross_val_score(self.model_logistic, self.X_scaled, self.y, cv=5, scoring='accuracy')
        print("Puntajes de validación cruzada:", cv_scores)
        print("Puntaje medio de validación cruzada:", cv_scores.mean())

    def train_linear_regression(self):
        X = self.data['glucosa'].values.reshape(-1, 1)
        Y = self.data['imc']
        self.model_linear = LinearRegression()
        self.model_linear.fit(X, Y)

        beta_0 = self.model_linear.intercept_
        beta_1 = self.model_linear.coef_[0]
        print("Modelo de Regresión:")
        print("Intercepto (beta_0):", beta_0)
        print("Coeficiente de X (beta_1):", beta_1)
        Y_pred = self.model_linear.predict(X)

        mse = mean_squared_error(Y, Y_pred)
        print("Error cuadrático medio (MSE):", mse)

    def predict_new_data(self):
        nueva_glucosa = float(input("Introduce el nivel de glucosa: "))
        nuevo_imc = float(input("Introduce el IMC: "))
        nuevo_dato = self.scaler.transform([[nuevo_imc, nueva_glucosa]])
        prediccion = self.model_logistic.predict(nuevo_dato)
        if prediccion[0] == 1:
            print("El modelo predice que la probabilidad que la persona tenga diabetes es positiva.")
        else:
            print("El modelo predice que la probabilidad que la persona tenga diabetes es baja.")

# Uso de la clase con una URL diferente

url = "https://github.com/francomar95/Topologia3A/blob/38d5753bf696fea5de6dc9db73041d26a51ffa9a/diabetes.csv?raw=true"
model = DiabetesModel(url)

model.plot_heatmap()
model.plot_scatter()
model.plot_regression('glucosa', 'diabetes')
model.plot_regression('imc', 'diabetes')

X_test, y_test, predicciones = model.train_logistic_regression()
model.logistic_regression_metrics(X_test, y_test, predicciones)

model.train_linear_regression()

# Llamada al nuevo método de predicción
model.predict_new_data()