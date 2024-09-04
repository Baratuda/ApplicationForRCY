
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

def dificult_length_calculator(dict):
    result = 0
    result_dict = {}
    if  isinstance(dict, type({}.values())):
       for j in dict:
           result= result+len(j.values())
    else:
        result = 0 
        for j in dict.values():
            if isinstance(j, type({})):
                result_dict = j
                while True:
                    if type(next(iter(result_dict))) is list:
                        for i in result_dict:
                            result+=len(i)
                        break
                    result_dict = j.values() 
            if type(j) is list:
                result+=len(j)  
            
                 
    return result 


def sort_firedepartments(list_firedepartments, main_firedepartments):
    main_firedepartment = {}
    for i,j in list_firedepartments.items():
        if i in main_firedepartments: 
            main_firedepartment = {i:j}
            del list_firedepartments[i]
            break
    return dict(list(main_firedepartment.items()) + list(list_firedepartments.items()))    

romanNumber = {0:'I',1:'II', 2:'III', 3:'IV', 4:'V', 5:'VI', 6:'VII', 7:'VII', 8:'VIII', 9:'IX', 10:'X'}
def sort_number_of_firetrukset(list_firedepartments):
    if list_firedepartments.get('Резерв'):    
        res = list_firedepartments.get('Резерв')
        del list_firedepartments['Резерв']
        list_firedepartments['Резерв'] = res
    if list_firedepartments.get('Ремонт'):
        rep = list_firedepartments.get('Ремонт')
        del list_firedepartments['Ремонт']
        list_firedepartments['Ремонт'] = rep
    return list_firedepartments

def sort_firefighters(list):
    sorted_list = []
    main = ''
    for i in list:
        if i.post == 'Командир':
            sorted_list.insert(0,i)
        elif i.post == 'Нач. дежурной смены': main=i   
        else: sorted_list.append(i)
    if main: sorted_list.insert(0,main)  
    return  sorted_list      
            
    



def noCombatTruksmarker(truks,notСombatVehicles):
    status = 'combat'
    licensePlate = ''
    for i in truks:
        if i.licensePlate in notСombatVehicles: 
            status = notСombatVehicles[i.licensePlate][1]
            licensePlate = i.licensePlate
    if status == 'combat':    
        return ('combat',colors['#049b24'])
    else:
        return (status, colors[notСombatVehicles[licensePlate][0]])