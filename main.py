from flask import Flask, request, render_template
from sqlalchemy.orm import scoped_session, sessionmaker
from config import engine
from filters.my_custom_filters import dificult_length_calculator, noCombatTruksmarker, sort_firedepartments, sort_number_of_firetrukset
from helpMethods import get_firetruks, getNotСombatVehicles, rictangles, test
from models import DistrictDepartment, FireTruks, FireDepartment, FireFighters
from sqlalchemy import or_, and_

db_session = scoped_session(sessionmaker(bind=engine))

app = Flask(__name__) 
app.add_template_filter(dificult_length_calculator)
app.add_template_filter(sort_firedepartments)
app.add_template_filter(sort_number_of_firetrukset)
app.add_template_filter(noCombatTruksmarker)

@app.route("/", methods=['GET','POST'])
def all():
    licensePlate = request.args.get('licensePlate')
    ric = request.args.get('rictangle')
    main_fireDepartment = [i[0] for i in db_session.query(FireDepartment.fireDepartmentNumber).filter(FireDepartment.isMain == True).all()]
    if request.method == 'POST':   
        query = request.form['query']
        if str(query) in rictangles:
            all_fire_department = rictangles[query]
            all_firetruks = db_session.query(FireTruks).filter(and_(FireTruks.fireDepartment_id.in_(all_fire_department),FireTruks.status == 'COM')).all()
            return render_template('rictangle.html', results=test(all_firetruks, all_fire_department), rictangle = query, notСombatVehicles=getNotСombatVehicles() , main_fireDepartment=main_fireDepartment)
        if query.lower() == 'ответсвенные' or query.lower() == 'отв':
            all_responsibles = db_session.query(FireFighters, DistrictDepartment)\
                          .filter(FireFighters.post.startswith("ответ"))\
                          .join(FireDepartment, FireFighters.fireDepartment_id==FireDepartment.fireDepartmentNumber)\
                          .join(DistrictDepartment, FireDepartment.districtDepartment_id==DistrictDepartment.id)\
                          .order_by(FireDepartment.isMain)\
                          .all()
            return render_template('responsebles.html', results=get_firetruks( all_responsibles), main_fireDepartment=main_fireDepartment)
        if query.lower() == 'диспетчера'or query.lower() == 'дис':
            all_dispatchers = db_session.query(FireFighters, DistrictDepartment)\
                          .filter(or_(FireFighters.post == "радиотелефонист", FireFighters.post == "Диспетчер") )\
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
        firefighters = db_session.query(FireFighters).filter(FireFighters.fireTruk_id==licensePlate).all()
        if not firefighters:
           licensePlate = db_session.query(FireTruks.main_truk_id).filter(FireTruks.licensePlate == licensePlate)
           firefighters = db_session.query(FireFighters).filter(FireFighters.fireTruk_id==licensePlate).all()
        if ric:
            all_fire_department = rictangles[ric]
            all_firetruks = db_session.query(FireTruks).filter(and_(FireTruks.fireDepartment_id.in_(all_fire_department),FireTruks.status == 'COM')).all()
            return render_template('rictangle.html', results=test(all_firetruks, all_fire_department), rictangle=ric, firefighters=firefighters, notСombatVehicles=getNotСombatVehicles(), main_fireDepartment=main_fireDepartment)    
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
    

if __name__ == '__main__':
    app.run()


