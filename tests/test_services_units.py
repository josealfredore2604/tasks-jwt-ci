from unittest.mock import MagicMock, patch
from app.services import create_task, get_tasks, delete_task
from app.models import Task
from app import models

def test_create_task_unit():
  mock_db = MagicMock() 
  test_title = "Test Unit Task"
  test_user_id = 1

  task = create_task(mock_db, test_title, test_user_id)

  assert isinstance(task, Task)
  assert task.title == test_title
  assert task.owner_id == test_user_id
  mock_db.add.assert_called_once_with(task)
  mock_db.commit.assert_called_once()
  mock_db.refresh.assert_called_once_with(task)

def test_get_tasks_unit():
  mock_db = MagicMock()
  test_user_id = 1
  expected_tasks = [Task(id=1, title="Task 1"), Task(id=2, title="Task 2")]
  
  mock_db.query.return_value.filter.return_value.all.return_value = expected_tasks

  tasks = get_tasks(mock_db, test_user_id)

  assert tasks == expected_tasks
  mock_db.query.assert_called_once_with(models.Task)
  
  mock_db.query.return_value.filter.assert_called_once()
  
  mock_db.query.return_value.filter.return_value.all.assert_called_once()

def test_delete_task_unit_found():
  mock_db = MagicMock()
  task_id_to_delete = 1
  test_user_id = 1
  mock_task = Task(id=task_id_to_delete, title="Task to delete", owner_id=test_user_id)

  mock_db.query.return_value.filter.return_value.first.return_value = mock_task

  result = delete_task(mock_db, task_id_to_delete, test_user_id)

  assert result == mock_task
  mock_db.query.assert_called_once_with(models.Task)
  
  mock_db.query.return_value.filter.assert_called_once()
  
  mock_db.delete.assert_called_once_with(mock_task)
  mock_db.commit.assert_called_once()

def test_delete_task_unit_not_found():
  mock_db = MagicMock()
  task_id_to_delete = 999
  test_user_id = 1

  mock_db.query.return_value.filter.return_value.first.return_value = None

  result = delete_task(mock_db, task_id_to_delete, test_user_id)

  assert result is None
  mock_db.query.assert_called_once_with(models.Task)
  
  mock_db.query.return_value.filter.assert_called_once()
  
  mock_db.delete.assert_not_called()
  mock_db.commit.assert_not_called()