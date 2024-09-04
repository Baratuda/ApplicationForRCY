from models import COU,NotCombatVinicles
import time



romanNumbers = {0:'I',1:'II', 2:'III', 3:'IV', 4:'V', 5:'VI', 6:'VII', 7:'VII', 8:'VIII', 9:'IX', 10:'X'}
rictangles = {
    '45':[1,30,5,3,29,36,21,14,15],
    '67':[5,15,36,29],
    '34':[21,14,30,5],
}   

colors = {'дежурство' : '#76d43e',
'другие загорания' : '#fdf401',
'занятия': '#ff7601',
'ликвидация жалоносных' : '#bf51c4',
'ложный' : '#07f583',
'платные услуги' : '#8bfe47',
'пожар' : '#fe2400',
'помощь населению' : '#01ffe7'}

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
        if time_of_liquidation != None:
            is_mistake, level_of_mistake, count_of_minutes = time_calculator(time_of_liquidation,120,60)    
        elif departure_time !=None:
            is_mistake, level_of_mistake, count_of_minutes = time_calculator(departure_time,180,120)
        elif arivall_time != None:
            is_mistake, level_of_mistake, count_of_minutes = time_calculator(arivall_time,180,120)
        if colors.get(purpose_of_departure):
            listNotСombatVehicles[j.car_id] = [colors[purpose_of_departure], purpose_of_departure, is_mistake, level_of_mistake, count_of_minutes]
        else:
            listNotСombatVehicles[j.car_id] = ['#ffffff', purpose_of_departure, is_mistake, level_of_mistake, count_of_minutes]  
    return listNotСombatVehicles

  

def test(list1, list2=None):
    truks = {}
    if list2:
        result = { i:{} for i in list2}   
    else:    
        result = { i.fireDepartment_id:{} for i in list1}
    for i in list1:
        if i.main_truk_id:
            if truks.get(i.main_truk_id):
                truks[i.main_truk_id].append(i)
                continue
            else:
                truks[i.main_truk_id] = [i]
                continue
        if not truks.get(i.licensePlate):
            truks[i.licensePlate] = [i]
            continue   
        else:
            truks[i.licensePlate].append(i)
            continue  
    for i in list1:
        x = 0
        if result[i.fireDepartment_id].get('Ремонт') and result[i.fireDepartment_id].get('Резерв'): x=2
        elif result[i.fireDepartment_id].get('Ремонт'): x=1
        elif result[i.fireDepartment_id].get('Резерв'): x=1
        number = len(result[i.fireDepartment_id])-x 
        if truks.get(i.licensePlate):
            if truks[i.licensePlate][0].status == 'COM':
                result[i.fireDepartment_id][romanNumbers[number]] = truks[i.licensePlate]
                continue
            elif truks[i.licensePlate][0].status == 'REP':
                result[i.fireDepartment_id]['Ремонт'] = truks[i.licensePlate] 
                continue
            else:
                result[i.fireDepartment_id]['Резерв'] = truks[i.licensePlate]
                continue 

    return result
           


def get_firetruks(list, list2=None):
    result = {}
    if list2: 
        truks = test(list2)
        for fireTruk, district in list:
            if result.get(district.districtDepartmentName):
                result[district.districtDepartmentName][fireTruk.fireDepartment_id] = truks[fireTruk.fireDepartment_id]
            else:
                result[district.districtDepartmentName]={fireTruk.fireDepartment_id : truks[fireTruk.fireDepartment_id]}    
    else:  
        for fireTruk, district in list:
            if result.get(district.districtDepartmentName):
                result[district.districtDepartmentName][fireTruk.fireDepartment_id] = [fireTruk,]
            else:
                result[district.districtDepartmentName]={fireTruk.fireDepartment_id : [fireTruk,]}                
    return result 