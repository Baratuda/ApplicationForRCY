import os
from collections import OrderedDict
from flask import Flask, request, render_template
from sqlalchemy.orm import scoped_session, sessionmaker
from config import engine
from filters.my_custom_filters import dificult_length_calculator, noCombatTruksmarker, sort_firedepartments, sort_firefighters, sort_number_of_firetrukset
from helpMethods import get_firetruks, getNotСombatVehicles, read_docx_table,  test
from models import DistrictDepartment, FireTruks, FireDepartment, FireFighters
from sqlalchemy import or_, and_
from docx import Document
import pandas as pd
import re


db_session = scoped_session(sessionmaker(bind=engine))
app = Flask(__name__) 
app.add_template_filter(dificult_length_calculator)
app.add_template_filter(sort_firedepartments)

app.add_template_filter(sort_number_of_firetrukset)
app.add_template_filter(noCombatTruksmarker)
app.add_template_filter(sort_firefighters)


def get_rictangles(i):
    df = pd.read_csv("rictangles.csv")
    df = df.loc[df['№ сектора'] == int(i)]
    my_list = [i for i in re.split(r'-\d',df.loc[df.index[0],'0']) if i!='']
    return list(OrderedDict.fromkeys( my_list))

@app.route("/downloader", methods=['GET','POST'])
def downloader():
    if request.method == 'GET':
        return render_template('downloader.html')
    else:
        file = request.files['file']
        document = Document(os.path.realpath(file.filename))
        df = read_docx_table(document)
        num_of_sector = df['№ сектора']
        num = df[['Выезжают ПАСЧ по номерам вызова','Резерв']].agg("".join, axis=1)
        det = pd.concat([num_of_sector, num], join = 'outer', axis = 1)
        for i, v in det.iterrows():
            det.loc[i] = [v['№ сектора'].replace('№','').replace('.',''), v[0].replace("\n","").replace(" ","")]
        det.to_csv('rictangles.csv', index=False)
        return render_template('downloader.html')

@app.route("/", methods=['GET','POST'])
def all():
    licensePlate = request.args.get('licensePlate')
    ric = request.args.get('rictangle')
    type = request.args.get('type')
    main_fireDepartment = [i[0] for i in db_session.query(FireDepartment.fireDepartmentNumber).filter(FireDepartment.isMain == True).all()]
    if request.method == 'POST':   
        query = request.form['query']
        all_fire_department = get_rictangles(query)
        if  all_fire_department:
            all_firetruks = db_session.query(FireTruks).filter(and_(FireTruks.fireDepartment_id.in_(all_fire_department),FireTruks.status == 'COM')).all()
            return render_template('rictangle.html', results=test(all_firetruks, all_fire_department), rictangle = query, notСombatVehicles=getNotСombatVehicles(db_session) , main_fireDepartment=main_fireDepartment)
        if query.lower() == 'ответсвенные' or query.lower() == 'отв':
            all_responsibles = db_session.query(FireFighters, DistrictDepartment)\
                          .filter(FireFighters.post.startswith("ответ"))\
                          .join(FireDepartment, FireFighters.fireDepartment_id==FireDepartment.fireDepartmentNumber)\
                          .join(DistrictDepartment, FireDepartment.districtDepartment_id==DistrictDepartment.id)\
                          .order_by(FireDepartment.isMain)\
                          .all()
            return render_template('responsebles.html', results=get_firetruks( all_responsibles), main_fireDepartment=main_fireDepartment)
        if query.lower() == 'штаб':
            headquarters = db_session.query(FireTruks)\
                          .filter(FireTruks.fireDepartment_id=='0').all()
            return render_template('headquarters.html', results=headquarters)
        if query.lower() == 'цоу':
            all = db_session.query(FireFighters).filter(FireFighters.fireDepartment_id=='0').order_by(FireFighters.isOfficer.desc()).all()
            headquarters = []
            cou = []
            main_person = ''
            main_assistant = '' 
            main_headquarter = ''
            for i in all:
                if i.post.startswith("Диспетчер"): cou.append(i)
                elif i.post.startswith("Главный"): main_person=i
                elif i.post.startswith("Помощник"): main_assistant=i    
                elif i.post.startswith("Заместитель"): main_headquarter=i   
                else: headquarters.append(i)
            cou.insert(0,main_assistant)    
            cou.insert(0,main_person)
            headquarters.insert(0,main_headquarter)
            return render_template('cou.html', results=cou, results2=headquarters)
        if query.lower() == 'диспетчера'or query.lower() == 'дис':
            all_dispatchers = db_session.query(FireFighters, DistrictDepartment)\
                          .filter(or_(FireFighters.post == "радиотелефонист", FireFighters.post=="Диспетчер"))\
                          .join(FireDepartment, FireFighters.fireDepartment_id==FireDepartment.fireDepartmentNumber)\
                          .join(DistrictDepartment, FireDepartment.districtDepartment_id==DistrictDepartment.id)\
                          .order_by(FireDepartment.isMain)\
                          .all()
            return render_template('dispatchers.html', results=get_firetruks(all_dispatchers), main_fireDepartment=main_fireDepartment)
        if query.lower() == 'ндс':
            all_nds = db_session.query(FireFighters, DistrictDepartment)\
                          .filter(FireFighters.post == "Нач. дежурной смены")\
                          .join(FireDepartment, FireFighters.fireDepartment_id==FireDepartment.fireDepartmentNumber)\
                          .join(DistrictDepartment, FireDepartment.districtDepartment_id==DistrictDepartment.id)\
                          .order_by(FireDepartment.isMain)\
                          .all()
            return render_template('nds.html', results=get_firetruks(all_nds), main_fireDepartment=main_fireDepartment)
        if query.lower() == 'ремонт'or query.lower() == 'рем':
            all_repaered_firetruks = db_session.query(FireTruks, DistrictDepartment)\
                          .filter(FireTruks.status == "REP")\
                          .join(FireDepartment, FireTruks.fireDepartment_id==FireDepartment.fireDepartmentNumber)\
                          .join(DistrictDepartment, FireDepartment.districtDepartment_id==DistrictDepartment.id)\
                          .order_by(FireDepartment.isMain)\
                          .all()
            return render_template('repair.html', results=get_firetruks(all_repaered_firetruks), main_fireDepartment=main_fireDepartment)
        if query.lower() == 'резерв' or query.lower() == 'рез':
            all_reserved_firetruks = db_session.query(FireTruks, DistrictDepartment)\
                          .filter(FireTruks.status == "RES")\
                          .join(FireDepartment, FireTruks.fireDepartment_id==FireDepartment.fireDepartmentNumber)\
                          .join(DistrictDepartment, FireDepartment.districtDepartment_id==DistrictDepartment.id)\
                          .order_by(FireDepartment.isMain)\
                          .all()
            return render_template('reserve.html', results=get_firetruks(all_reserved_firetruks), main_fireDepartment=main_fireDepartment) 
    if licensePlate:
        firefighters = db_session.query(FireFighters).filter(FireFighters.fireTruk_id==licensePlate).order_by(FireFighters.post).all()
        if not firefighters:
           licensePlate = db_session.query(FireTruks.main_truk_id).filter(FireTruks.licensePlate == licensePlate)
           firefighters = db_session.query(FireFighters).filter(FireFighters.fireTruk_id==licensePlate).order_by(FireFighters.post).all()
        if ric:
            all_fire_department = rictangles[ric]
            all_firetruks = db_session.query(FireTruks).filter(and_(FireTruks.fireDepartment_id.in_(all_fire_department),FireTruks.status == 'COM')).all()
            return render_template('rictangle.html', results=test(all_firetruks, all_fire_department), rictangle=ric, firefighters=firefighters, notСombatVehicles=getNotСombatVehicles(db_session), main_fireDepartment=main_fireDepartment)    
        elif type:
            fireTruks = db_session.query(FireTruks).filter(FireTruks.fireDepartment_id=='0').all()
            return render_template('headquarters.html', results=fireTruks, firefighters=firefighters)
        else:
            all_fireTruks = db_session.query(FireTruks).all()
            all = db_session.query(FireTruks, DistrictDepartment)\
                          .join(FireDepartment, FireTruks.fireDepartment_id==FireDepartment.fireDepartmentNumber)\
                          .join(DistrictDepartment, FireDepartment.districtDepartment_id==DistrictDepartment.id)\
                          .order_by(FireDepartment.isMain)\
                          .all()  
            return render_template('all.html', results=get_firetruks(all, all_fireTruks), firefighters=firefighters, main_fireDepartment=main_fireDepartment)

    if request.method == 'GET' or query=='' or query.lower() == 'все':
        all_fireTruks = db_session.query(FireTruks).all()
        all = db_session.query(FireTruks, DistrictDepartment)\
                          .join(FireDepartment, FireTruks.fireDepartment_id==FireDepartment.fireDepartmentNumber)\
                          .join(DistrictDepartment, FireDepartment.districtDepartment_id==DistrictDepartment.id)\
                          .order_by(FireDepartment.isMain)\
                          .all()
        return render_template('all.html', results = get_firetruks(all, all_fireTruks), main_fireDepartment=main_fireDepartment)     
    else:
        return render_template('main.html')






if __name__ == '__main__':
    app.run()


