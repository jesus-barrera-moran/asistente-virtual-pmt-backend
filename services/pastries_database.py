import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
from database.engine import connect_with_connector
from typing import Optional
from uuid import UUID

db_name = os.environ["BUSINESS_DATABASE_NAME"]

# Pasteleria and User Creation Service

async def obtener_pasteleria_por_id(id_pasteleria: UUID):
    engine = connect_with_connector(db_name)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Consulta para obtener los datos de la pastelería por su id_pasteleria
        result_pasteleria = session.execute(
            text(
                # "SELECT id, nombre, email, telefono, direccion, ciudad, codigo_postal, url_website, fecha_registro "
                "SELECT id, nombre, email, url_website "
                "FROM pasteleria "
                "WHERE id = :id_pasteleria"
            ),
            {
                "id_pasteleria": id_pasteleria
            }
        )

        pasteleria = result_pasteleria.fetchone()

        # Si no se encuentra la pastelería, devolver un mensaje informativo
        if not pasteleria:
            return {"message": "No se encontró la pastelería."}

        pasteleria_dict = {
            "id": pasteleria.id,
            "nombre": pasteleria.nombre,
            "email": pasteleria.email,
            # "telefono": pasteleria.telefono,
            # "direccion": pasteleria.direccion,
            # "ciudad": pasteleria.ciudad,
            # "codigo_postal": pasteleria.codigo_postal,
            "url_website": pasteleria.url_website,
            # "fecha_registro": pasteleria.fecha_registro
        }

        return pasteleria_dict

    except Exception as exception:
        session.rollback()
        raise exception
    finally:
        session.close()

# Función para obtener todos los usuarios correspondientes a una pastelería
async def obtener_usuarios_por_pasteleria(id_pasteleria: UUID):
    engine = connect_with_connector(db_name)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Consulta para obtener todos los usuarios asociados a la pastelería por su id_pasteleria
        result_usuarios = session.execute(
            text(
                "SELECT u.id, u.usuario, u.email, r.id as rol, u.deshabilitado "
                "FROM usuario u "
                "JOIN rol r ON u.id_rol = r.id "
                "WHERE u.id_pasteleria = :id_pasteleria"
            ),
            {
                "id_pasteleria": id_pasteleria
            }
        )

        usuarios = result_usuarios.fetchall()

        # Si no se encuentran usuarios, devolver un mensaje informativo
        if not usuarios:
            return {"message": "No se encontraron usuarios para esta pastelería."}

        # Estructurar la salida en una lista de diccionarios
        lista_usuarios = [
            {
                "id_usuario": usuario.id,
                "nombre_usuario": usuario.usuario,
                "email": usuario.email,
                "rol": usuario.rol,
                "deshabilitado": usuario.deshabilitado
            }
            for usuario in usuarios
        ]

        return lista_usuarios

    except Exception as exception:
        session.rollback()
        raise exception
    finally:
        session.close()

async def obtener_documentos_por_pasteleria(id_pasteleria: UUID):
    engine = connect_with_connector(db_name)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Consulta para obtener los documentos asociados a la pastelería
        result_documentos = session.execute(
            text(
                "SELECT id, nombre, nombre_interfaz "
                "FROM documento "
                "WHERE id_pasteleria = :id_pasteleria"
            ),
            {
                "id_pasteleria": id_pasteleria
            }
        )

        documentos = result_documentos.fetchall()

        # Si no se encuentran documentos, devolver un mensaje informativo
        if not documentos:
            return []

        # Estructurar la salida en una lista de diccionarios
        lista_documentos = [
            {
                "id": documento.id,
                "nombre": documento.nombre,
                "nombre_interfaz": documento.nombre_interfaz,
            }
            for documento in documentos
        ]

        return lista_documentos

    except Exception as exception:
        session.rollback()
        raise exception
    finally:
        session.close()
