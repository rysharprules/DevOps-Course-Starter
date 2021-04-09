import pytest
from todo_app.ViewModel import ViewModel
from todo_app.Item import Item
from todo_app.Status import Status
import datetime

items = [Item('1', 'do the thing', 'To Do', '', '', ''),
    Item('2', 'do the other thing', 'Doing', '', '', ''), 
    Item('3', 'a thing that was done', 'Done', '', '', ''),
    Item('4', 'and one last thing', 'To Do', '', '', '')]

statuses = [Status('4', 'To Do'), Status('5', 'Doing'), Status('6', 'Done'), Status('7', 'Another Status')]

@pytest.fixture
def viewModel():
    return ViewModel(items, statuses)

@pytest.fixture
def done_items():
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    formattedToday = today.strftime('%Y-%m-%dT%H:%M:%S.%f%z')
    formattedYesterday = yesterday.strftime('%Y-%m-%dT%H:%M:%S.%f%z')

    return [Item('11', 'done that thing', 'Done', '', '', formattedYesterday),
                Item('12', 'done this thing', 'Done', '', '', formattedYesterday),
                Item('13', 'and this thing', 'Done', '', '', formattedToday),
                Item('14', 'and one last thing', 'Done', '', '', formattedYesterday),
                Item('15', 'and one last thing', 'Done', '', '', formattedYesterday),]


def test_getBoardStatuses(viewModel):
    # when
    board_statuses = viewModel.getBoardStatuses()

    # then
    assert len(board_statuses) == 3
    assert board_statuses[0].title == statuses[0].title
    assert board_statuses[1].title == statuses[1].title
    assert board_statuses[2].title == statuses[2].title


def test_filterItemsByStatus_todos(viewModel):
    # when
    filter_todos = viewModel.filterItemsByStatus(statuses[0])

    # then
    assert filter_todos[0].id == items[0].id
    assert filter_todos[0].title == items[0].title
    assert filter_todos[1].id == items[3].id
    assert filter_todos[1].title == items[3].title


def test_filterItemsByStatus_doing(viewModel):
    # when
    filter_doing = viewModel.filterItemsByStatus(statuses[1])

    # then
    assert filter_doing[0].id == items[1].id
    assert filter_doing[0].title == items[1].title


def test_filterItemsByStatus_done(viewModel):
    # when
    filter_done = viewModel.filterItemsByStatus(statuses[2])

    # then
    assert filter_done[0].id == items[2].id
    assert filter_done[0].title == items[2].title

@pytest.mark.parametrize("title", ["To Do", "Doing", "Done"])
def test_getStatusWithTitle(viewModel, title):
    # when
    status = viewModel.getStatusWithTitle(title)

    # then
    assert status.title == title

def test_getToDoItems(viewModel):
    # when
    todo_items = viewModel.getToDoItems()
    
    # then
    assert todo_items[0].id == items[0].id
    assert todo_items[0].title == items[0].title
    assert todo_items[1].id == items[3].id
    assert todo_items[1].title == items[3].title

def test_getDoingItems(viewModel):
    # when
    doing_items = viewModel.getDoingItems()

    # then
    assert doing_items[0].id == items[1].id
    assert doing_items[0].title == items[1].title

def test_getAllDoneItems(viewModel):
    # when
    done_items = viewModel.getAllDoneItems()

    # then
    assert done_items[0].id == items[2].id
    assert done_items[0].title == items[2].title

def test_getDoneItems_lt5(done_items):
    # given (lt5 done items)
    lt5_done_items = done_items[:4]
    lt5_done_viewModel = ViewModel(lt5_done_items, statuses)
    
    # when
    items = lt5_done_viewModel.getDoneItems()

    # then 
    assert len(items) == 4


def test_getDoneItems_today(done_items):
    # given (gt5 done items, _show_all_done_items has default value of False, and item[2] was done today)
    today_done_viewModel = ViewModel(done_items, statuses)

    # when
    today_done_items = today_done_viewModel.getDoneItems()

    # then
    assert len(today_done_items) == 1
    assert today_done_items[0].done == done_items[2].done
    assert today_done_items[0].id == done_items[2].id


def test_getDoneItems_showAllDoneItems(done_items):
    # given (gt5 done items, and _show_all_done_items has value of True)
    today_done_viewModel = ViewModel(done_items, statuses)
    today_done_viewModel.show_all_done_items = True

    # when
    today_done_items = today_done_viewModel.getDoneItems()

    # then
    assert len(today_done_items) == 5


def test_filterItemsByDoneDate_today(done_items):
    # given
    done_viewModel = ViewModel(done_items, statuses)

    # when
    results = done_viewModel.filterItemsByDoneDate(
        done_items, datetime.date.today())

    # then
    assert len(results) == 1
    assert results[0].done == done_items[2].done


def test_filterItemsByDoneDate_yesterday(done_items):
    # given
    done_viewModel = ViewModel(done_items, statuses)

    # when
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    results = done_viewModel.filterItemsByDoneDate(done_items, yesterday)

    # then
    assert len(results) == 4
    assert results[0].done == done_items[0].done
    assert results[1].done == done_items[1].done
    assert results[2].done == done_items[3].done
    assert results[3].done == done_items[4].done
