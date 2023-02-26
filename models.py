from sqlalchemy import Column, Integer, String, Date, Float, Boolean, LargeBinary
#from sqlalchemy.dialects.postgresql import POINT
from datetime import date
from sqlalchemy.ext.declarative import declarative_base
#from geoalchemy2 import Geometry
#from sqlalchemy.types import Point
from sqlalchemy.orm import Query

class CustomQuery(Query):
    pass


Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(String, primary_key=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    

class User_Role(Base):
    __tablename__ = 'user_role'
    id = Column(String, primary_key=True)
    role = Column(String, primary_key=True)
  
class Student(Base):
    __tablename__ = 'student'
    admission_no = Column(String, primary_key=True)
    name = Column(String)
    program_id = Column(String)
    institute_id=Column(String)
    admission_type = Column(String)
    entry_sem = Column(String)
    exit_sem = Column(String)
    year_of_admission = Column(Integer)
    date_of_admission = Column(Date)
    advisor1_pen = Column(String)
    advisor2_pen = Column(String)
    status = Column(String)
    sgpa = Column(Float)
    disci_action = Column(String)
    entrance_name = Column(String)
    entrance_score = Column(Float)
    entrance_rank = Column(Integer)
    quota = Column(String)
    school1 = Column(String)
    reg_no1 = Column(String)
    board1 = Column(String)
    score1 = Column(Float)
    total1 = Column(Float)
    grade1 = Column(Float)
    percentage1 = Column(Float)
    nochance1 = Column(Integer)
    school2 = Column(String)
    reg_no2 = Column(String)
    board2 = Column(String)
    phys_score2 = Column(Float)
    che_score2 = Column(Float)
    math_score2 = Column(Float)
    score2 = Column(Float)
    total2 = Column(Float)
    grade2 = Column(Float)
    percentage2 = Column(Float)
    nochance2 = Column(Integer)
    ug_name = Column(String)
    ug_institute = Column(String)
    ug_university = Column(String)
    ug_score = Column(Float)
    total_ug_score = Column(Float)
    ug_cgpa = Column(Float)
    ug_percentage = Column(Float)
    pg_name = Column(String)
    pg_institute = Column(String)
    pg_university = Column(String)
    pg_score = Column(Float)
    total_pg_score = Column(Float)
    pg_cgpa = Column(Float)
    pg_percentage = Column(Float)
    gate = Column(Float)
    jrf = Column(Float)
    net = Column(Float)
    additional_quali = Column(String)
    name_last_studied = Column(String)
    dob = Column(Date)
    gender = Column(String)
    religion = Column(String)
    caste = Column(String)
    sc = Column(Boolean)
    st = Column(Boolean)
    obc = Column(Boolean)
    oec = Column(Boolean)
    muslim = Column(Boolean)
    ecs = Column(Boolean)
    ph = Column(Boolean)
    bpl = Column(Boolean)
    blood = Column(String)
    image = Column(LargeBinary)
    image_status = Column(String)
    address1 = Column(String)
    p_office1 = Column(String)
    district1 = Column(String)
    state1 = Column(String)
    pincode1 = Column(String)
    gps1 =  Column(String)
    address2 = Column(String)
    p_office2 = Column(String)
    district2 = Column(String)
    state2 = Column(String)
    pincode2 = Column(String)
    gps2 =  Column(String)
    email = Column(String)
    rit_email = Column(String)
    mobile_ph_no = Column(String)
    land_ph_no = Column(String)
    aadhar = Column(String)
    pan = Column(String)
    passport = Column(String)
    bank_ac = Column(String)
    bank_name = Column(String)
    bank_branch = Column(String)
    ifsc = Column(String)
    remarks = Column(String)

class Staffer(Base):
    __tablename__ = 'staffer'

    pen = Column(String, primary_key=True)
    staffer_name = Column(String)
    desig = Column(String)
    date_service_entry = Column(Date)
    date_present_position = Column(Date)
    date_joined = Column(Date)
    date_relieved = Column(Date)
    name_last_worked = Column(String)
    teaching_experience = Column(Integer)
    industrial_experience = Column(Integer)
    areas_of_interest = Column(String)
    research_and_develop = Column(String)
    status = Column(String)
    link1 = Column(String)
    link2 = Column(String)
    staffer_disci_action = Column(String)
    recruitment_exam_name = Column(String)
    recruitment_rank = Column(Float)
    staffer_quota = Column(String)
    staffer_ug_name = Column(String)
    staffer_ug_institute = Column(String)
    staffer_ug_university = Column(String)
    staffer_ug_score = Column(Float)
    staffer_pg_name = Column(String)
    staffer_pg_institute = Column(String)
    staffer_pg_university = Column(String)
    staffer_pg_score = Column(Float)
    staffer_phd_title = Column(String)
    staffer_phd_discipline = Column(String)
    staffer_phd_institute = Column(String)
    staffer_phd_university = Column(String)
    staffer_gate = Column(String)
    staffer_jrf = Column(String)
    staffer_net = Column(String)
    staffer_additional_quali = Column(String)
    staffer_dob = Column(Date)
    staffer_gender = Column(String)
    staffer_religion = Column(String)
    staffer_caste = Column(String)
    staffer_sc = Column(Boolean)
    staffer_st = Column(Boolean)
    staffer_obc = Column(Boolean)
    staffer_oec = Column(Boolean)
    staffer_muslim = Column(Boolean)
    staffer_lc = Column(Boolean)
    staffer_ecs = Column(Boolean)
    staffer_ph = Column(String)
    staffer_bpl = Column(String)
    staffer_blood = Column(String)
    staffer_image = Column(String)
    staffer_image_status = Column(String)
    staffer_address1 = Column(String)
    staffer_poffice1 = Column(String)
    staffer_district1 = Column(String)
    staffer_state1 = Column(String)
    staffer_pincode1 = Column(String)
    staffer_gps1 = Column(String)
    staffer_address2 = Column(String)
    staffer_poffice2 = Column(String)
    staffer_district2 = Column(String)
    staffer_state2 = Column(String)
    staffer_pincode2 = Column(String)
    staffer_gps2 = Column(String)
    staffer_mobile_phno = Column(String)
    staffer_land_phno = Column(String)
    staffer_email = Column(String)
    staffer_rite_mail = Column(String)
    staffer_aadhar = Column(String)
    staffer_pan = Column(String)
    staffer_passport = Column(String)
    staffer_bank_ac = Column(String)
    staffer_bank_name = Column(String)
    staffer_bank_branch = Column(String)
    staffer_ifsc = Column(String)
    staffer_remarks = Column(String)
