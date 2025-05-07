from flask import (
    Blueprint, render_template, json, flash, request, redirect, url_for
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

        num_rows = len(formdata.getlist(fields[0]))
        records_to_insert = []
        duplicate_count = 0
        incomplete_count = 0
        duplicates = []

        for i in range(num_rows):
            record_kwargs = {}
            row_is_valid = True

            for field in fields:
                value = formdata.getlist(field)[i].strip()

                if field in ['request_no', 'return_no']:
                    record_kwargs[field] = value if value else None
                else:
                    if not value:
                        row_is_valid = False
                    record_kwargs[field] = value

            if not row_is_valid:
                incomplete_count += 1
                continue  # Skip row if any required field is missing

            existing = db.session.execute(
                db.select(Record).filter_by(**record_kwargs)
            ).scalar()

            if existing:
                duplicates.append(record_kwargs)
                duplicate_count += 1
                continue  # Skip duplicate

            records_to_insert.append(Record(**record_kwargs))

        if records_to_insert:
            db.session.add_all(records_to_insert)
            db.session.commit()
            flash(f"{len(records_to_insert)} new record(s) inserted successfully.", "success")

        if duplicate_count > 0:
            flash(f"{duplicate_count} duplicate record(s) were skipped.", "warning")

        if incomplete_count > 0:
            flash(f"{incomplete_count} incomplete row(s) were skipped (required fields missing).", "warning")

        return render_template('record_insert.html', header=fields)

    




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

        duplicate_updates = 0
        updated_count = 0

        if len(updated_fields) != len(updated_ids) * len(fields):
            return "Mismatch in form data", 400

        for i, record_id in enumerate(updated_ids):
            record = db.session.get(Record, int(record_id))
            if not record:
                continue

            # Prepare proposed update
            offset = i * len(fields)
            new_data = {}
            for j, field in enumerate(fields):
                value = updated_fields[offset + j]
                value = None if value == 'None' else value
                new_data[field] = value

        # Check for duplicate with other records
            existing = db.session.execute(
                db.select(Record)
                .filter_by(**new_data)
                .filter(Record.record_id != record.record_id)
            ).scalar()

            if existing:
                duplicate_updates += 1
                continue  # Skip update due to duplication

        # Apply changes
            for field, value in new_data.items():
                setattr(record, field, value)
            updated_count += 1

        if updated_count > 0:
            db.session.commit()
            flash(f"{updated_count} record(s) updated successfully.", "success")

        if duplicate_updates > 0:
            flash(f"{duplicate_updates} record(s) were skipped due to duplication.", "warning")

        return redirect(url_for('rec_con.record_update'))
      
    
    
    return render_template('record_update.html', header=header, records_json=records_json, filter_option = filter_option)









@rec_con.route('request_search')
def request_search():
    return 'Welcome to requestsh'


    

@rec_con.route('return_search')
def return_search():
    return 'Welcome to returnsh'















    
    






