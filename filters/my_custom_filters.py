
colors = {'#76d43e': ['#76d43e','#6cc439', '#63b434', '#579e2e','#50912a'],
          '#fdf401':['#fdf401', '#e7e003', '#d3cc03', '#bdb703', '#aaa401'], 
          '#ff7601':['#ff7601', '#e76e03',' #d16303', '#c45d03', '#b65602'],
          '#ffffff':['#ffffff', '#ebeaea', '#d4d4d4', '#c0c0c0', '#b1b1b1'],
          '#bf51c4':['#bf51c4','#ac4ab1', '#9d44a1', '#914096', '#7e3881'], 
          '#07f583':['#07f583','#08e279', '#07c96b', '#07b15f', '#089953'],
          '#8bfe47':['#8bfe47', '#79dd3f', '#6ac038', '#5fac32', '#53962c'],
          '#fe2400':['#fe2400', '#e72503', '#d82303', '#bd1f04', '#a11c04'],
          '#01ffe7':['#01ffe7', '#03e6cf', '#05cab7', '#04b9a7', '#06a091'],
          '#049b24': ['#049b24','#028d20','#04791d','#046e1b','#045c17']}

car_names = {'АБР1':'АБР','АБР2':'АБР(Кобра)','АЦ1':'Цистерна','АЦ2':'Бочка','АЦ3':'Волна','АЛ-3':'Лестница','АЛ-5':'Высотка',
             'АКП-3':'Колено','АКП-5':'Подъемник','АВ':'Пена','АП':'Порошок','МПУ':'МПУ','АСА':'АСА','ВС':'Воздух', 'АГДЗС':'Газовка','АКТПЛ-24':'Колено'}

def carNamer(car_name):
    result = car_names.get(car_name)
    result2 = car_names.get(car_name[:-1])
    if result:
        return result
    elif result2:
        return result2


    

def noCombatTruksmarker(truks,notСombatVehicles,key):
    status = 'combat'
    licensePlate = ''
    
    for i in truks:
        if i.licensePlate in notСombatVehicles: 
            status = notСombatVehicles[i.licensePlate][1]
            licensePlate = i.licensePlate
        if status.lower() == 'передислокация' and str(i.fireDepartment_id) !=  key:
            status = 'передислокация2' 
        
              
    if status == 'combat':    
        return ('combat',colors['#049b24'],licensePlate,1)
    elif status == 'передислокация2':
        return ('передислокация', colors['#049b24'],licensePlate,1)
    else:
        return (status.lower(), colors[notСombatVehicles[licensePlate][0]],licensePlate,0)

