# SRH - SISTEMA DE RESERVAS DE HOTELES BACKEND - FASTAPI

Backend del Sistema de Reservas de Hoteles (SRH)

UNIVERSIDAD POLITÉCNICA SALESIANA - UPS

Materia: Ingeniería de Software  
Tarea: T02.03  
Grupo: B  

Integrantes:
- Andrea Murillo Medina  
- Andy Arévalo Dueñas  

Fecha: 23/12/2025  
Docente: Darío Huilcapi  

---

## Gestión del Proyecto

El repositorio del proyecto fue creado en GitHub para el control de versiones y
seguimiento del desarrollo. El proyecto fue iniciado y desarrollado inicialmente
por Andrea Murillo, incorporándose posteriormente Andy Arévalo como colaborador
en las actividades de apoyo, ajustes y revisión del backend.

El control de versiones se gestionó mediante commits progresivos, permitiendo
evidenciar el avance del desarrollo y la participación de los integrantes del
equipo.

---

## Asignación de Tareas

- Diseño e implementación del backend (FastAPI): Andrea Murillo  
- Gestión de clientes, habitaciones y reservas: Andrea Murillo  
- Documentación Swagger y README: Andrea Murillo  
- Apoyo en revisión, ajustes y mejoras del proyecto: Andy Arévalo  
- Control de versiones y repositorio GitHub: Andrea Murillo y Andy Arévalo  

---

## Cumplimiento de la SRS y la DDS

El desarrollo del backend se realizó tomando como base los requerimientos
funcionales definidos en la Tarea 02.01 (SRS) y las descripciones de diseño
planteadas en la Tarea 02.02 (DDS). Para esta implementación se desarrollaron los
módulos principales del sistema: Clientes, Habitaciones y Reservas, los cuales
representan el flujo principal del Sistema de Reservas de Hoteles.

---

## Backend y Framework

El backend del proyecto corresponde a una API REST desarrollada para el Sistema
de Reservas de Hoteles. Para su implementación se utilizó el framework FastAPI,
el cual permite la creación de servicios REST eficientes y la documentación
automática de los endpoints mediante Swagger (OpenAPI).

---

## Documentación de Servicios

Los servicios REST desarrollados se encuentran documentados mediante Swagger,
accesible a través de los siguientes endpoints:

- Swagger UI: http://127.0.0.1:8000/docs  
- OpenAPI JSON: http://127.0.0.1:8000/openapi.json  

---

## Arquitectura del Sistema

El backend fue desarrollado siguiendo una arquitectura por capas, separando los
componentes en modelos, esquemas (schemas), servicios y controladores (routers),
equivalente al esquema modelo / repositorio / controlador / servicio definido en
la consigna, lo que permite un código modular, ordenado y mantenible.

---

## Trabajo Colaborativo y Control de Versiones

El repositorio fue compartido con los integrantes del grupo mediante la
configuración de colaboradores en GitHub, permitiendo el trabajo colaborativo,
el seguimiento de cambios y el control de versiones a través de commits
progresivos realizados por cada integrante.

---

## Ejecución y Visualización

Para ejecutar el backend del SRH se debe iniciar el servidor con el siguiente
comando:

```bash
uvicorn app.main:app --reload

