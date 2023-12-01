import math

import pandas as pd
import utils
import matplotlib.pyplot as plt

csv_filename = 'datasets/diabetes.csv'
new_df_filename = 'datasets/diabetes_appended.csv'
params_to_analysis = ["BloodPressure", "Insulin", "BMI", "Pregnancies"]

plt.rcParams.update({
    "lines.color": "white",
    "patch.edgecolor": "white",
    "text.color": "black",
    "axes.facecolor": "white",
    "axes.edgecolor": "lightgray",
    "axes.labelcolor": "white",
    "xtick.color": "white",
    "ytick.color": "white",
    "grid.color": "lightgray",
    "figure.facecolor": "black",
    "figure.edgecolor": "black",
    "savefig.facecolor": "black",
    "savefig.edgecolor": "black"})

if __name__ == '__main__':
    df = pd.read_csv(csv_filename)

    df_pred = utils.create_regression_data(df, ["BloodPressure", "BMI"])
    df_pred = df_pred.sort_values(by="BloodPressure")
    plot = df_pred.plot(
        kind='line',
        x='BloodPressure',
        y=['Original BMI', 'Predicted BMI']
    )
    plt.savefig("static/plot.png",
                edgecolor='White',
                transparent=True)
    plt.show()
