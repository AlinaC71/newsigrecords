from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # Initialize SQLAlchemy

# Define the models
class Record(db.Model):
    __tablename__ = 'records'
    
    record_id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(80), nullable=False )
    control_area = db.Column(db.String(80), nullable=False)
    installation = db.Column(db.String(80), nullable=False)
    location = db.Column(db.String(80), nullable=False)
    drawing_no = db.Column(db.String(80), nullable=False)
    title = db.Column(db.String(80), nullable=False)
    record_centre_name = db.Column(db.String(80), nullable=False)    
    return_no = db.Column(db.String(80), db.ForeignKey('returns.return_no'), nullable=True)  # Foreign Key
    request_no = db.Column(db.String(80), db.ForeignKey('requests.request_no'), nullable=True)  # Foreign Key

    rtrn = db.relationship('Return', back_populates='record')
    rqst = db.relationship('Request', back_populates='record')
    


    def record_to_dict(self):

        return {
            "record_id" : self.record_id,          
            "control_area" : self.control_area,
            "installation" : self.installation, 
            "location" : self.location,
            "drawing_no" : self.drawing_no,
            "title" : self.title,
            "record_centre_name" : self.record_centre_name,
            "status" : self.status,
            "return_no" : self.return_no,
            "request_no" : self.request_no
        }


class Project(db.Model):
    __tablename__ = 'projects'
    
    project_name = db.Column(db.String(80), primary_key=True)
    stage = db.Column(db.String(6), nullable=False )
    control_area = db.Column(db.String(80), nullable=False)
    installation = db.Column(db.String(80), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)



class RecordCentre(db.Model):
    __tablename__ = 'record_centres'
    
    rec_cen_name = db.Column(db.String(80), primary_key=True,nullable=False)
    rec_cen_email = db.Column(db.String(80))
    rec_cen_cont_name = db.Column(db.String(80))
    record_centre_tech_name = db.Column(db.String(80))



class Request(db.Model):
    __tablename__ = 'requests'
    
    request_no = db.Column(db.String(80), primary_key=True)    
    request_date = db.Column(db.Date, nullable=False)
    request_status = db.Column(db.String(6), nullable=False )
    
    record = db.relationship('Record', back_populates='rqst')


class Return(db.Model):
    __tablename__ = 'returns'

    return_no = db.Column(db.String(80), primary_key=True)    
    return_date = db.Column(db.Date, nullable=False)
    return_status = db.Column(db.String(6), nullable=False )
    return_corr  = db.Column(db.String(6), nullable=False )
    return_test  = db.Column(db.String(6), nullable=False )
    return_ab  = db.Column(db.String(6), nullable=False )
    return_air = db.Column(db.String(6), nullable=False )
    return_ack = db.Column(db.String(6), nullable=False )
    
    record = db.relationship('Record', back_populates='rtrn')









#create the associaton/junction tables
project_requests = db.Table(
    'project_requests',
    db.Column('project_name', db.String(80), db.ForeignKey('projects.project_name'), primary_key = True),
    db.Column('request_no', db.String(80), db.ForeignKey('requests.request_no'), primary_key = True)    
)


project_returns = db.Table(
    'project_returns',
    db.Column('project_name', db.String(80), db.ForeignKey('projects.project_name'), primary_key = True),
    db.Column('return_no', db.String(80), db.ForeignKey('returns.return_no'), primary_key = True)    
)











