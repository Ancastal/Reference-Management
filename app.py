from flask import Flask, request, render_template, redirect, url_for, flash, get_flashed_messages
from pybibtex import BibTeXFile, BibTeXEntry

DATABASE_FILE = 'references.bib'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
database = BibTeXFile(DATABASE_FILE)

@app.route('/')
def home():
    messages = get_flashed_messages(with_categories=True)
    return render_template('home.html', messages=messages)

@app.route('/add', methods=['GET', 'POST'])
def add_reference():
    if request.method == 'POST':
        key = request.form.get('key')
        author = request.form.get('author')
        title = request.form.get('title')
        year = request.form.get('year')
        journal = request.form.get('journal')
        fields = {"author": author, "title": title, "year": year, "journal": journal}
        database.add_entry("article", key, fields)
        database.save()
        flash("Reference added successfully!", "success")
        return redirect(url_for('home'))
    return render_template('add_reference.html')

@app.route('/search', methods=['GET', 'POST'])
def search_reference():
    if request.method == 'POST':
        query = request.form.get('query')
        results = []
        for key, entry in database.entries.items():
            if 'author' in entry.fields and query.lower() in entry.fields['author'].lower():
                results.append(entry.generate_citation())
            elif 'title' in entry.fields and query.lower() in entry.fields['title'].lower():
                results.append(entry.generate_citation())
        if results:
            return render_template('search_results.html', results=results)
        else:
            return "No matching references found."
    return render_template('search_reference.html')

@app.route('/list_references', methods=['GET'])
def list_references():
    citations = [entry.generate_citation() for key, entry in database.entries.items()]

    return render_template('list_references.html',citations=citations)

@app.route('/filter_entries', methods=['GET', 'POST'])
def filter_entries():
    if request.method == 'POST':
        field = request.form.get('field')
        condition_str = request.form.get('condition')

        # Define a condition function
        def condition(value):
            # Check if the value can be converted to a float
            try:
                numeric_value = float(value)
                return eval(f"{numeric_value} {condition_str}")
            except ValueError:
                # It's a non-numeric value
                return eval(f"'{value}' {condition_str}")

        # Use the filter_entries function
        filtered_entries = database.filter_entries(field, condition)

        # Send the filtered entries to the template
        return render_template('filtered_entries.html', entries=filtered_entries)
    else:
        return render_template('filter_entries.html')



if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True, host='0.0.0.0')
