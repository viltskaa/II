import utils
import pandas as pd
import matplotlib.pyplot as plt

csv_filename = 'datasets/diabetes.csv'
new_df_filename = 'datasets/diabetes_appended.csv'
params_to_analysis = ["BloodPressure", "Insulin", "BMI", "Pregnancies"]

if __name__ == '__main__':
    df = pd.read_csv(csv_filename)
    df_new = utils.append_dataset(dataframe=df,
                                  percent_to_add=0.1,
                                  shuffle=False,
                                  filename=new_df_filename)

    for column in params_to_analysis:
        dataframe_original = utils.data_analysis(df, column)
        dataframe_appended = utils.data_analysis(df_new, column)
        dataframe_appended = dataframe_appended.iloc[:, 1:].add_suffix("+")
        dataframe_original = dataframe_original.join(dataframe_appended)

        ax = dataframe_original.plot.bar(x="AgeGroup", figsize=(16, 8), title=f"{column}-analysis")
        for container in ax.containers:
            ax.bar_label(container, label_type='edge')
        plt.show()
