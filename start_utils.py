import math

import pandas as pd
import utils
import matplotlib.pyplot as plt

csv_filename = 'datasets/diabetes.csv'
new_df_filename = 'datasets/diabetes_appended.csv'
params_to_analysis = ["BloodPressure", "Insulin", "BMI", "Pregnancies"]

if __name__ == '__main__':
    df = pd.read_csv(csv_filename)

    model, _, dataframe = utils.get_predict_from_desicion_tree(df,
                                                            ["Age", "BMI"],
                                                            "BloodPressure",
                                                            input_rows=25,
                                                            output_rows=5,
                                                            shuffle=True)
    dataframe = dataframe.reset_index(drop=True)
    dataframe.reset_index(inplace=True)
    dataframe = dataframe[["index", "BloodPressure", "Predicted BloodPressure"]]
    utils.get_plot_from_dataset(
        dataframe=dataframe,
        x="index",
        y=["BloodPressure", "Predicted BloodPressure"]
    )
    plt.show()
