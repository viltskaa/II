from __future__ import annotations

from pandas import DataFrame, cut, concat
import matplotlib.pyplot as plt
import random
import math
from sklearn.linear_model import LinearRegression
from sklearn import preprocessing


def data_analysis(dataframe: DataFrame, column_to_research: str) -> DataFrame:
    if column_to_research not in dataframe.columns.values.tolist():
        return DataFrame()

    dataframe_to_analysis = dataframe[[column_to_research, "Age"]].copy()
    dataframe_to_analysis.loc[:, 'AgeGroup'] = cut(dataframe_to_analysis['Age'],
                                                   bins=[0, 18, 25, 35, 50, 65, 100],
                                                   labels=['0-18', '19-25', '26-35', '36-50', '51-65', '65+'])
    dataframe_to_analysis = dataframe_to_analysis.groupby('AgeGroup', observed=True)[column_to_research] \
        .describe().reset_index()[['AgeGroup', 'min', 'mean', 'max']] \
        .set_axis(
        ['AgeGroup', f"Min{column_to_research}", f"Avg{column_to_research}", f"Max{column_to_research}"],
        axis=1
    )
    return dataframe_to_analysis


def append_dataset(dataframe: DataFrame,
                   percent_to_add: float,
                   filename: str = "new_dataframe.csv",
                   shuffle: bool = False) -> DataFrame:
    rows_to_add = (dataframe.__len__() * percent_to_add).__int__()

    dataframe_to_add: DataFrame = dataframe \
        .copy().mean() \
        .to_frame().transpose()

    dataframe_all = dataframe.copy()
    for _ in range(rows_to_add):
        random_appended_dataframe = dataframe_to_add.copy()
        for name in random_appended_dataframe.columns.values:
            min_arg = dataframe[name].min()
            max_arg = dataframe[name].max()
            is_add = random.random() >= 0.5
            value = random_appended_dataframe[name].values
            random_appended_dataframe[name] += random.uniform(
                0,
                (max_arg - value) if is_add else (value - min_arg)
            ) * (1 if is_add else -1)
            assert min_arg <= random_appended_dataframe[name].values <= max_arg, name

        random_appended_dataframe = random_appended_dataframe.astype(dataframe.dtypes.to_dict())

        dataframe_all = concat([dataframe_all, random_appended_dataframe]).reset_index(drop=True)

    if shuffle:
        dataframe_all = dataframe_all.sample(frac=1)
    dataframe_all.to_csv(filename, index=False)
    return dataframe_all


def create_regression_model(dataframe: DataFrame, columns: [str, str]) -> LinearRegression:
    x = dataframe[columns[0]].to_numpy().reshape((-1, 1))
    y = dataframe[columns[1]].to_numpy()

    model = LinearRegression()
    model.fit(x, y)

    return model


def create_regression_data(dataframe: DataFrame,
                           columns: list[str, str],
                           percents: list[float, float] | tuple[float, float] = (0.99, 0.1),
                           shuffle: bool = False,
                           normalize_data: bool = False,
                           test_on_all_dataframe: bool = False) -> DataFrame | None:
    if sum(percents) != 1:
        raise Exception()
    dataframe = dataframe[columns]
    if shuffle:
        dataframe = dataframe.sample(frac=1)
    if normalize_data:
        df_nr = preprocessing.normalize(dataframe, axis=0)
        dataframe = DataFrame(df_nr, columns=dataframe.columns.values)
    rows = dataframe.shape[0]
    df99p = dataframe.iloc[0:math.ceil(rows * percents[0])]
    df1p = dataframe.iloc[math.ceil(rows * percents[0]):rows]

    model = create_regression_model(df99p, columns)

    if test_on_all_dataframe:
        y_pred = model.predict(dataframe[columns[0]].to_numpy().reshape((-1, 1)))
        return DataFrame({
            f"{columns[0]}": dataframe[columns[0]],
            f"Original {columns[1]}": dataframe[columns[1]],
            f"Predicted {columns[1]}": y_pred,
            "Difference": map(lambda x: x[0] / x[1] - 1, zip(dataframe[columns[1]], y_pred))
        }).reset_index(drop=True)

    y_pred = model.predict(df1p[columns[0]].to_numpy().reshape((-1, 1)))
    return DataFrame({
        f"{columns[0]}": df1p[columns[0]],
        f"Original {columns[1]}": df1p[columns[1]],
        f"Predicted {columns[1]}": y_pred,
        "Difference": map(lambda x: x[0] / x[1] - 1, zip(df1p[columns[1]], y_pred))
    }).reset_index(drop=True)


def statistic_dataframe(dataframe: DataFrame, column: str) -> DataFrame:
    return dataframe[column].describe().to_frame().transpose()


def get_plot_from_dataset(dataframe: DataFrame, x: str, y: [str, str], filename: str = 'static/plot.png'):
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
    df_pred = dataframe.sort_values(by=x)
    df_pred.plot(
        kind='line',
        x=x,
        y=y
    )
    plt.savefig(filename, edgecolor='White', transparent=True)
