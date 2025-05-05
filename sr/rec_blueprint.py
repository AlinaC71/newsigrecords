from flask import (
    Blueprint, render_template
)

#, request, url_for
from werkzeug.exceptions import abort

# from sr.auth import login_required
# from sr.db import execute_query

rbp = Blueprint('rec_blueprint', __name__)

@rbp.route('/')#, methods=['GET', 'POST']
def index():
    return render_template("index.html")


# @bp.route('/records/')
# def records():
#     query = "SELECT status, control_area, installation, location, drawing_no, barcode, title, medium FROM records"
#     rows = execute_query(query)
#     return render_template("records.html", rows = rows)