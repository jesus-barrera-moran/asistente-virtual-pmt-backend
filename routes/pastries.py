import uuid
from typing import Annotated, List
from fastapi import Depends, APIRouter
from models.user import User
from services.pastries_database import obtener_usuarios_por_pasteleria, obtener_documentos_por_pasteleria, obtener_pasteleria_por_id
from services.files_storage import get_all_files_from_pasteleria
from services.authentication import get_current_active_admin_user
from utils.exceptions import INTERNAL_SERVER_ERROR_EXCEPTION, PERMISSION_DENIED_EXCEPTION

router = APIRouter()

@router.get("/pastelerias/{id_pasteleria}")
async def obtener_datos_pasteleria_endpoint(
    id_pasteleria: str,
):
    try:
        # Obtener los datos de la pastelería
        pasteleria = await obtener_pasteleria_por_id(id_pasteleria)

        if "message" in pasteleria:
            raise INTERNAL_SERVER_ERROR_EXCEPTION(pasteleria["message"])

        return pasteleria

    except Exception as e:
        raise INTERNAL_SERVER_ERROR_EXCEPTION(e)

@router.get("/pastelerias/{id_pasteleria}/usuarios")
async def obtener_usuarios_endpoint(
    id_pasteleria: str,
    current_user: Annotated[dict, Depends(get_current_active_admin_user)],
):
    try:
        # Obtener los usuarios de la pastelería
        usuarios = await obtener_usuarios_por_pasteleria(id_pasteleria)

        if str(current_user.id_pasteleria) != id_pasteleria:
            raise PERMISSION_DENIED_EXCEPTION

        if "message" in usuarios:
            raise INTERNAL_SERVER_ERROR_EXCEPTION(usuarios["message"])

        # Formatear la respuesta para que coincida con la estructura solicitada
        users_response = [
            {
                "id": usuario["id_usuario"],
                "username": usuario["nombre_usuario"],
                "email": usuario["email"],
                "role": usuario["rol"],
                "enabled": not usuario["deshabilitado"]
            }
            for usuario in usuarios
        ]

        return users_response

    except Exception as e:
        raise INTERNAL_SERVER_ERROR_EXCEPTION(e)

@router.get("/pastelerias/{id_pasteleria}/files")
async def get_all_files(
    current_user: Annotated[User, Depends(get_current_active_admin_user)]
):
    try:
        # Verificar si el usuario tiene acceso a la pastelería actual
        folder_name = str(current_user.id_pasteleria)

        # Llamar a la función para obtener todos los archivos
        files = get_all_files_from_pasteleria(folder_name)

        if not files:
            return []

        return files

    except Exception as e:
        raise INTERNAL_SERVER_ERROR_EXCEPTION(e)

@router.get("/pastelerias/{id_pasteleria}/documentos")
async def get_all_documents(
    id_pasteleria: str,
    current_user: Annotated[User, Depends(get_current_active_admin_user)]
):
    try:
        # Verificar si el usuario tiene acceso a la pastelería actual
        if str(current_user.id_pasteleria) != id_pasteleria:
            raise PERMISSION_DENIED_EXCEPTION

        # Llamar a la función para obtener todos los documentos de la pastelería
        documentos = await obtener_documentos_por_pasteleria(uuid.UUID(id_pasteleria))

        if not documentos:
            return {"message": "No se encontraron documentos para esta pastelería."}

        return documentos

    except Exception as e:
        raise INTERNAL_SERVER_ERROR_EXCEPTION(e)
