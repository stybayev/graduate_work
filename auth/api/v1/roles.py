from uuid import UUID

from fastapi import APIRouter, Depends, Path, Request
from fastapi_jwt_auth import AuthJWT

from auth.core.tracer import traced
from auth.schema.roles import (AssignRoleResponse, RoleResponse, RoleSchema,
                               RoleUpdateSchema, UserPermissionsSchema)
from auth.services.roles import RoleService, get_role_service

router = APIRouter()


@router.post("/", response_model=dict)
@traced(__name__)
async def create_role(request: Request, role: RoleSchema,
                      service: RoleService = Depends(get_role_service),
                      Authorize: AuthJWT = Depends()
                      ) -> RoleResponse:
    """
    Создание роли
    """
    new_role = await service.create_role(role, Authorize=Authorize)
    return RoleResponse.from_orm(new_role)


@router.delete("/")
@traced(__name__)
async def delete_role(request: Request, role_id: UUID = None, role_name: str = None,
                      service: RoleService = Depends(get_role_service),
                      Authorize: AuthJWT = Depends()) -> dict:
    """
    Удалить роль по ID или имени.

    Параметры:
    - role_id: UUID (необязательно) - ID роли, которую нужно удалить.
    - name: str (необязательно) - Имя роли, которую нужно удалить.

    Необходимо указать либо role_id, либо name.
    """
    result = await service.delete_role(Authorize=Authorize, role_id=role_id, role_name=role_name)
    return result


@router.patch("/{role_id}")
@traced(__name__)
async def update_role(request: Request, role_id: UUID, data: RoleUpdateSchema,
                      service: RoleService = Depends(get_role_service),
                      Authorize: AuthJWT = Depends()) -> RoleResponse:
    """
    Обновить роль по ID.

    Параметры:
    - role_id: UUID - ID роли, которую нужно обновить.
    - data: RoleUpdateSchema - Данные для обновления.
    """
    updated_role = await service.update_role(role_id=role_id, data=data, Authorize=Authorize)
    return RoleResponse.from_orm(updated_role)


@router.get("/")
@traced(__name__)
async def get_roles(request: Request, service: RoleService = Depends(get_role_service)):
    """
    Просмотр всех ролей
    """
    roles = await service.get_all_roles()
    return roles


@router.post("/users/{user_id}/roles/{role_id}", response_model=AssignRoleResponse)
@traced(__name__)
async def assign_role_to_user(
        request: Request,
        user_id: UUID = Path(..., description="User ID"),
        role_id: UUID = Path(..., description="Role ID"),
        service: RoleService = Depends(get_role_service),
        Authorize: AuthJWT = Depends()
):
    """
    Назначение роли пользователю

    Этот эндпоинт позволяет назначить роль существующему пользователю в системе.

    ### Параметры:
    - **user_id**: UUID - Идентификатор пользователя.
    - **role_id**: UUID - Идентификатор роли.

    ### Возвращает:
    - **user_id**: UUID - Идентификатор пользователя.
    - **role_id**: UUID - Идентификатор роли.
    - **message**: str - Сообщение о результате операции.

    ### Исключения:
    - **404 Not Found**: Пользователь или роль не найдены.
    - **400 Bad Request**: Роль уже назначена пользователю.
    """

    result = await service.assign_role_to_user(user_id=user_id, role_id=role_id, Authorize=Authorize)
    return AssignRoleResponse(user_id=user_id, role_id=role_id, message=result['message'])


@router.delete("/users/{user_id}/roles/{role_id}")
@traced(__name__)
async def remove_role_from_user(request: Request,
                                user_id: UUID = Path(..., description="User ID"),
                                role_id: UUID = Path(..., description="Role ID"),
                                service: RoleService = Depends(get_role_service),
                                Authorize: AuthJWT = Depends()) -> dict:
    """
    Отобрать роль у пользователя
    """
    result = await service.remove_role_from_user(user_id=user_id, role_id=role_id, Authorize=Authorize)
    return result


@router.get("/users/{user_id}/permissions")
@traced(__name__)
async def check_user_permissions(request: Request,
                                 user_id: UUID = Path(..., description="User ID"),
                                 service: RoleService = Depends(get_role_service)) -> UserPermissionsSchema:
    """
    Проверка наличия прав у пользователя
    """
    result = await service.get_user_permissions(user_id=user_id)
    return result
