from models import COU,NotCombatVinicles
import time
import pandas as pd

romanNumbers = {0:'I',1:'II', 2:'III', 3:'IV', 4:'V', 5:'VI', 6:'VII', 7:'VII', 8:'VIII', 9:'IX', 10:'X'}


colors = {'дежурство' : '#76d43e',
          'другие загорания' : '#fdf401',
          'занятия': '#ff7601',
          'ликвидация жалоносных' : '#bf51c4',
          'ложный' : '#07f583',
          'платные услуги' : '#8bfe47',
          'пожар' : '#fe2400',
          'помощь населению' : '#01ffe7'
        }

def read_docx_table(document):
    table = document.tables[0]
    data = [[cell.text for cell in row.cells] for row in table.rows]
    df = pd.DataFrame(data)
    outside_col, inside_col = df.iloc[0], df.iloc[1]
    hier_index = pd.MultiIndex.from_tuples(list(zip(outside_col, inside_col)))
    df = pd.DataFrame(data,columns=hier_index).drop(df.index[[0,1]] ).reset_index(drop=True)
    return df

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
        result = { str(i):{} for i in list2}   
    else:    
        result = { str(i.fireDepartment_id):{} for i in list1}    
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
        fireDepartment = str(i.fireDepartment_id)
        x = 0
        if result[fireDepartment].get('Ремонт') and result[fireDepartment].get('Резерв'): x=2
        elif result[fireDepartment].get('Ремонт'): x=1
        elif result[fireDepartment].get('Резерв'): x=1
        number = len(result[fireDepartment])-x 
        if truks.get(i.licensePlate):
            if truks[i.licensePlate][0].status == 'COM':
                result[fireDepartment][romanNumbers[number]] = truks[i.licensePlate]
                continue
            elif truks[i.licensePlate][0].status == 'REP':
                result[fireDepartment]['Ремонт'] = truks[i.licensePlate] 
                continue
            else:
                result[fireDepartment]['Резерв'] = truks[i.licensePlate]
                continue 

    new_result = {}            
    for i,j in result.items():            
        if j == {}:
             continue 
        else:
            new_result[i] = j      
    return new_result
           


def get_firetruks(list, list2=None):
    result = {}
    if list2: 
        truks = test(list2)
        for fireTruk, district in list:
            department_id = str(fireTruk.fireDepartment_id)
            if result.get(district.districtDepartmentName):
                result[district.districtDepartmentName][department_id] = truks[department_id]
            else:
                result[district.districtDepartmentName]={department_id : truks[department_id]}    
    else:  
        for fireTruk, district in list:
            department_id = str(fireTruk.fireDepartment_id)
            if result.get(district.districtDepartmentName):
                result[district.districtDepartmentName][department_id] = [fireTruk,]
            else:
                result[district.districtDepartmentName]={department_id : [fireTruk,]}  
                          
    return result 