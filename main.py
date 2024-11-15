import os
from flask_debugtoolbar import DebugToolbarExtension 
from config import engine
from sqlalchemy import  and_
from models import FireTruks, LocalityTowns, Sectors
from flask import Flask, request, render_template
from sqlalchemy.orm import scoped_session, sessionmaker, contains_eager 
from filters.my_custom_filters import  noCombatTruksmarker,carNamer
from helpMethods import fireTrukGetter, get_rictangles, getNotСombatVehicles
from flask_caching import Cache


db_session = scoped_session(sessionmaker(bind=engine))
app = Flask(__name__) 
app.config.from_pyfile('config.py')
cache = Cache(app)
app.add_template_filter(noCombatTruksmarker)
app.add_template_filter(carNamer)
toolbar = DebugToolbarExtension(app)

@cache.memoize(60 * 60)
def all_firetruks_getter(all_fire_department):
    return db_session.query(FireTruks).filter(and_(FireTruks.fireDepartment_id.in_(all_fire_department),FireTruks.status == 'COM')).all()

@app.route("/")
def getter():
    return render_template('main.html')

@app.route("/<int:num>/", methods=['GET','POST'])
def all(num):
    if request.method == 'POST':
        query = request.form['query']
    else:
        query = request.args.get('query')    
    not_combat = getNotСombatVehicles(db_session)
    x = ''
    x2 = ''
    for i in query:
        if i.isdigit():
            x+=i
        else:
            x2 += i    
    x = int(x)
    res = db_session.query(Sectors, LocalityTowns, Sectors.name)\
                    .filter(and_(Sectors.locality_id==27137,LocalityTowns.street == x2,LocalityTowns.numberHouseTo<=x,LocalityTowns.umberHouseDo>=x))\
                    .join(Sectors, LocalityTowns.sector_id==Sectors.sectorID)\
                    .with_entities(Sectors.name)\
                    .scalar()
    all_fire_department = get_rictangles(str(res))
    results=fireTrukGetter(all_firetruks_getter(all_fire_department), all_fire_department,not_combat)
    return render_template('rictangle.html', results=results, 
                                             notСombatVehicles=not_combat,
                                             query=query,
                                             num = num
                                            ) 

if __name__ == '__main__':
    app.run()


