from flask import render_template, request
from .db import execute_query
from .app import app


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html")

@app.route('/records/')
def records():
    query = "SELECT status, control_area, installation, location, drawing_no, barcode, title, medium FROM records"
    rows = execute_query(query)
    return render_template("records.html", rows = rows)

@app.route('/projects/')
def projects():
    query = "SELECT project_id, project_name, stage FROM project"
    rows = execute_query(query)
    return render_template("projects.html", rows = rows)


@app.route('/update_records/', methods=["GET", "POST"])
def update_records():
    
    if request.method == "POST":
        print("Form Data:", request.form)
        status = request.form.get('status')
        control_area = request.form.get('control_area')
        installation = request.form.get('installation')
        location = request.form.get('location')
        drawing_no = request.form.get('drawing_no')
        barcode = request.form.get('barcode')
        title = request.form.get('title')
        medium = request.form.get('medium')

        print("Status:", status)
        if installation is None or installation.strip() =="":
            return("Error. Status field cannot be empty")
        if location is None or location.strip() =="":
            return("Error. Location field cannot be empty")
        if status is None or status.strip() =="":
            return("Error. Status field cannot be empty")
        
    
        query = "INSERT INTO records (status, control_area, installation, location, drawing_no, old_version, new_version,     barcode, title, cad_file_name, medium, size, in_production, return_ready, return_no, request_no, record_centre_name, drawing_type_code) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (status, control_area, installation, location, drawing_no, None, None, barcode, title,  None,  medium,  None,  None,  None,  None,  None,  None,  None)
        
        rows = execute_query(query, values)
        return "Record updated successfully"
    
    elif request.method == "GET":
        return render_template("update_record.html")


@app.route('/search_records/', methods=["GET", "POST"])
def search_records():
    if request.method == "POST":
        # control_area = request.form.get('control_area')
        # installation = request.form.get('installation')
        # location = request.form.get('location')
        # drawing_no = request.form.get('drawing_no')
        # barcode = request.form.get('barcode')
        # title = request.form.get('title')


        control_area, installation, location, drawing_no, barcode, title = \
            (request.form.get(field) for field in ['control_area', 'installation', 'location', 'drawing_no', 'barcode', 'title'])



        query = "SELECT * FROM records WHERE 1=1 "


        condition_values = [control_area, installation, location, drawing_no, barcode, title] 

        conditions_string = ["control_area", "installation", "location", "drawing_no","barcode", "title"] 

        condition_parameters = []
        
        conditions_query = ""   

        for value, string in zip(condition_values, conditions_string):
            if value:
                conditions_query += " AND " + f"{string} = %s"               
                condition_parameters.append(value)

        if conditions_query:
                query += conditions_query    

        parameters = tuple(condition_parameters)         
        
        print(query)
        print(parameters)

        rows = execute_query(query, parameters)
        return render_template("display_srchd_record.html", rows = rows[1:])
    



    elif request.method == "GET":
        return render_template("search_record.html")
    

      
        # status, control_area, installation, location, drawing_no, old_version, new_version, barcode, title, cad_file_name, medium, size, in_production, return_ready, return_no, request_no, record_centre_name, drawing_type_code =                    (request.form.get(field) for field in ['status', 'control_area', 'installation', 'location', 'drawing_no', 'old_version', 'new_version', 'barcode', 'title', 'cad_file_name', 'medium', 'size', 'in_production', 'return_ready', 'return_no', 'request_no', 'record_centre_name', 'drawing_type_code'])
        
      


# query = "INSERT INTO records (status, control_area, installation, location, drawing_no, old_version, new_version, barcode, title, cad_file_name, medium, size, in_production, return_ready, return_no, request_no, record_centre_name, drawing_type_code)  FROM records"


@app.route('/request_records/')
def request_records():
    return render_template("search_record_html")

@app.route('/return_records/', methods=["GET", "POST"])
def return_records():
    return render_template("search_record_html")