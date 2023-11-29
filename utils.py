from pandas import DataFrame, cut, concat
import random


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
