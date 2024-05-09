from db import execute_query
import mysql.connector


try:

    query = "UPDATE records SET status = TRIM(status), control_area = TRIM(control_area), installation = TRIM(installation), location  = TRIM(location), drawing_no = TRIM(drawing_no), old_version = TRIM(old_version), new_version = TRIM(new_version), barcode = TRIM(barcode), title = TRIM(title), cad_file_name = TRIM(cad_file_name), medium = TRIM(medium), size = TRIM(size), in_production = TRIM(in_production), return_ready = TRIM(return_ready), return_no = TRIM(return_no), request_no = TRIM(request_no), record_centre_name = TRIM(record_centre_name), drawing_type_code= TRIM(drawing_type_code);"

    e_query = execute_query(query)


except mysql.connector.Error as error:
    print("Something went wrong: {}".format(error))