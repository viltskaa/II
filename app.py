from flask import Flask, render_template, request, redirect
import pandas as pd

app = Flask(__name__)
csv_filename = 'diabetes.csv'

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
    row_start, row_end, column_start, column_end = map(int, [x[1] for x in request.args.items()])
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
                .to_html(classes='table border-0', index=False, justify='left')
    )


if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True, host='0.0.0.0')
