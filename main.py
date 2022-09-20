from datetime import date, timedelta

from simple_term_menu import TerminalMenu

list_collection = {}
class ItemContent:
    def __init__(self, name, priority, due_date):
        self.name = name
        self.priority = priority
        self.due_date = due_date

    def __repr__(self):
        return f'Item name: {self.name}, Priority: {self.priority}, Due on: {self.due_date}'

class PriorityError(Exception):
    def __init__(self):
        super().__init__('Wrong priority level!')

class InvalidInputError(Exception):
    def __init__(self):
        super().__init__('Invalid input (element missing)')

class BackToMain(Exception):
    def __init__(self):
        super().__init__('Back to Main menu!')

class BackToUpper(Exception):
    def __init__(self):
        super().__init__('Back to the upper level menu!')

class BackToListSelection(Exception):
    def __init__(self):
        super().__init__('Back to List Selection menu!')

class BackToEdit(Exception):
    def __init__(self):
        super().__init__('Back to Edit menu!')

class EmptyListCollection(Exception):
    def __init__(self):
        super().__init__('No lists available. Please create one first.')

class ListNotExist(Exception):
    def __init__(self, list_name):
        super().__init__(f'The list \'{list_name}\' does not exist! Try another one!')
        

def quit_app(input):
    if input == 'X':
        raise KeyboardInterrupt

def quit_check_main(input):
    if input == 'Q':
        raise BackToMain
    else:
        quit_app(input)

def quit_check_sub(input):
    if input == 'q':
        raise BackToUpper
    else:
        quit_check_main(input)



def add_item(list_name, item):
    item_content = item.split(',')
    item_name = item_content[0].lower()
    item_priority_level = item_content[1].lower()
    item_due_date = item_content[2]
    default_due_date= (date.today() + timedelta(days = 1)).strftime('%d/%m/%y')

    if len(item_priority_level) == 0 and len(item_due_date) != 0:
        item_content_details = ItemContent(item_name, '2', item_due_date)
    elif len(item_priority_level) == 0 and len(item_due_date) == 0:
        item_content_details = ItemContent(item_name, '2', default_due_date)
    elif len(item_priority_level) != 0 and len(item_due_date) == 0:
        item_content_details = ItemContent(item_name, item_priority_level, default_due_date)
    else:
        item_content_details = ItemContent(item_name, item_priority_level, item_due_date)

    item_details = {'Name': item_content_details.name, 'Priority': item_content_details.priority, 'Due date':item_content_details.due_date}
    print(item_details)

    items.append(item_details)
    # items_list = dict(enumerate(items))
    sorted_item_list = sorted(items, key = lambda item: (item['Priority'], item['Due date']), reverse = True )
    print(sorted_item_list)
    new_list = {list_name: sorted_item_list}
    list_collection.update(new_list)
    print(list_collection)


def name_and_priority_check(item):
    item_content = item.split(',')
    if item.count(',') == 2 and len(item_content[0]) != 0:
        if len(item_content[1]) != 0 and item_content[1] not in ['1', '2', '3']:
            raise PriorityError
        else:
            return item
    else:
        raise InvalidInputError


def validate_and_add(list_name):
    input_is_valid = False
    while not input_is_valid:
        item = input('Enter the item\'s name, priority and due date DD/MM/YY (X to exit the app or Q to back to Main Menu): ')
        quit_check_main(item)
        try:
            name_and_priority_check(item)
            add_item(list_name, item)
            input_is_valid = True
        except PriorityError as err:
            print(err)
        except InvalidInputError as err:
            print(err)
        except ValueError:
            print('Invalid date!')

def validate_and_add_edit(list_name):
    input_is_valid = False
    while not input_is_valid:
        item = input('Enter the item\'s name, priority and due date DD/MM/YY (X to exit the app, Q to back to Main Menu, q to back to the upper level menu): ')
        quit_check_sub(item)
        try:
            name_and_priority_check(item)
            add_item(list_name, item)
            input_is_valid = True
        except PriorityError as err:
            print(err)
        except InvalidInputError as err:
            print(err)
        except ValueError:
            print('Invalid date!')

def list_collection_check():
    if len(list_collection) == 0:
        raise EmptyListCollection
    
def list_check(list_name):
    if list_name.lower() not in list_collection.keys():
        raise ListNotExist(list_name)

def main_menu_selection():
    options = ['Create a new list', 'Edit an existing list', 'Delete an exiting list', 'View an existing list', 'Exit the app']
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()
    print(f"You have selected \'{options[menu_entry_index]}\'!")
    if menu_entry_index == len(options) - 1:
        raise KeyboardInterrupt
    else:
        return options[menu_entry_index]

def add_more_decision():
    options = ['Yes', 'Back to Main menu', 'Exit the app']
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()
    print(f"You have selected \'{options[menu_entry_index]}\'!")
    if menu_entry_index == len(options) - 1:
        raise KeyboardInterrupt
    elif menu_entry_index == len(options) - 2:
        raise BackToMain
    else:
        return options[menu_entry_index]

def add_more_decision_edit():
    options = ['Yes', 'Back to the upper level menu', 'Back to Main menu', 'Exit the app']
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()
    print(f"You have selected \'{options[menu_entry_index]}\'!")
    if menu_entry_index == len(options) - 1:
        raise KeyboardInterrupt
    elif menu_entry_index == len(options) - 2:
        raise BackToMain
    elif menu_entry_index == len(options) - 3:
        raise BackToUpper
    else:
        return options[menu_entry_index]

def list_selection(list_names):
    options = [*list_names, 'Back to Main menu', 'Exit the app']
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()
    print(f"You have selected the \'{options[menu_entry_index]}\' item!")
    if menu_entry_index == len(options) - 1:
        raise KeyboardInterrupt
    elif menu_entry_index == len(options) - 2:
        raise BackToMain
    else:
        return options[menu_entry_index]

def item_selection(item_name_list):
    options = [*item_name_list, 'Back to Main menu', 'Exit the app']
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()
    print(f"You have selected the \'{options[menu_entry_index]}\' item!")
    if menu_entry_index == len(options) - 1:
        raise KeyboardInterrupt
    elif menu_entry_index == len(options) - 2:
        raise BackToMain
    else:
        return options[menu_entry_index]

def how_to_edit_selection():
    options = ['Add new item', 'Modify the existing item', 'Delete the exiting item', 'Back to the upper level menu', 'Back to Main menu', 'Exit the app']
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()
    print(f"You have selected the \'{options[menu_entry_index]}\' item to edit!")
    if menu_entry_index == len(options) - 1:
        raise KeyboardInterrupt
    elif menu_entry_index == len(options) - 2:
        raise BackToMain
    elif menu_entry_index == len(options) - 3:
        raise BackToUpper
    else:
        return options[menu_entry_index]

def element_selection():
    options = ['Name', 'Priority', 'Due date', 'Back to Main menu', 'Exit the app']
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()
    print(f"You have selected the \'{options[menu_entry_index]}\' element to edit!")
    if menu_entry_index == len(options) - 1:
        raise KeyboardInterrupt
    elif menu_entry_index == len(options) - 2:
        raise BackToMain
    else:
        return options[menu_entry_index]


try:
    while True:
        print('What would you like to do?')
        try:
            match main_menu_selection():            
                case 'Create a new list':
                    items = []
                    list_name = input('Enter the name of the new list (X to exit the app or Q to back to Main Menu): ')
                    quit_check_main(list_name)
                    validate_and_add(list_name)
                    while True:
                        print('Would you like to add another item?')
                        add_more_decision()
                        validate_and_add(list_name)
                case 'Edit an existing list':
                    try:
                        while True:
                            list_collection_check()
                            list_names = list(list_collection.keys())
                            print(list_names)
                            try:
                                while True:                                
                                    print('Select which list you would like to edit:')
                                    selected_list_name = list_selection(list_names)
                                    try:
                                        while True:                                                                    
                                            print(f'How would you like to edit the \'{list_name}\' list?')
                                            selected_edit_method = how_to_edit_selection()
                                            try:
                                                match selected_edit_method:
                                                    case 'Add new item':
                                                        validate_and_add_edit(list_name)
                                                        while True:
                                                            print('Would you like to add another item?')
                                                            add_more_decision_edit()
                                                            validate_and_add_edit(list_name)
                                                    case 'Modify the existing item':
                                                        item_name_list = [item['Name'] for item in list_collection[list_name]]
                                                        print(item_name_list)
                                                        selected_item_name = item_selection(item_name_list)
                                                        selected_item = [item for item in list_collection[list_name] if item['Name'] == selected_item_name]
                                                        print(selected_item)
                                                        print(f'Which element of \'{selected_item_name}\' would you like to edit ?')
                                                        match element_selection():
                                                            case 'Name':
                                                                new_name = input('Enter the new name of the item (X to exit the app, Q to back to Main Menu or q to back to the upper level menu): ')
                                                                quit_check_sub(new_name)
                                                                selected_item['Name'] = new_name
                                                            case 'Priority':
                                                                pass
                                                            case 'Due date':
                                                                pass
                                                    case 'Delete the exiting item':
                                                        pass
                                            except BackToUpper as err:
                                                print(err)
                                    except BackToUpper as err:
                                        print(err)
                            except BackToUpper as err:
                                print(err)
                    except EmptyListCollection as err:
                        print(err)
                case 'Delete an exiting list':
                    pass
                case 'View an existing list':
                    pass
        except BackToMain as err:
            print(err)
except KeyboardInterrupt:
    print('You have existed the app!')