from flask import Flask, render_template, request, redirect

import utils
from utils import data_analysis
from Structs import blume_filter
import pandas as pd

app = Flask(__name__)
csv_filename = 'datasets/diabetes.csv'
params_to_analysis = ["BloodPressure", "Insulin", "BMI", "Pregnancies"]


@app.route('/')
def main_page():
    return render_template("index.html")


@app.route('/csv')
def csv_page():
    df = pd.read_csv(csv_filename)
    return render_template(
        "CsvView.html",
        column_info=[f"{_name}:{_type}" for _name, _type in df.dtypes.items()],
        rows_count=len(df),
        columns_count=len(df.columns),
        filled_cells=[f"{_name}:{_type}" for _name, _type in df.count().items()],
        empty_cells=[f"{_name}:{_type.sum()}" for _name, _type in df.isna().items()]
    )


@app.route('/csv_view', methods=['GET'])
def view_page():
    data_analysis_check = request.args.get("data_analysis") == 'on'

    row_start, row_end, column_start, column_end, *_ = map(
        lambda x: int(x) if x != 'on' and x != 'off' else x, request.args.values()
    )

    if row_start >= row_end or column_start >= column_end:
        return redirect("/")

    df = pd.read_csv(csv_filename, skiprows=row_start, nrows=row_end, sep=',')

    return render_template(
        "CsvView.html",
        column_info=[f"{_name}:{_type}" for _name, _type in df.dtypes.items()],
        rows_count=len(df),
        columns_count=len(df.columns),
        filled_cells=[f"{_name}:{_type}" for _name, _type in df.count().items()],
        empty_cells=[f"{_name}:{_type.sum()}" for _name, _type in df.isna().items()],
        table=(df.iloc[row_start:row_end, column_start:column_end])
        .to_html(classes='table border-0', index=False, justify='left'),
        analysis=[
            data_analysis(df, x).to_html(classes='table border-0', index=False, justify='left') for x in
            params_to_analysis
        ] if data_analysis_check else None
    )


@app.route('/finder', methods=['GET'])
def search_blume_get():
    return render_template('finder.html')


@app.route('/finder_result', methods=['GET'])
def search_blume_post():
    arg = request.args['arg']

    if arg not in blume_filter:
        return render_template("NotFound.html")

    return redirect("/")


@app.route('/pair_regression', methods=['GET'])
def pair_regression_page():
    df = pd.read_csv(csv_filename, index_col=0, nrows=0)
    return render_template("Regression.html", columns=df.columns.values.tolist())


@app.route('/pair_regression_view', methods=['GET'])
def pair_regression_view():
    df = pd.read_csv(csv_filename)
    args = request.args

    column_name_1, column_name_2 = args.get("FirstPair"), args.get("SecondPair")
    if column_name_1 is None or column_name_2 is None:
        return redirect("/pair_regression")

    if column_name_1 == column_name_2:
        return redirect("/pair_regression")

    perc = int(args.get("RangePers")) / 100

    dataframe_regression_data = utils.create_regression_data(
        df,
        [args["FirstPair"], args["SecondPair"]],
        [perc, 1 - perc],
        shuffle="ShuffleCheck" in args,
        normalize_data="NormalizeCheck" in args,
        test_on_all_dataframe="TestDatasetCheck" in args
    )

    utils.get_plot_from_dataset(
        dataframe_regression_data,
        args["FirstPair"],
        [f"Original {args['SecondPair']}", f"Predicted {args['SecondPair']}"]
    )

    dataframe_stats_data = [
        utils.statistic_dataframe(dataframe_regression_data, f"Original {args['SecondPair']}").round(2),
        utils.statistic_dataframe(dataframe_regression_data, f"Predicted {args['SecondPair']}").round(2)
    ] if "StatsCheck" in args else None

    return render_template(
        "RegressionView.html",
        tags=[
            "Shuffled" if "ShuffleCheck" in args else None,
            "Normalized" if "NormalizeCheck" in args else None,
            "All Data Test" if "TestDatasetCheck" in args else None,
            f'{args["FirstPair"]} -> {args["SecondPair"]}'
        ],
        regression_data=dataframe_regression_data.to_html(
            classes='table border-0 table-dark',
            index=False,
            justify='left'),
        stats_before=dataframe_stats_data[0].to_html(
            classes='table border-0 table-dark',
            index=False,
            justify='left') if dataframe_stats_data is not None else None,
        stats_after=dataframe_stats_data[1].to_html(
            classes='table border-0 table-dark',
            index=False,
            justify='left') if dataframe_stats_data is not None else None
    )


if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True, host='0.0.0.0')
