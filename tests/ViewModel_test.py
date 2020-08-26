import pytest
from ViewModel import ViewModel
from Item import Item
from Status import Status

items = [Item('1', 'do the thing', 'To Do', '', ''), 
            Item('2', 'do the other thing', 'Doing', '', ''), 
            Item('3', 'a thing that was done', 'Done', '', ''),
            Item('4', 'and one last thing', 'To Do', '', '')]

statuses = [Status('4', 'To Do'), Status('5', 'Doing'), Status('6', 'Done'), Status('7', 'Another Status')]

@pytest.fixture
def view_model():
    return ViewModel(items, statuses)


def test_getBoardStatuses(view_model):
    # when
    board_statuses = view_model.getBoardStatuses()

    # then
    assert len(board_statuses) == 3
    assert board_statuses[0].title == statuses[0].title
    assert board_statuses[1].title == statuses[1].title
    assert board_statuses[2].title == statuses[2].title


def test_filterItemsByStatus_todos(view_model):
    # when
    filter_todos = view_model.filterItemsByStatus(statuses[0])

    # then
    assert filter_todos[0].id == items[0].id
    assert filter_todos[0].title == items[0].title
    assert filter_todos[1].id == items[3].id
    assert filter_todos[1].title == items[3].title


def test_filterItemsByStatus_todos(view_model):
    # when
    filter_todos = view_model.filterItemsByStatus(statuses[0])

    # then
    assert filter_todos[0].id == items[0].id
    assert filter_todos[0].title == items[0].title
    assert filter_todos[1].id == items[3].id
    assert filter_todos[1].title == items[3].title


def test_filterItemsByStatus_doing(view_model):
    # when
    filter_doing = view_model.filterItemsByStatus(statuses[1])

    # then
    assert filter_doing[0].id == items[1].id
    assert filter_doing[0].title == items[1].title


def test_filterItemsByStatus_done(view_model):
    # when
    filter_done = view_model.filterItemsByStatus(statuses[2])

    # then
    assert filter_done[0].id == items[2].id
    assert filter_done[0].title == items[2].title

@pytest.mark.parametrize("title", ["To Do", "Doing", "Done"])
def test_getStatusWithTitle(view_model, title):
    # when
    status = view_model.getStatusWithTitle(title)

    # then
    assert status.title == title

def test_getToDoItems(view_model):
    # when
    todo_items = view_model.getToDoItems()
    
    # then
    assert todo_items[0].id == items[0].id
    assert todo_items[0].title == items[0].title
    assert todo_items[1].id == items[3].id
    assert todo_items[1].title == items[3].title

def test_getDoingItems(view_model):
    # when
    doing_items = view_model.getDoingItems()

    # then
    assert doing_items[0].id == items[1].id
    assert doing_items[0].title == items[1].title

def test_getDoneItems(view_model):
    # when
    done_items = view_model.getDoneItems()

    # then
    assert done_items[0].id == items[2].id
    assert done_items[0].title == items[2].title
