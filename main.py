from flask import Flask, request, render_template
from sqlalchemy.orm import scoped_session, sessionmaker
from config import engine
from filters.my_custom_filters import dificult_length_calculator, noCombatTruksmarker, sort_firedepartments, sort_firefighters, sort_number_of_firetrukset
from helpMethods import get_rictangles, getNotСombatVehicles,                                  test
from models import FireTruks, FireDepartment
from sqlalchemy import  and_

db_session = scoped_session(sessionmaker(bind=engine))
app = Flask(__name__) 
app.add_template_filter(dificult_length_calculator)
app.add_template_filter(sort_firedepartments)
app.add_template_filter(sort_number_of_firetrukset)
app.add_template_filter(noCombatTruksmarker)
app.add_template_filter(sort_firefighters)

@app.route("/", methods=['GET','POST'])
def all():
    main_fireDepartment = [i[0] for i in db_session.query(FireDepartment.fireDepartmentNumber).filter(FireDepartment.isMain == True).all()]
    if request.method == 'POST':   
        query = request.form['query']
        all_fire_department = get_rictangles(query)
        if  all_fire_department:
            all_firetruks = db_session.query(FireTruks).filter(and_(FireTruks.fireDepartment_id.in_(all_fire_department),FireTruks.status == 'COM')).all()
            return render_template('rictangle.html', results=test(all_firetruks, all_fire_department), rictangle = query, notСombatVehicles=getNotСombatVehicles(db_session) , main_fireDepartment=main_fireDepartment)
    else:
        return render_template('main.html')


if __name__ == '__main__':
    app.run()


