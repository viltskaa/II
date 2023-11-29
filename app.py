from flask import Flask, render_template, request, redirect
from utils import data_analysis
from Structs import blume_filter
import pandas as pd

app = Flask(__name__)
csv_filename = 'datasets/diabetes.csv'
params_to_analysis = ["BloodPressure", "Insulin", "BMI", "Pregnancies"]

"""

Задание 1. Минимальное, среднее, максимальное АД по возрастным группам +
Задание 2. Минимальное, среднее, значение инсулина по возрастным группам + 
Задание 3. Минимальное, среднее, значение ИМТ по возрастным группам +
Задание 4. Минимальное, среднее,значение количества беременностей по возрастным группам

"""


@app.route('/')
def main_page():
    df = pd.read_csv(csv_filename)
    return render_template(
        "CsvView.html",
        column_info=[f"{_name}:{_type}" for _name, _type in df.dtypes.items()],
        rows_count=len(df),
        columns_count=len(df.columns),
        filled_cells=[f"{_name}:{_type}" for _name, _type in df.count().items()],
        empty_cells=[f"{_name}:{_type.sum()}" for _name, _type in df.isna().items()]
    )


@app.route('/view', methods=['GET'])
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


@app.route('/s', methods=['GET'])
def search_blume_get():
    return render_template('finder.html')


@app.route('/search', methods=['GET'])
def search_blume_post():
    arg = request.args['arg']

    if arg not in blume_filter:
        return render_template("NotFound.html")

    return redirect("/")


if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True, host='0.0.0.0')
