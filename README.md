# SRH - SISTEMA DE RESERVAS DE HOTELES BACKEND - FASTAPI

Backend del Sistema de Reservas de Hoteles (SRH)

UNIVERSIDAD POLITÉCNICA SALESIANA - UPS


Materia: Ingeniería de Software  

Tarea: T02.03

Grupo: B

Estudiante: Andrea Murillo Medina

Fecha: 22/12/2025

Docente: Darío Huilcapi


## Gestión del Proyecto

El repositorio del proyecto fue creado en GitHub para el control de versiones
y seguimiento del desarrollo. Las tareas del proyecto fueron definidas y
asignadas a la única integrante activa del grupo Andrea Murillo, quien realizó de manera
individual todas las actividades de análisis, diseño, implementación y
documentación del backend de la aplicación.

## Cumplimiento de la SRS y la DDS

El desarrollo del backend se realizó tomando como base los requerimientos
funcionales definidos en la Tarea 02.01 (SRS) y las descripciones de diseño
planteadas en la Tarea 02.02 (DDS). Para esta implementación se desarrollaron
los módulos núcleo del sistema: Clientes, Habitaciones y Reservas, los cuales
representan el flujo principal del sistema de reservas hoteleras.

## Framework Backend

El backend de la aplicación fue implementado utilizando el framework FastAPI,
cumpliendo con las opciones permitidas en la consigna de la Tarea 02.03.

## Documentación de Servicios

Los servicios REST desarrollados se encuentran documentados mediante Swagger,
accesible a través del endpoint /docs, lo que permite visualizar y probar los
endpoints del backend de manera interactiva.

## Arquitectura del Sistema

El backend fue desarrollado siguiendo un esquema de arquitectura por capas,
separando modelos, esquemas (schemas) y controladores (routers), equivalente al
modelo/repositorio/controlador/servicio definido en la consigna, lo que permite
un código modular, ordenado y mantenible.

## Ejecución y Visualización

Para ejecutar el backend del SRH, se debe levantar el servidor con el siguiente comando:

```bash
uvicorn app.main:app --reload

Una vez iniciado el servidor, el sistema puede visualizarse en:

Página principal del backend:
http://127.0.0.1:8000

Documentación de los servicios (Swagger):
http://127.0.0.1:8000/docs