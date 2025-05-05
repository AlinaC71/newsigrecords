from flask import (
    Blueprint, render_template, json, jsonify, request, redirect, url_for
)

from collections import defaultdict
# from werkzeug.exceptions import abort
from sr.models import db, Record
from sqlalchemy import delete

# from sr.auth import login_required


rec_con = Blueprint('rec_con', __name__, url_prefix='/reccontrol', template_folder='templates/reccontrol')


@rec_con.route('/')
def reccon_welcome():
    return render_template("reccon_welcome.html")


@rec_con.route('/record_search')
def record_search():

    records = db.session.execute(db.select(Record)).scalars().all()    
    records_json = [r.record_to_dict() for r in records]
    

    fields = ["control_area", "installation", "location", "drawing_no", "title", "record_centre_name", "status", "return_no", "request_no"]    
    header=fields
    
    filter_option = {field : db.session.execute
                        (db.select(getattr(Record,field)).distinct())
                        .scalars()
                        .all() for field in fields}    
        

    return render_template('record_search.html',  header = header, records_json = records_json, filter_option = filter_option )

    
       

@rec_con.route('/record_insert', methods=('GET', 'POST'))
def record_insert():

    fields = ["control_area", "installation", "location", "drawing_no",
                "title", "record_centre_name", "status", "return_no", "request_no"
            ]
    header=fields
    # records = db.session.execute(db.select(Record)).scalars().all()
    # records_json = [r.record_to_dict() for r in records ]
    # print(records_json)

    if request.method == 'POST':
        formdata = request.form
        # print("FORMDATA:", request.form)
        records_to_insert = []

        
        # Determine how many “rows” were submitted by looking at the first field
        num_rows = len(formdata.getlist(fields[0]))
        
        # Build Record instances dynamically        
        for i in range(num_rows):
            record_kwargs = {}
            for field in fields:                
                value = formdata.getlist(field)[i] 
                record_kwargs[field] = value                  
                if field in ['request_no', 'return_no']:
                    record_kwargs[field] = value.strip() if value.strip() else None 
                
            records_to_insert.append(Record(**record_kwargs))           


        # Bulk-insert and commit
        db.session.add_all(records_to_insert)
        db.session.commit()
        


    #     if records_to_insert:
    #         record_dict = records_to_insert[0].record_to_dict()
    #         header = record_dict.keys()


    return render_template('record_insert.html', header=header)

    




@rec_con.route('/record_delete', methods=('GET', 'POST'))
def record_delete():
    records = db.session.execute(db.select(Record)).scalars().all()  # Fetch full Record objects
    records_json = [r.record_to_dict() for r in records]
    
    
    fields = ["control_area", "installation", "location", "drawing_no", "title", "record_centre_name", "status", "return_no", "request_no"]
    header = fields
   
    filter_option = {field : db.session.execute
                        (db.select(getattr(Record,field)).distinct())
                        .scalars()
                        .all() for field in fields}
    
    

    if request.method == 'POST':
        deleted_ids_json = request.form.get("deleted_ids")
        print(deleted_ids_json)
        if deleted_ids_json:
            deleted_ids = json.loads(deleted_ids_json)
            print("Deleting records with IDs:", deleted_ids)

            db.session.execute(delete(Record).where(Record.record_id.in_(deleted_ids)))
            db.session.commit()

            # Optional: reload records after deletion
            records = db.session.execute(db.select(Record)).scalars().all()
            records_json = [r.record_to_dict() for r in records]

    return render_template('record_delete.html', header=header, records_json=records_json, filter_option=filter_option)
   

    

@rec_con.route('/record_update', methods=('GET', 'POST'))
def record_update():


    records = db.session.execute(db.select(Record)).scalars().all()  # Fetch full Record objects
    records_json = [r.record_to_dict() for r in records]
    
    
    fields = ["control_area", "installation", "location", "drawing_no", "title", "record_centre_name", "status", "return_no", "request_no"]
    header = fields
    
    filter_option = {field : db.session.execute
                        (db.select(getattr(Record,field)).distinct())
                        .scalars()
                        .all() for field in fields}


    if request.method == 'POST':
        updated_ids = request.form.getlist('record_ids')
        updated_fields = request.form.getlist('fieldname[]')

        print("Updated IDs:", updated_ids)
        print("Updated field values:", updated_fields)

        # Validate count
        if len(updated_fields) != len(updated_ids) * len(fields):
            return "Mismatch in form data", 400

        # Process each record
        for i, record_id in enumerate(updated_ids):
            record = db.session.get(Record, int(record_id))
            if not record:
                continue  # Skip if not found

            offset = i * len(fields)
            for j, field in enumerate(fields):
                value = updated_fields[offset + j]
                if value == 'None':
                    value = None
                setattr(record, field, value)

        db.session.commit()
        return redirect(url_for('rec_con.record_update'))



       
    
    
    return render_template('record_update.html', header=header, records_json=records_json, filter_option = filter_option)










@rec_con.route('request_search')
def request_search():
    return 'Welcome to requestsh'


    

@rec_con.route('return_search')
def return_search():
    return 'Welcome to returnsh'















    
    






