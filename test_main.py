import pytest

from rich.prompt import Prompt

from datetime import datetime

import main

from to_do_list_class import EmptyList, BackToMain, BackToChooseEditMethod, BackToChooseElement, BackToChooseList, EmptyListCollection


inputs = iter(['2', 'M', 'X', 'secondlist', 'Firstlist', '1', 'firstList', 'x', 'm', 'walk dog', 'shopping', 'shopping', 'Shopping', '', 'x', 'm', '2/2/22', '03/03/33', '2', '2/', 's', 'x', 'm', '1', 'do laundry','shopping', 'Shopping', ''])

test_cases = iter(['1', '2', '3', 'test', '1', '2022-3-2', 0, 0, 1, 1])

def fake_input(prompt):
    return next(inputs)

def fake_selection(options):
    return next(test_cases)

def fake_name(all_item_names):
    return next(test_cases)

def fake_level():
    return next(test_cases)

def fake_date():
    return next(test_cases)

def fake_item(fake_name, fake_level, fake_date):
    return f'Item name: {fake_name}, Priority: {fake_level}, Due on: {fake_date}'

def fake_option(prompt, choices):
    return next(test_cases)

def fake_names(collection):
    return ['shopping', 'dishwashing']

# Test Quit functions 
# test exit app function
class TestExitApp:
    # valid input
    def test_exit(self):
        with pytest.raises(KeyboardInterrupt):
            main.exit_app('x')

    # invalid input
    def test_not_exit(self):
        assert main.exit_app('a') is None
        assert main.exit_app(1) is None
        assert main.exit_app(1.2) is None

# test Back to main menu and exit the app function
class TestExitMain:
    # valid input - back to main menu
    def test_to_main(self):
        with pytest.raises(BackToMain):
            main.exit_main_check('m')
    
    # invalid input
    def test_not_to_main(self):
        assert main.exit_main_check('a') is None
        assert main.exit_main_check(1) is None

    # valid input - exit the app
    def test_exit(self):
        with pytest.raises(KeyboardInterrupt):
            main.exit_main_check('x')

# test back to choose another edit method function
class TestToUpper:
    # valid input
    def test_to_upper(self):
        with pytest.raises(BackToChooseEditMethod):
            main.back_to_upper_menu_check('q')
    
    # invalid input
    def test_not_to_upper(self):
        assert main.back_to_upper_menu_check('m') is None

# test back to choose another list function
class TestToEdit:
    # valid input
    def test_to_edit(self):
        with pytest.raises(BackToChooseList):
            main.back_to_edit_menu_check('l')
    
    # invalid input
    def test_not_to_edit(self):
        assert main.back_to_edit_menu_check('m') is None

# test back to choose another element function
class TestChooseAnotherElement:
    # valid input
    def test_choose_another_one(self):
        with pytest.raises(BackToChooseElement):
            main.select_another_element('e')
    
    # invalid input
    def test_not_to_choose(self):
        assert main.select_another_element('m') is None

# Test the essential functions relating to the create a new to-do list feature
# test the function which is used to check if user's input has been used as a list name already
class TestListNameDuplicate:
    # valid input - case insensitive
    def test_valid(self):
        assert main.list_name_duplicate_check('a', ['b', 'c']) == 'a'
        assert main.list_name_duplicate_check('A', ['b', 'c']) == 'a'


    # invalid input (been used already)
    def test_duplicate(self):
        assert main.list_name_duplicate_check('a', ['a', 'b']) is False

    # invalid input (case insensitive)
    def test_case_insensitive(self):
        assert main.list_name_duplicate_check('AB', ['b', 'ab']) is False

# test the function which is used to obtain and return a valid list name
class TestObtainListName:
    # valid input
    def test_valid_name(self, monkeypatch):
        monkeypatch.setattr(Prompt, 'ask', fake_input) # test case ['2', 'M', 'X', 'secondlist']
        assert main.obtain_list_name(all_list_names = ['firstlist', '1'], running_time_for_test = 1) == '2'
        assert main.obtain_list_name(all_list_names = ['firstlist', '1'], running_time_for_test = 1) == 'm'
        assert main.obtain_list_name(all_list_names = ['firstlist', '1'], running_time_for_test = 1) == 'x'
        assert main.obtain_list_name(all_list_names = ['firstlist', '1'], running_time_for_test = 1) == 'secondlist'

    # invalid input - duplicates(case insensitive)
    def test_invalid_name(self, monkeypatch):
        monkeypatch.setattr(Prompt, 'ask', fake_input) # test case ['Firstlist', '1', 'firstList']
        assert main.obtain_list_name(all_list_names = ['firstlist', '1'], running_time_for_test = 1) is False
        assert main.obtain_list_name(all_list_names = ['firstlist', '1'], running_time_for_test = 1) is False
        assert main.obtain_list_name(all_list_names = ['firstlist', '1'], running_time_for_test = 1) is False

    # quit the function - exit the app
    def test_exit(self, monkeypatch):
        with pytest.raises(KeyboardInterrupt):
            monkeypatch.setattr(Prompt, 'ask', fake_input) # test case ['x']
            main.obtain_list_name(all_list_names = ['firstlist', '1'], running_time_for_test = 1)

    # quit the function - back to main menu
    def test_quit(self, monkeypatch):
        with pytest.raises(BackToMain):
            monkeypatch.setattr(Prompt, 'ask', fake_input) # test case ['m']
            main.obtain_list_name(all_list_names = ['firstlist', '1'], running_time_for_test = 1)

# test the function which is used to check if user's input has been used as an item name already
class TestItemDuplicate:
    # valid input
    def test_valid(self):
        assert main.item_duplicate_check('shopping', ['dishwashing', 'walk dog', 'do laundry']) == 'shopping'

    # invalid input - duplicates
    def test_duplicate(self):
        assert main.item_duplicate_check('walk dog', ['dishwashing', 'walk dog', 'do laundry']) is False

# test the function which is used to obtain and return a valid item name
class TestObtainItemName:
    # valid input
    def test_valid_name(self, monkeypatch):
        monkeypatch.setattr(Prompt, 'ask', fake_input) # test case ['walk dog', 'shopping']
        assert main.obtain_item_name(all_item_names = ['do laundry'], running_time_for_test = 1) == 'walk dog'
        assert main.obtain_item_name(all_item_names = ['do laundry'], running_time_for_test = 1) == 'shopping'

    # invalid input - duplicates (case insensitive)
    def test_invalid_name(self, monkeypatch):
        monkeypatch.setattr(Prompt, 'ask', fake_input) # test case ['shopping', 'Shopping']
        assert main.obtain_item_name(all_item_names = ['shopping'], running_time_for_test = 1) is False
        assert main.obtain_item_name(all_item_names = ['shopping'], running_time_for_test = 1) is False

    # invalid input - empty input
    def test_empty_input(self, monkeypatch):
        monkeypatch.setattr(Prompt, 'ask', fake_input) # test case ['']
        assert main.obtain_item_name(all_item_names = ['shopping'], running_time_for_test = 1) is False

    # quite the function - exit the app
    def test_exit(self, monkeypatch):
        with pytest.raises(KeyboardInterrupt):
            monkeypatch.setattr(Prompt, 'ask', fake_input) # test case ['x']
            main.obtain_item_name(all_item_names = ['shopping'], running_time_for_test = 1)

    # quite the function - back to main menu
    def test_quit(self, monkeypatch):
        with pytest.raises(BackToMain):
            monkeypatch.setattr(Prompt, 'ask', fake_input) # test case ['m']
            main.obtain_item_name(all_item_names = ['shopping'], running_time_for_test = 1)

# test the function which is used to check if user's input is in a valid format
class TestDateFormat:
    # valid input
    def test_valid(self):
        assert main.date_convert_format('2/2/22') == datetime(2022, 2, 2).date()
        assert main.date_convert_format('02/02/22') == datetime(2022, 2, 2).date()

    # invalid input
    def test_invalid(self):
        assert main.date_convert_format('2/2') is None
        assert main.date_convert_format('0.2/2') is None

# test the function which is used to obtain and return a valid due date
class TestObtainDueDate:
    # valid input
    def test_valid_date(self, monkeypatch):
        monkeypatch.setattr(Prompt, 'ask', fake_input) # test case ['2/2/22', '03/03/33']
        assert main.obtain_due_date(running_time_for_test = 1) 
        assert main.obtain_due_date(running_time_for_test = 1)

    # invalid input
    def test_invalid_date(self, monkeypatch):
        monkeypatch.setattr(Prompt, 'ask', fake_input) # test case ['2', '2/', 's']
        assert main.obtain_due_date(running_time_for_test = 1) is False
        assert main.obtain_due_date(running_time_for_test = 1) is False
        assert main.obtain_due_date(running_time_for_test = 1) is False

    # quite the function - exit the app
    def test_exit(self, monkeypatch):
        with pytest.raises(KeyboardInterrupt):
            monkeypatch.setattr(Prompt, 'ask', fake_input) # test case ['x']
            main.obtain_due_date(running_time_for_test = 1)

    # quite the function - back to main menu
    def test_quit(self, monkeypatch):
        with pytest.raises(BackToMain):
            monkeypatch.setattr(Prompt, 'ask', fake_input) # test case ['m']
            main.obtain_due_date(running_time_for_test = 1)

# test the function which is used to get a priority level from the user
class TestGetPriority:
    def test_get_priority(self, monkeypatch):
        monkeypatch.setattr(Prompt, 'ask', fake_option) # test case ['1', '2', '3']
        assert main.obtain_priority_level() == '1'
        assert main.obtain_priority_level() == '2'
        assert main.obtain_priority_level() == '3'

# test the function to add an item to a list
class TestAddItem:
    def test_add_item(self, monkeypatch):
        monkeypatch.setattr(main, 'obtain_item_name', fake_name) # test case ['test']
        monkeypatch.setattr(main, 'obtain_priority_level', fake_level) # test case ['1']
        monkeypatch.setattr(main, 'obtain_due_date', fake_date) # test case ['2022-3-2']
        monkeypatch.setattr(main, 'ListItem', fake_item)
        
        list_name = 'first'
        list_content = ['Item name: shopping, Priority: 1, Due on: 2022-2-2', 'Item name: do laundry, Priority: 2, Due on: 2022-2-1']
        all_item_names = ['shopping', 'do laundry']
        result = ['Item name: shopping, Priority: 1, Due on: 2022-2-2', 'Item name: do laundry, Priority: 2, Due on: 2022-2-1', 'Item name: test, Priority: 1, Due on: 2022-3-2']
        assert main.add_item(list_name, list_content, all_item_names) == result

# Test some essential functions relating to the edit an existing list feature
# test if the list which the following code works on is empty or not
class TestEmptyList:
    # empty list
    def test_empty_list(self):
        with pytest.raises(EmptyList):
            main.empty_list_check('first', {'first':[], 'second':['test']})

    # not an empty list
    def test_unempty_list(self):
        assert main.empty_list_check('first', {'first':['test'], 'second':['test']}) is None

# test if the list collection is empty or not
class TestEmptyListCollection:
    # empty list collection
    def test_empty_list_collection(self):
        with pytest.raises(EmptyListCollection):
            main.empty_list_collection_check({})

    # not an empty list collection
    def test_unempty_list_collection(self):
        assert main.empty_list_collection_check({'first':['test', '1'], 'second':['test', '2']}) is None

# test the function to update the list collection
class TestUpdateCollection:
    def test_can_update(self):
        list_name = 'first'
        list_content = [{'name': 'walk dog', 'priority': '2', 'due date': '2/2/22'}]
        list_collection = {'second': [{'name': 'shopping', 'priority': '1', 'due date': '3/3/22'}]}
        result = {'second': [{'name': 'shopping', 'priority': '1', 'due date': '3/3/22'}], 'first': [{'name': 'walk dog', 'priority': '2', 'due date': '2/2/22'}]}
        assert main.update_collection(list_name, list_content, list_collection) == result

# test the function to update the item name
class TestUpdateItemName:
    # valid input
    def test_valid_name(self, monkeypatch):
        monkeypatch.setattr(Prompt, 'ask', fake_input) # test case ['1', 'do laundry']
        all_item_names = ['shopping', 'walk dog']
        assert main.update_item_name(all_item_names, running_time_for_test = 1) == '1'
        assert main.update_item_name(all_item_names, running_time_for_test = 1) == 'do laundry'

    # invalid input - duplicates (case insensitive)
    def test_invalid_name(self, monkeypatch):
        monkeypatch.setattr(Prompt, 'ask', fake_input) # test case ['shopping', 'Shopping']
        assert main.update_item_name(['shopping'], running_time_for_test = 1) is False
        assert main.update_item_name(['shopping'], running_time_for_test = 1) is False

    # invalid input - empty input
    def test_empty_input(self, monkeypatch):
        monkeypatch.setattr(Prompt, 'ask', fake_input) # test case ['']
        assert main.update_item_name(['shopping'], running_time_for_test = 1) is False


# test the function which is used to remove an item from the list
class TestRemoveItem:
    item_name_list = ['shopping', 'dishwashing']
    def test_remove(self, monkeypatch):
        monkeypatch.setattr(main, 'item_selection', fake_selection) # test case [0, 0, 1, 1]
        monkeypatch.setattr('main.item_names', fake_names) # test case ['shopping', 'dishwashing']
        list_name = 'second'
        list_collection = {'first': [{'name': 'shopping', 'priority': '1', 'due date': '3/3/22'}, {'name': 'dishwashing', 'priority': '1', 'due date': '3/3/22'}], 'second': [{'name': 'shopping', 'priority': '1', 'due date': '3/3/22'}, {'name': 'dishwashing', 'priority': '1', 'due date': '3/3/22'}]}
        result0 = {'first': [{'name': 'shopping', 'priority': '1', 'due date': '3/3/22'}, {'name': 'dishwashing', 'priority': '1', 'due date': '3/3/22'}], 'second': [{'name': 'dishwashing', 'priority': '1', 'due date': '3/3/22'}]}
        result1 = {'first': [{'name': 'shopping', 'priority': '1', 'due date': '3/3/22'}, {'name': 'dishwashing', 'priority': '1', 'due date': '3/3/22'}], 'second': []}
        assert main.remove_item(list_name, list_collection) == result0
        assert main.remove_item(list_name, list_collection) == result1



