import json
import logging

ch = logging.StreamHandler() # console central_log
ch.setLevel(logging.DEBUG)
ch.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
log = logging.getLogger('MENU_CLASS')
log.setLevel(logging.DEBUG)
log.addHandler(ch)

class Menu:
    '''
    display & create text menus
    '''

    def __init__(self, Title=None):
        self.menu = {}
        if Title == None:
            self.menu['title'] = "--------------- MENU ---------------"
        elif isinstance(Title,str):
            self.menu['title'] = Title
        else:
            self.menu['title'] = "--------------- MENU ---------------"
        self.menu['fields'] = []
        self.menu['exit'] = "0. Exit script"


    def __str__(self):
        result = self.menu['title'] + "\n"
        if len(self.menu['fields']) > 0:
            for x in range(0,len(self.menu['fields'])):
                #log.info("Xx loop: " + str(x) + " " + self.menu['fields'][x])
                result += str(x+1) + ". " + self.menu['fields'][x] + "\n"
        result += self.menu['exit']
        return result

    def add_field(self,field=str,index=0):
        '''
        add a field to the menu
        :param field: string to display
        :param index:  position to insert the field if necessary
        :return: nb of fields
        '''
        if isinstance(field,str):
            if isinstance(index,int):
                if index<=0 or index > len(self.menu['fields']) :
                    self.menu['fields'].append(field)
                else:
                    self.menu['fields'].insert(index-1, field)
                return len(self.menu['fields'])
            else:
                raise TypeError('index must be integer')
        else:
            raise TypeError('field must be string')

    def mod_field(self,field,index):
        '''
        replace an existing field
        :param field: string to insert
        :param index: position field to replace
        :return:
        '''
        if isinstance(field,str):
            if isinstance(index,int):
                if index<0 or index > len(self.menu['fields']) :
                    raise ValueError("index out of menu range")
                else:
                    self.menu['fields'][index-1] = field
                return
            else:
                raise TypeError('index must be integer')
        else:
            raise TypeError('field must be string')

    def get_choice(self):
        '''
        display choice string & return index
        quit script if 0 is chosen
        :return:
        '''
        choice = ""
        while not choice.isdigit():
            choice = input("\nEnter your choice [0-" + str(len(self.menu['fields'])) + "]: ")
            if choice.isdigit():
                if int(choice) < 0 or int(choice) > len(self.menu['fields']):
                    choice = ""

        if choice == '0':
            print("Exiting..")
            exit(0)
        return choice


"""x = Menu()
x.add_field("11111")
x.add_field("22222")
x.add_field("3333",2)
x.add_field("4444")
x.add_field("66666",0)
x.add_field("222222222",2)
print(x)

c = x.get_choice()"""