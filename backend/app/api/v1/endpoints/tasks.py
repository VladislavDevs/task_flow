from typing import Optional
from fastapi import APIRouter, Depends, Query, Response, status
from pydantic import BaseModel

from app.api.v1.dependencies import get_current_user
from app.schemas.task import TaskCreate, TaskUpdate, TaskOut, TaskListOut
from app.models.task import TaskStatus  # только для аннотаций в схемах


router = APIRouter(prefix="/tasks", tags=["tasks"])


# Эндпоинты
@router.post(
    "/",
    response_model=TaskOut,
    status_code=status.HTTP_201_CREATED,
    summary="Создать задачу"
)
def create_task(
    task_in: TaskCreate,
    current_user=Depends(get_current_user),
):
    """
    Создание новой задачи.

    Принимает: name, description, category_id, initial_assessment_seconds.
    """
    pass


@router.get(
    "/",
    response_model=TaskListOut,
    summary="Список задач"
)
def get_tasks(
    skip: int = Query(0, ge=0, description="Смещение (offset)"),
    limit: int = Query(10, ge=1, le=100, description="Лимит записей"),
    status_filter: Optional[str] = Query(
        None,
        alias="status",
        description="Фильтр по статусу: open, work, waiting, close, cancelled"
    ),
    category_id: Optional[int] = Query(
        None,
        description="Фильтр по ID категории"
    ),
    sort_by: Optional[str] = Query(
        None,
        description="Сортировка: id, status, initial_assessment_seconds"
    ),
    sort_order: Optional[str] = Query(
        "asc",
        regex="^(asc|desc)$",
        description="Порядок: asc / desc"
    ),
    current_user=Depends(get_current_user),
):
    """
    Список задач текущего пользователя.

    Поддерживает:
    - пагинацию (skip / limit)
    - фильтрацию по статусу и категории
    - сортировку по id, status, initial_assessment_seconds
    """
    pass


@router.get(
    "/{task_id}",
    response_model=TaskOut,
    summary="Получить задачу"
)
def get_task(
    task_id: int,
    current_user=Depends(get_current_user),
):
    """
    Получить одну задачу по ID.
    Только если задача принадлежит текущему пользователю.
    """
    pass


@router.put(
    "/{task_id}",
    response_model=TaskOut,
    summary="Обновить задачу"
)
def update_task(
    task_id: int,
    task_in: TaskUpdate,
    current_user=Depends(get_current_user),
):
    """
    Полное или частичное обновление задачи.

    Все поля опциональны. Обновляются только переданные.
    """
    pass


@router.patch(
    "/{task_id}/status",
    response_model=TaskOut,
    summary="Изменить статус задачи"
)
def update_task_status(
    task_id: int,
    new_status: str = Query(
        ...,
        description="Новый статус: open, work, waiting, close, cancelled"
    ),
    current_user=Depends(get_current_user),
):
    """
    Быстрое изменение статуса задачи.
    """
    pass


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить задачу"
)
def delete_task(
    task_id: int,
    current_user=Depends(get_current_user),
):
    """
    Удаление задачи.
    Только если задача принадлежит текущему пользователю.
    """
    pass