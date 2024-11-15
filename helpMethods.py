from models import COU,NotCombatVinicles
import time
import pandas as pd
import re

mainList = ['АЦ','АБР', 'АГДЗС', 'АСА']
romanNumbers = {0:'1',1:'2', 2:'3', 3:'4', 4:'5', 5:'6', 6:'7', 7:'8', 8:'9', 9:'10', 10:'11'}
colors = {'дежурство' : '#76d43e',
          'другие загорания' : '#fdf401',
          'занятия': '#ff7601',
          'ликвидация жалоносных' : '#bf51c4',
          'ложный' : '#07f583',
          'платные услуги' : '#8bfe47',
          'пожар' : '#fe2400',
          'помощь населению' : '#01ffe7'
        }

    
            

def get_rictangles(i):
    if not i.isalpha():
        df = pd.read_csv("rictangles.csv")
        df = df.loc[df['№ сектора'] == int(i)]
        my_list = [i for i in re.split(r'-\d',df.loc[df.index[0],'0']) if i!='']
        return  my_list
    else: return


def time_calculator(t, x,y):
    is_mistake  = False
    level_of_mistake = 0
    curent_time = time.localtime()
    count_of_minutes = (curent_time.tm_hour - t.hour)*60 + (curent_time.tm_min - t.minute)
    if count_of_minutes > x: 
            is_mistake = True
            level_of_mistake = 2
    elif  count_of_minutes > y:
            is_mistake = True
            level_of_mistake = 1
    minutes = count_of_minutes%60 
    hour = int(count_of_minutes/60)
    return  (is_mistake, level_of_mistake, (hour,minutes))       

def getNotСombatVehicles(session):
    notСombatVehicles = session.query(COU, NotCombatVinicles)\
                          .filter(COU.return_time.is_(None))\
                          .join(COU, NotCombatVinicles.cou_id==COU.id)\
                          .all()
    listNotСombatVehicles = {}
    for i,j in notСombatVehicles:
        purpose_of_departure = i.purpose_of_departure.lower()
        time_of_liquidation = i.time_of_liquidation
        arivall_time = i.arivall_time
        departure_time = i.departure_time
        department = ''
        if i.department_id:
            department = i.department_id
        if time_of_liquidation != None:
            is_mistake, level_of_mistake, count_of_minutes = time_calculator(time_of_liquidation,120,60)    
        elif departure_time !=None:
            is_mistake, level_of_mistake, count_of_minutes = time_calculator(departure_time,180,120)
        elif arivall_time != None:
            is_mistake, level_of_mistake, count_of_minutes = time_calculator(arivall_time,180,120)
        if colors.get(purpose_of_departure):
            listNotСombatVehicles[j.car_id] = [colors[purpose_of_departure], purpose_of_departure, is_mistake, level_of_mistake, count_of_minutes,department]
        else:
            listNotСombatVehicles[j.car_id] = ['#ffffff', purpose_of_departure, is_mistake, level_of_mistake, count_of_minutes,department]  
    return listNotСombatVehicles

def helper(licensePlate, truks,result, is_index=False):
    if truks.get(licensePlate):
        if is_index:
            truks[licensePlate].append(result) 
        else:
            truks[licensePlate].insert(0,result)   
    else:
        truks[licensePlate] = [result]
    return truks    

def redeployedCarFinder(not_combat):
    redeployedCarList = {}
    for i,j in not_combat.items():
        if j[1].lower() == 'передислокация':
            redeployedCarList[i] = j[5]
    return redeployedCarList        


def dict_maker(list_firedepartments):
    result= {}
    for i in list_firedepartments:
        if i in result:
            i = i + ' '
        result[i] = {} 
    return result            



def fireTrukGetter(all_firetruks, all_fire_department, not_combat):
    truks = {}
    main_truks = {}
    listRedeployedCars = {}
    is_index = False
    list_truks = []
    redeployedCars = redeployedCarFinder(not_combat)
    result = dict_maker(all_fire_department) 
    for i in all_firetruks:
        if i.main_truk_id: 
            licensePlate = i.main_truk_id
            if i.name == 'АЦ' or i.name == 'АБР': 
                list_truks.append(i.main_truk_id)
        else: 
            licensePlate = i.licensePlate
            is_index=True
    
        if i.name in mainList:
            if i.licensePlate in redeployedCars:
                helper(licensePlate,listRedeployedCars,i, is_index)
            helper(licensePlate,main_truks,i, is_index)
        else:
            if i.licensePlate in redeployedCars:
                helper(licensePlate,listRedeployedCars,i, is_index)
            helper(licensePlate,truks,i,is_index)

   
    for i,j in main_truks.items():
        fireDepartment = str(j[0].fireDepartment_id)
        length = len(result[fireDepartment])
        if result.get(fireDepartment+' ')=={} and len(result.get(fireDepartment))==1:
            result[fireDepartment+' '][romanNumbers[length]] = j    
        else:
            result[fireDepartment][romanNumbers[length]] = j   


        
    for i,j in truks.items():
        fireDepartment = str(j[0].fireDepartment_id)
        if result.get(fireDepartment+' '): 
            length = len(result[fireDepartment])+len(result[fireDepartment+' '])
        else:
            length = len(result[fireDepartment])
        result[fireDepartment][romanNumbers[length]] = j

    for i,j in listRedeployedCars.items():
         result[str(redeployedCars[j[0].licensePlate])]['Пер.'] = j    


        
            
    return { i:j for i,j in result.items() if j!={} }